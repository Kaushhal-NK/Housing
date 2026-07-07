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

- `geocode_cache.json` stores the lat/long looked up for each listing address
  so repeat runs don't re-query OpenStreetMap for addresses already resolved.
  It's created automatically if missing, but **it's committed to the repo on
  purpose** rather than gitignored: Render's disk is ephemeral, so without a
  seeded cache every cold start would re-geocode all ~600+ addresses from
  scratch at OpenStreetMap's ~1 req/sec rate limit (~11 minutes). Shipping a
  warm cache means a fresh deploy only has to geocode genuinely new addresses,
  which is fast.
  - **To refresh it** (e.g. after adding new listing sources), run
    `py -3 pools.py` locally to warm the cache, confirm no unexpected new
    nulls with `py -3 -c "import json; c=json.load(open('geocode_cache.json'));
    print(sum(1 for v in c.values() if v is None), 'unresolved of', len(c))"`,
    then commit the updated file.
- Listing data comes from two pools, kept separate throughout: the scored
  pool (listings with enough data to run through the matching/scoring logic)
  and the bonus pool (real listings missing rent or bed/bath, shown for
  manual review but never ranked).
