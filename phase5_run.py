"""Run Phase 5 scoring against the 193-listing SCORED_POOL using the two test
profiles already confirmed working in the Phase 4 intake test."""

from pools import build_pools
from geocode import distances_for_addresses
from phase5_scoring import run_matching

# Same two profiles used to confirm intake.py works correctly.
SHARED_UNIT_TEST_PROFILE = {
    "budget_max": 1400.0,
    "unit_type": "shared",
    "room_privacy": "private",
    "bathroom_privacy": "shared",
    "unit_size": "2br",
    "distance_max_miles": 2.5,
    "move_in_date": "2026-08-15",
    "has_pet": True,
}

ENTIRE_UNIT_TEST_PROFILE = {
    "budget_max": 2500.0,
    "unit_type": "entire",
    "room_privacy": "private",
    "bathroom_privacy": "private",
    "unit_size": "studio",
    "distance_max_miles": 3.0,
    "move_in_date": "2026-08-15",
    "has_pet": False,
}


def print_results(label, prefs, results):
    print(f"\n{'=' * 70}\nTOP {len(results)} RESULTS - {label}\n{'=' * 70}")
    print(f"Profile: {prefs}\n")
    for rank, (listing, score, distance, explanation) in enumerate(results, start=1):
        d = listing.to_dict()
        print(f"{rank}. {d['address']}")
        print(f"   rent=${d['rent']:.0f} | bed={d['bedrooms']} bath={d['bathrooms']} | "
              f"distance={distance} mi | pets={d['pet_policy']} | source={d['source']} | score={score:.2f}")
        print(f"   -> {explanation}")


def main():
    scored_pool, bonus_pool = build_pools()
    print(f"\nSCORED_POOL: {len(scored_pool)} listings | BONUS_POOL (unscored): {len(bonus_pool)} listings")

    addresses = [l.address for l in scored_pool]
    distances = distances_for_addresses(addresses)

    shared_results = run_matching(scored_pool, SHARED_UNIT_TEST_PROFILE, distances)
    print_results("SHARED UNIT TEST PROFILE", SHARED_UNIT_TEST_PROFILE, shared_results)

    entire_results = run_matching(scored_pool, ENTIRE_UNIT_TEST_PROFILE, distances)
    print_results("ENTIRE UNIT TEST PROFILE", ENTIRE_UNIT_TEST_PROFILE, entire_results)


if __name__ == "__main__":
    main()
