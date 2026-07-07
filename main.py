"""End-to-end USC student housing matcher: intake -> load pools -> score -> print results."""

from intake import run_intake
from pools import build_pools
from geocode import distances_for_addresses
from phase5_scoring import run_matching


def _fmt_count(value):
    return value if value is not None else "Unknown (see listing details)"


def print_top_results(results, used_fallback):
    if not results:
        print("\nNo matches found. Every listing within your criteria was filtered out.")
        print("Try raising your monthly budget or widening your distance radius from USC, then run again.")
        return

    if used_fallback:
        print("\nOops - nothing matched your exact unit size preference. "
              "Here are some other options we think will match:")

    print(f"\nTop {len(results)} match{'es' if len(results) != 1 else ''}:\n")
    for rank, (listing, score, distance, explanation) in enumerate(results, start=1):
        d = listing.to_dict()
        print(f"{rank}. {d['address']}")
        print(f"   rent=${d['rent']:.0f} | bed={_fmt_count(d['bedrooms'])} bath={_fmt_count(d['bathrooms'])} | "
              f"distance={distance} mi | pets={d['pet_policy']} | source={d['source']}")
        print(f"   -> {explanation}")


def print_bonus_matches(bonus_pool, prefs, distances_by_address):
    """Bonus/unscored listings (missing rent or missing bed/bath) that still
    fall within the student's stated budget and distance radius, surfaced as
    a manual-check note rather than folded into the ranked results."""
    matches = []
    for listing in bonus_pool:
        if listing.rent is None or listing.rent > prefs["budget_max"]:
            continue
        distance = distances_by_address.get(listing.address)
        if distance is None or distance > prefs["distance_max_miles"]:
            continue
        matches.append((listing, distance))

    print(f"\n{'-' * 70}")
    print("BONUS (unscored) listings within your budget and distance radius,")
    print("excluded from ranking because they're missing bed/bath or other data.")
    print("Worth checking manually:")
    print(f"{'-' * 70}")

    if not matches:
        print("  (none)")
        return

    for listing, distance in matches:
        d = listing.to_dict()
        print(f"  - {d['address']} | rent=${d['rent']:.0f} | distance={distance} mi | "
              f"bed={_fmt_count(d['bedrooms'])} bath={_fmt_count(d['bathrooms'])} | "
              f"pets={d['pet_policy']} | source={d['source']}")


def main():
    print("=== USC Student Housing Matcher ===\n")
    prefs = run_intake()

    print("\nLoading listing pools...")
    scored_pool, bonus_pool = build_pools()
    print(f"Loaded {len(scored_pool)} scored listings and {len(bonus_pool)} bonus (unscored) listings.")

    all_addresses = [l.address for l in scored_pool] + [l.address for l in bonus_pool]
    distances = distances_for_addresses(all_addresses)

    results, used_fallback = run_matching(scored_pool, prefs, distances)
    print_top_results(results, used_fallback)
    print_bonus_matches(bonus_pool, prefs, distances)


if __name__ == "__main__":
    main()
