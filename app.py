"""Flask front end for the USC student housing matcher.

Listing pools are fetched and geocoded once at startup (not per-request) -
each build involves live network calls to 11 property management sites plus
OpenStreetMap geocoding (~600+ addresses, ~1 req/sec rate limit), which is
too slow to repeat on every form submit and, on a platform like Render,
too slow to do *before* the process starts listening on $PORT. Render's
deploy health check gives up and marks the deploy failed if nothing binds
the port within its scan window (confirmed in production: the 707-listing
pool took long enough that Render killed the deploy after ~5 minutes of
"No open ports detected"). So the initial load also happens in a background
thread - gunicorn binds the port immediately, and the app serves the intake
form right away; /submit shows a "still loading" message until the first
load finishes.

Two refresh paths keep that data from going stale after the initial load:
1. A background thread reloads everything once a day. Only helps while the
   process stays alive - Render's free tier spins the service down after 15
   minutes idle, so on free tier this thread may never fire between cold
   starts.
2. A /refresh endpoint that an external scheduler (Render Cron Job,
   cron-job.org, etc.) can hit on a schedule to force a reload regardless of
   tier. If REFRESH_TOKEN is set as an env var, /refresh requires
   ?token=<value> so the public internet can't trigger reloads at will;
   if unset, /refresh is open (fine for a low-stakes demo, not recommended
   once this has real traffic).
"""

import os
import sys
import threading
import time

# Line-buffer stdout so Render's logs show accurate timestamps for each
# print() as it actually happens. Without this, Python batches output and
# flushes it all at once - which made "Ready: N scored listings" appear to
# happen instantly when the real work (11 live site fetches) was still
# running, and made a genuine ~30s wait look like a stuck/broken app.
sys.stdout.reconfigure(line_buffering=True)

from flask import Flask, jsonify, render_template, request

from pools import build_pools
from geocode import distances_for_addresses
from phase5_scoring import run_matching

app = Flask(__name__)

REFRESH_INTERVAL_SECONDS = 24 * 60 * 60
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
_data_lock = threading.Lock()
_data_ready = threading.Event()

SCORED_POOL, BONUS_POOL, DISTANCES = [], [], {}

# Diagnostic state only - not used for any real logic, just so /status can
# show what THIS process (this specific gunicorn worker/PID) has actually
# done, since worker restarts mean log lines from a previous, now-dead
# worker can look like progress that never reached the one serving traffic.
_PROCESS_STARTED_AT = time.time()
_load_started_at = None
_load_finished_at = None
_last_load_error = None
_initial_load_thread = None


def _load_data():
    print(f"[pid {os.getpid()}] Loading listing pools...")
    scored_pool, bonus_pool = build_pools()
    all_addresses = [l.address for l in scored_pool] + [l.address for l in bonus_pool]
    distances = distances_for_addresses(all_addresses)
    print(f"[pid {os.getpid()}] Ready: {len(scored_pool)} scored listings, {len(bonus_pool)} bonus listings.")
    return scored_pool, bonus_pool, distances


def _apply_refresh():
    """Reload the pools and swap them in under a lock. Raises on failure so
    callers (the initial-load thread, the background loop, the /refresh
    route) can decide how to report it - either way the old data (or the
    empty initial state) stays live until a reload succeeds."""
    global SCORED_POOL, BONUS_POOL, DISTANCES
    scored_pool, bonus_pool, distances = _load_data()
    with _data_lock:
        SCORED_POOL, BONUS_POOL, DISTANCES = scored_pool, bonus_pool, distances
    _data_ready.set()
    return scored_pool, bonus_pool


def _initial_load():
    global _load_started_at, _load_finished_at, _last_load_error
    _load_started_at = time.time()
    try:
        _apply_refresh()
        _load_finished_at = time.time()
    except Exception as exc:
        _last_load_error = repr(exc)
        print(f"[pid {os.getpid()}] Initial data load failed: {exc}")


def _refresh_loop():
    while True:
        time.sleep(REFRESH_INTERVAL_SECONDS)
        try:
            _apply_refresh()
            print(f"[pid {os.getpid()}] Background refresh complete.")
        except Exception as exc:
            print(f"[pid {os.getpid()}] Background refresh failed, keeping existing data: {exc}")


_initial_load_thread = threading.Thread(target=_initial_load, daemon=True)
_initial_load_thread.start()
threading.Thread(target=_refresh_loop, daemon=True).start()


def _build_prefs_from_form(form):
    unit_type = form.get("unit_type", "entire")

    distance_raw = form.get("distance_max_miles", "").strip()
    distance_max_miles = float(distance_raw) if distance_raw else 3.0

    if unit_type == "shared":
        room_privacy = form.get("room_privacy", "private")
        bathroom_privacy = form.get("bathroom_privacy", "private")
    else:
        room_privacy = "private"
        bathroom_privacy = "private"

    return {
        "budget_max": float(form["budget_max"]),
        "unit_type": unit_type,
        "room_privacy": room_privacy,
        "bathroom_privacy": bathroom_privacy,
        "unit_size": form["unit_size"],
        "distance_max_miles": distance_max_miles,
        "move_in_date": form.get("move_in_date", ""),
        "has_pet": form.get("has_pet") == "yes",
    }


def _bonus_matches(prefs):
    matches = []
    for listing in BONUS_POOL:
        if listing.rent is None or listing.rent > prefs["budget_max"]:
            continue
        distance = DISTANCES.get(listing.address)
        if distance is None or distance > prefs["distance_max_miles"]:
            continue
        d = listing.to_dict()
        d["distance"] = distance
        matches.append(d)
    return matches


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status")
def status():
    now = time.time()
    return jsonify({
        "pid": os.getpid(),
        "process_uptime_seconds": round(now - _PROCESS_STARTED_AT, 1),
        "data_ready": _data_ready.is_set(),
        "scored_count": len(SCORED_POOL),
        "bonus_count": len(BONUS_POOL),
        "initial_load_thread_alive": _initial_load_thread.is_alive() if _initial_load_thread else None,
        "load_started_at": _load_started_at,
        "load_finished_at": _load_finished_at,
        "load_in_progress_seconds": round(now - _load_started_at, 1) if _load_started_at and not _load_finished_at else None,
        "last_load_error": _last_load_error,
    })


@app.route("/refresh", methods=["GET", "POST"])
def refresh():
    if REFRESH_TOKEN and request.args.get("token") != REFRESH_TOKEN:
        return jsonify({"status": "forbidden"}), 403

    try:
        scored_pool, bonus_pool = _apply_refresh()
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500

    return jsonify({"status": "ok", "scored_count": len(scored_pool), "bonus_count": len(bonus_pool)})


@app.route("/submit", methods=["POST"])
def submit():
    if not _data_ready.is_set():
        return render_template("loading.html"), 503

    prefs = _build_prefs_from_form(request.form)

    matched, used_fallback = run_matching(SCORED_POOL, prefs, DISTANCES)
    results = []
    for listing, score, distance, explanation in matched:
        d = listing.to_dict()
        d["distance"] = distance
        d["score"] = score
        d["explanation"] = explanation
        results.append(d)

    bonus_results = _bonus_matches(prefs)

    return render_template("results.html", results=results, bonus_results=bonus_results,
                            used_fallback=used_fallback)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
