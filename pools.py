"""Builds the two final listing pools that feed Phase 5. Kept strictly separate:
SCORED_POOL is the only one ever run through the scoring function; BONUS_POOL
is display-only and never touches the hard/soft filter logic."""

from sources import CONFIRMED_APPFOLIO_SOURCES
from appfolio_feed import fetch_appfolio_listings
from phase3_data import ALUMNI_MANAGEMENT_LISTINGS, MOO_HOUSING_LISTINGS


def build_pools():
    appfolio_priced = []
    appfolio_unpriced = []

    for src in CONFIRMED_APPFOLIO_SOURCES:
        listings = fetch_appfolio_listings(src["site_name"], src["appfolio_subdomain"])
        appfolio_priced.extend(l for l in listings if l.rent is not None)
        appfolio_unpriced.extend(l for l in listings if l.rent is None)

    scored_pool = appfolio_priced + ALUMNI_MANAGEMENT_LISTINGS
    bonus_pool = appfolio_unpriced + MOO_HOUSING_LISTINGS

    return scored_pool, bonus_pool


if __name__ == "__main__":
    scored, bonus = build_pools()
    print(f"\nSCORED_POOL: {len(scored)} listings (expected 193)")
    print(f"BONUS_POOL: {len(bonus)} listings (expected 55)")
