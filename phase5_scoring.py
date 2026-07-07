"""
Phase 5: hard filters, soft-filter scoring, and one-sentence explanations.

Data limitation handled here: none of our sources expose an explicit
"private room" vs "shared room" or "private bath" vs "shared bath" field for
a listing - the schema only has bedrooms/bathrooms counts for the unit. USC
off-campus housing in this market runs two common patterns: smaller
1-2-bedroom units leased as a whole apartment, and larger 3+ bedroom houses
leased by the individual bedroom (this is visible directly in the raw Orion
data, e.g. a listing titled "...Private Room" on a 7bd/4ba house priced at
$1,075/month - clearly a per-room rate, not a whole-house rate). We use
bedroom count as an explicit, documented proxy for that split rather than
inventing a field we don't have:
  - bedrooms <= 2  -> treated as "whole-unit style" (private room implied)
  - bedrooms >= 3  -> treated as "shared-house style" (rooms rented individually)
Bathroom privacy uses bathrooms-per-bedroom as its proxy: bathrooms >=
bedrooms suggests a private bath is realistic; fewer bathrooms than bedrooms
suggests a shared bath. Both are soft filters only - they nudge score, they
never eliminate a listing, since the underlying data is a heuristic, not a
confirmed fact.
"""

UNIT_SIZE_TO_BEDROOMS = {"studio": 0, "1br": 1, "2br": 2, "3br+": 3}


def pet_explicitly_no(pet_policy):
    """True only when every pet type mentioned is explicitly disallowed.
    None/unrecognized phrasing returns False (keep the listing) per the
    'null pet policy is not a hard filter' rule."""
    if not pet_policy:
        return False

    text = pet_policy.lower()
    if "pet friendly" in text or "pets ok" in text or "pets allowed" in text:
        return False

    segments = [s.strip() for s in text.split(",")]
    has_allowed = any("allowed" in seg and "not allowed" not in seg for seg in segments)
    has_not_allowed = any("not allowed" in seg for seg in segments)

    if has_allowed:
        return False
    return has_not_allowed


def passes_hard_filters(listing, prefs, distance_miles):
    """Budget over max, distance over radius, and (if the student has a pet)
    an explicit no-pets policy all remove the listing entirely."""
    if listing.rent is None or listing.rent > prefs["budget_max"]:
        return False, "over budget"

    if distance_miles is None:
        return False, "distance could not be determined"
    if distance_miles > prefs["distance_max_miles"]:
        return False, "outside distance radius"

    if prefs["has_pet"] and pet_explicitly_no(listing.pet_policy):
        return False, "pet policy explicitly disallows pets"

    return True, None


def _size_score(bedrooms, unit_size_pref):
    wanted = UNIT_SIZE_TO_BEDROOMS[unit_size_pref]
    if bedrooms is None:
        return 0.5  # unknown - neutral, don't penalize or reward

    if unit_size_pref == "3br+":
        if bedrooms >= 3:
            return 1.0
        return max(0.0, 1.0 - (3 - bedrooms) * 0.3)

    return max(0.0, 1.0 - abs(bedrooms - wanted) * 0.3)


def _room_privacy_score(bedrooms, room_privacy_pref):
    if bedrooms is None:
        return 0.5
    inferred_shared_style = bedrooms >= 3
    if room_privacy_pref == "private":
        return 0.3 if inferred_shared_style else 1.0
    return 1.0  # open to sharing a room - not penalized either way


def _bathroom_privacy_score(bedrooms, bathrooms, bathroom_privacy_pref):
    if bathroom_privacy_pref != "private":
        return 1.0
    if bedrooms is None or bathrooms is None or bedrooms == 0:
        return 0.5
    return 1.0 if bathrooms >= bedrooms else 0.3


def score_listing(listing, prefs, distance_miles):
    size_score = _size_score(listing.bedrooms, prefs["unit_size"])
    privacy_score = _room_privacy_score(listing.bedrooms, prefs["room_privacy"])
    bath_score = _bathroom_privacy_score(listing.bedrooms, listing.bathrooms, prefs["bathroom_privacy"])
    distance_score = max(0.0, 1.0 - distance_miles / prefs["distance_max_miles"])
    budget_score = max(0.0, 1.0 - listing.rent / prefs["budget_max"])

    total = (size_score * 3) + (privacy_score * 2) + (bath_score * 2) + (distance_score * 1) + (budget_score * 1)
    return total


def explain_match(listing, prefs, distance_miles):
    parts = []

    if listing.bedrooms is not None:
        wanted = UNIT_SIZE_TO_BEDROOMS[prefs["unit_size"]]
        if (prefs["unit_size"] == "3br+" and listing.bedrooms >= 3) or listing.bedrooms == wanted:
            parts.append(f"matches your {prefs['unit_size']} size preference")
        else:
            parts.append(f"has {int(listing.bedrooms)} bedroom(s), close to your {prefs['unit_size']} preference")

    parts.append(f"is {distance_miles} miles from USC (within your {prefs['distance_max_miles']}-mile radius)")

    headroom = prefs["budget_max"] - listing.rent
    parts.append(f"is ${listing.rent:.0f}/mo, ${headroom:.0f} under your budget")

    if prefs["has_pet"]:
        if listing.pet_policy:
            parts.append(f"lists a pet policy of '{listing.pet_policy}'")
        else:
            parts.append("has no stated pet policy so it wasn't ruled out for your pet")

    return ", ".join(parts[:-1]) + ", and " + parts[-1] + "." if len(parts) > 1 else parts[0] + "."


def run_matching(pool, prefs, distances_by_address, top_n=10):
    """Returns a list of (listing, score, distance, explanation), sorted best first."""
    results = []
    dropped_reasons = {}

    for listing in pool:
        distance = distances_by_address.get(listing.address)
        ok, reason = passes_hard_filters(listing, prefs, distance)
        if not ok:
            dropped_reasons[reason] = dropped_reasons.get(reason, 0) + 1
            continue

        score = score_listing(listing, prefs, distance)
        explanation = explain_match(listing, prefs, distance)
        results.append((listing, score, distance, explanation))

    results.sort(key=lambda r: r[1], reverse=True)

    print(f"Hard-filter drops: {dropped_reasons} | Survived: {len(results)} of {len(pool)}")
    return results[:top_n]
