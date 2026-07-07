"""Geocode listing addresses and compute straight-line distance from USC using
OpenStreetMap's free Nominatim API (no key required). Results are cached to
disk since the same handful of streets repeat across many listings/units."""

import json
import math
import os
import re
import time

import requests

USC_LAT, USC_LON = 34.0224, -118.2851

CACHE_PATH = os.path.join(os.path.dirname(__file__), "geocode_cache.json")
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "usc-housing-matcher/1.0 (student project, contact: n/a)"}


def _load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def _haversine_miles(lat1, lon1, lat2, lon2):
    r_miles = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r_miles * math.asin(math.sqrt(a))


def _strip_unit_suffix(address):
    """Unit/apartment/building-nickname suffixes confuse Nominatim's street
    matching. Handles the patterns actually seen across the 12 original USC
    sources plus the Mid City/DTLA/Koreatown/Hollywood/Culver City/Santa
    Monica expansion sources:
      - trailing '#3', 'Unit 302', '- Whitney Manor' (alphabetic nickname)
      - trailing NUMERIC unit suffixes: '- 107', '- 1351', '- A' (this was
        the single biggest source of geocoding failures after the expansion -
        the old regex only matched alphabetic dash-suffixes)
      - 'APT 21' / 'Unit 302' sitting as its own comma-separated segment
        between the street and city, e.g. '123 Main St, APT 21, Los Angeles, CA'
      - compound/range street numbers like '1273-1275.5 W 35th St' or
        '1418, 1418.5, 1420, 1420.5 West 28th Street' - collapsed to the
        first street number only, since Nominatim can't parse a numeric range
        as a single street address
    """
    parts = [p.strip() for p in address.split(",")]
    if len(parts) < 3:
        return address  # can't confidently split street vs city vs state

    state_zip = parts[-1]
    city = parts[-2]
    street_parts = parts[:-2]

    # Drop any segment that's purely a unit/apartment marker (e.g. "APT 21").
    # Everything else gets joined with spaces, not commas - a compound street
    # number range like "1418, 1418.5, 1420, 1420.5 West 28th Street" only
    # parses correctly if we stop treating those internal commas as real
    # field separators.
    street_parts = [s for s in street_parts if not re.match(r"^(apt\.?|unit|#)\s*[\w-]*$", s, re.I)]
    street_blob = " ".join(street_parts) if street_parts else parts[0]

    # Collapse a compound/range street number down to just the first number,
    # e.g. "1273-1275.5 W 35th St" -> "1273 W 35th St", or
    # "1418 1418.5 1420 1420.5 West 28th Street" -> "1418 West 28th Street".
    m = re.match(r"\s*(\d+)[\d.\-–,\s/]*?\s+([A-Za-z].*)", street_blob)
    if m:
        street_blob = f"{m.group(1)} {m.group(2)}"

    street_blob = re.sub(r"#\s*\w+\s*$", "", street_blob)
    street_blob = re.sub(r"\bUnit\s*\w+\s*$", "", street_blob, flags=re.I)
    street_blob = re.sub(r"-\s*\w+\s*$", "", street_blob)  # trailing "- 107", "- A", "- Whitney Manor"
    # A bare trailing number with no letters (e.g. "Western Ave 10237") is a
    # repeated-unit-number artifact, not a real street name - seen from one
    # company that writes "10237 Western Ave, 10237- A" (street number
    # repeated as a unit prefix). Strip it.
    street_blob = re.sub(r"\s+\d+\s*$", "", street_blob)
    street_blob = re.sub(r"\s{2,}", " ", street_blob).strip(" -")

    return f"{street_blob}, {city}, {state_zip}"


def _query_nominatim(query, timeout):
    resp = requests.get(
        NOMINATIM_URL,
        params={"q": query, "format": "json", "limit": 1},
        headers=HEADERS,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def geocode_address(address, cache, timeout=10):
    """Returns (lat, lon) or None. Mutates cache in place; caller saves it."""
    if address in cache:
        return tuple(cache[address]) if cache[address] else None

    try:
        results = _query_nominatim(address, timeout)
        if not results:
            cleaned = _strip_unit_suffix(address)
            if cleaned != address:
                time.sleep(1.1)
                results = _query_nominatim(cleaned, timeout)
    except requests.RequestException:
        cache[address] = None
        return None

    if not results:
        cache[address] = None
        return None

    lat, lon = float(results[0]["lat"]), float(results[0]["lon"])
    cache[address] = [lat, lon]
    return lat, lon


def distances_for_addresses(addresses, rate_limit_seconds=1.1):
    """Geocode a list of (possibly repeated) addresses once each, return
    dict address -> distance_from_usc_miles (float) or None if ungeocodable."""
    cache = _load_cache()
    unique_addresses = sorted(set(a for a in addresses if a))

    to_fetch = [a for a in unique_addresses if a not in cache]
    print(f"Geocoding {len(to_fetch)} new addresses ({len(unique_addresses)} unique, "
          f"{len(unique_addresses) - len(to_fetch)} already cached)...")

    for i, address in enumerate(to_fetch):
        geocode_address(address, cache)
        if (i + 1) % 20 == 0:
            _save_cache(cache)
            print(f"  ...{i + 1}/{len(to_fetch)}")
        time.sleep(rate_limit_seconds)

    _save_cache(cache)

    distances = {}
    for address in unique_addresses:
        coords = cache.get(address)
        if coords:
            distances[address] = round(_haversine_miles(USC_LAT, USC_LON, coords[0], coords[1]), 2)
        else:
            distances[address] = None

    return distances
