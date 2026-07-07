"""Flask front end for the USC student housing matcher.

Listing pools are fetched and geocoded once at startup (not per-request) -
each build involves live network calls to 3 property management sites plus
OpenStreetMap geocoding, which is too slow to repeat on every form submit.
"""

import os

from flask import Flask, render_template, request

from pools import build_pools
from geocode import distances_for_addresses
from phase5_scoring import run_matching

app = Flask(__name__)

print("Loading listing pools at startup...")
SCORED_POOL, BONUS_POOL = build_pools()
ALL_ADDRESSES = [l.address for l in SCORED_POOL] + [l.address for l in BONUS_POOL]
DISTANCES = distances_for_addresses(ALL_ADDRESSES)
print(f"Ready: {len(SCORED_POOL)} scored listings, {len(BONUS_POOL)} bonus listings.")


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


@app.route("/submit", methods=["POST"])
def submit():
    prefs = _build_prefs_from_form(request.form)

    matched = run_matching(SCORED_POOL, prefs, DISTANCES)
    results = []
    for listing, score, distance, explanation in matched:
        d = listing.to_dict()
        d["distance"] = distance
        d["score"] = score
        d["explanation"] = explanation
        results.append(d)

    bonus_results = _bonus_matches(prefs)

    return render_template("results.html", results=results, bonus_results=bonus_results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
