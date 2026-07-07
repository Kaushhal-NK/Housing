"""Phase 2: fetch confirmed AppFolio sources, apply the geo filter, split priced
vs. unpriced listings, and print the first 3 real listings from each source."""

from sources import CONFIRMED_APPFOLIO_SOURCES
from appfolio_feed import fetch_appfolio_listings

PRICED_LISTINGS = []    # -> feeds Phase 5 scoring
UNPRICED_LISTINGS = []  # -> "coming soon / unposted" bonus list, excluded from scoring

for src in CONFIRMED_APPFOLIO_SOURCES:
    site_name = src["site_name"]
    subdomain = src["appfolio_subdomain"]
    print(f"\n=== {site_name} ({subdomain}.appfolio.com) ===")

    listings = fetch_appfolio_listings(site_name, subdomain)

    priced = [l for l in listings if l.rent is not None]
    unpriced = [l for l in listings if l.rent is None]
    print(f"Priced listings: {len(priced)} | Unposted-rent listings: {len(unpriced)}")

    for listing in listings[:3]:
        d = listing.to_dict()
        print(f"  - {d['address']}")
        print(f"    rent=${d['rent']} | bed={d['bedrooms']} bath={d['bathrooms']} | "
              f"sqft={d['square_feet']} | available={d['available_date']} | "
              f"pets={d['pet_policy']}")

    PRICED_LISTINGS.extend(priced)
    UNPRICED_LISTINGS.extend(unpriced)

print("\n" + "=" * 60)
print("PHASE 2 SUMMARY")
print("=" * 60)
print(f"Total priced listings moving into Phase 5 scoring: {len(PRICED_LISTINGS)}")
print(f"Total unposted-rent listings (bonus list, excluded from scoring): {len(UNPRICED_LISTINGS)}")

if UNPRICED_LISTINGS:
    print("\n--- BONUS LIST: coming soon / unposted pricing (not scored) ---")
    for listing in UNPRICED_LISTINGS:
        d = listing.to_dict()
        print(f"  - {d['address']} | bed={d['bedrooms']} bath={d['bathrooms']} | "
              f"available={d['available_date']} | source={d['source']}")
