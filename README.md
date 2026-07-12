# USC Student Housing Matcher

A Flask web app that pulls real rental listings from USC-area property
management companies, scores them against a student's stated preferences, and
returns ranked matches with a plain-English reason for each.

**Live demo:** https://usc-housing-matcher.onrender.com

> The demo runs on Render's free tier. A cold start takes about 107 seconds
> because the app fetches 11 live property sites and geocodes their addresses
> at startup. An external uptime monitor pings `/status` every 5 minutes to
> keep the instance warm, so real visitors normally hit an already-loaded app.
> See [Deployment](#deployment) for why the cold start exists and how the
> keep-alive works.

## What it does

A student fills out a short form. The app has already loaded current listings
from the sources below, scores every listing against the student's answers,
and returns the best matches plus a separate "bonus" list of real listings
that were in range but lacked enough data to score.

**Input** (web form): budget, entire unit vs shared house, room privacy,
bathroom privacy, unit size, max distance from USC, move-in date, has a pet.

**Output**: a top-10 ranked by match score, each with address, rent,
bed/bath, distance from USC, pet policy if known, a score, and a one-sentence
explanation. Below that, an unscored bonus list of in-budget, in-radius
listings that were missing rent or bed/bath data.

## Architecture

The pipeline runs in phases, each in its own module:

| Phase | Module | Job |
|-------|--------|-----|
| 1 | `sources.py` | Catalog of target property managers and which platform each uses |
| 2 | `appfolio_feed.py` | Live-fetch and parse each confirmed AppFolio company's public `/listings` page |
| 3 | `phase3_data.py`, `phase3_stuho.py` | Listings from non-AppFolio sources, extracted during development and stored as static data |
| — | `pools.py` | Assemble the two final pools (scored vs bonus) |
| — | `geocode.py`, `geo.py` | Geocode addresses via OpenStreetMap, compute distance from USC, cache results |
| 5 | `phase5_scoring.py` | Hard filters, weighted soft scoring, exact-size tiering, explanations |
| — | `app.py` | Flask front end, background loading, refresh endpoints |

## Data sources

Listings come from two kinds of source, kept in two separate pools throughout.

**1. Live first-party fetch (AppFolio).** Eleven property management companies
host their public vacancy pages on AppFolio, for example
`orion.appfolio.com/listings`. At startup the app fetches each company's own
`/listings` page and parses the HTML with BeautifulSoup, reading stable CSS
hooks for address, rent, bed/bath, availability, and pet policy. This is a
first-party page the manager publishes to advertise vacancies, not an
aggregator. This is where the bulk of the ~725 scored listings come from and
it refreshes on every deploy or manual refresh.

**2. Static extraction (Stuho, Alumni Management, Moo Housing).** These sites
did not expose a clean AppFolio feed. Their listings were extracted during
development, some by parsing embedded per-unit JSON, some manually, and the
results are stored as Python lists in `phase3_stuho.py` and `phase3_data.py`.
**There is no runtime LLM call.** The extraction happened once while building;
the running app just reads the frozen results. These are a snapshot, not
live-fetched.

**Two pools.** The *scored pool* is every listing with enough data (a real
rent and bed/bath) to run through the matching logic. The *bonus pool* is real
listings missing rent or bed/bath, shown for manual review but never ranked.
For example, Moo Housing rents whole shared houses by the room and only
publishes bed/bath as ranges, so per the no-guessing rule those stay unscored.

## Matching logic (`phase5_scoring.py`)

A deterministic, hand-weighted scoring model. Not machine learning.

**Hard filters** remove a listing entirely:
- Rent missing or above the student's budget
- Distance missing or beyond the radius (default 3 miles)
- Student has a pet and the listing's pet policy explicitly disallows pets

Note the deliberate asymmetry: an unknown *distance* removes a listing (it
cannot be placed), but an unknown *pet policy* does not (it is kept, since pet
data is unreliable across sources).

**Soft scoring** produces a weighted total:

| Factor | Weight |
|--------|--------|
| Unit size match | 3 |
| Room privacy | 2 |
| Bathroom privacy | 2 |
| Distance closeness | 1 |
| Budget headroom | 1 |

**Documented proxies, not invented data.** No source exposes a "private room"
or "private bath" field, so the model infers from counts and says so in the
code: 3+ bedrooms is treated as a shared-house-rented-by-the-room style,
2 or fewer as whole-unit style; bathrooms >= bedrooms suggests a private bath
is realistic. These are heuristics and only nudge the score; they never
eliminate a listing.

**Exact-size tiering.** Unit size began as a pure soft filter, but a larger
unit with strong price/distance could out-rank an exact-size match, which is
wrong for a student who specifically wants, say, a studio. So exact-size
matches form their own top tier, and the app only falls back to near sizes
when there are zero exact matches. The results page flags when that fallback
was used.

Explanations are assembled from the scored fields as templated text, not
LLM-generated.

## Distance and geocoding

Addresses are geocoded with OpenStreetMap's Nominatim API (free, no key) and
distance from USC is a haversine calculation. `geocode.py` includes address
cleanup for the messy unit/range formats these sites use (compound street
numbers like `1418, 1418.5, 1420 West 28th Street`, trailing unit suffixes,
building nicknames, etc.).

`geocode_cache.json` is **committed on purpose**, not gitignored. Render's disk
is ephemeral, so without a seeded cache every cold start would re-geocode
600+ addresses at Nominatim's ~1 req/sec limit (~11 minutes). Shipping a warm
cache means a fresh deploy only geocodes genuinely new addresses.

To refresh the cache after adding sources, run `py -3 pools.py` locally to warm
it, then commit the updated `geocode_cache.json`.

## Running locally

```
py -3 -m pip install -r requirements.txt
py -3 main.py      # CLI intake + scoring, prints matches
py -3 app.py       # Flask dev server at http://localhost:5000
```

## Deployment

Deployed on Render as a gunicorn web service (`Procfile`, `gunicorn.conf.py`).

**Background loading and the gunicorn worker model.** All listings are loaded
in a background thread so the process can bind `$PORT` fast. This must be
started from gunicorn's `post_fork` hook (in `gunicorn.conf.py`), **not** at
module-import time. Gunicorn imports `app.py` once in the master process to
validate the WSGI callable, then again in each worker after forking. A thread
started at import time runs in the master, which never serves traffic, so the
worker handling `/submit` would see data that never arrives. In production this
showed up as `/submit` returning 503 for many minutes while the logs said
`Ready: N scored listings` (that "Ready" was the master's copy). Starting the
load in `post_fork` runs it inside each real worker; the `__main__` block also
starts it for plain local `python app.py` runs where there is no `post_fork`.

**Cold start.** Because startup fetches 11 live sites and geocodes addresses, a
cold start takes ~107 seconds to reach `data_ready: true`. While loading,
`/submit` returns a loading page with HTTP 503.

**Keep-alive.** Render's free tier sleeps after 15 minutes idle. An external
uptime monitor (UptimeRobot) pings
`https://usc-housing-matcher.onrender.com/status` every 5 minutes so the
instance never idles, and the ~107s load only happens on an actual redeploy or
a Render-forced restart, never to a real visitor. `/status` is used because it
is cheap and does not trigger a reload. Keep to a single free service:
Render's free tier allows 750 instance-hours a month, which covers one
always-warm app but not two.

**Keeping data fresh.** Two paths keep listings current after the initial load:
- A daily background thread reloads everything. It only fires while the process
  stays alive, so on free tier it may rarely run between restarts.
- A `/refresh` endpoint an external scheduler can hit to force a reload. If
  `REFRESH_TOKEN` is set as an env var, `/refresh` requires `?token=<value>`;
  if unset, it is open (fine for a low-stakes demo).

`/status` returns per-process diagnostics (pid, uptime, `data_ready`,
`scored_count`, load timing, last error) so you can tell what the actual
serving worker has done, independent of stale log lines from a previous worker.

## Known constraints

- The static sources (Stuho, Alumni, Moo) are a snapshot, not live-fetched.
- No runtime LLM: the extraction that produced the static sources ran during
  development only.
- Keep-alive prevents idle sleep but not the ~107s warm-up after a real restart
  or redeploy. Eliminating that would mean persisting the loaded pool to disk
  or a database so a restart reads it in seconds instead of re-fetching.
- Free tier allows one always-warm service; a second would push past Render's
  750 monthly instance-hours and suspend both.

## Tech stack

Python, Flask, gunicorn, BeautifulSoup, OpenStreetMap Nominatim. No database
(in-memory pools plus a committed geocode cache). ~1,400 lines of Python across
15 modules, with server-rendered HTML/CSS templates.
