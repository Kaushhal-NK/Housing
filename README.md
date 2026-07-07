# USC Student Housing Matcher

Pulls real listings from confirmed USC-area property management sources, scores
them against a student's stated preferences, and returns the top matches.

## Setup

```
py -3 -m pip install -r requirements.txt
```

## Run

```
py -3 main.py
```

This runs the intake questionnaire (budget, unit/room/bathroom privacy, unit
size, distance from USC, move-in date, pet), then fetches and scores live
listings against your answers, then prints your top matches followed by a
bonus list of unscored listings (missing rent or bed/bath data) that still
fall within your budget and distance radius.

## Notes

- `geocode_cache.json` is created automatically the first time you run
  `main.py` (or any script that calls `geocode.distances_for_addresses`). It
  stores the lat/long looked up for each listing address so repeat runs don't
  re-query the OpenStreetMap geocoding service for addresses already resolved.
  Safe to delete if you want a clean re-geocode; it will just regenerate.
- Listing data comes from two pools, kept separate throughout: the scored
  pool (listings with enough data to run through the matching/scoring logic)
  and the bonus pool (real listings missing rent or bed/bath, shown for
  manual review but never ranked).
