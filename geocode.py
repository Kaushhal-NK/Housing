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
    """Unit/apartment/building-nickname suffixes (e.g. '- #3', 'Unit 302',
    '- Whitney Manor') confuse Nominatim's street matching. Strip them and
    geocode the underlying street address instead."""
    street_part, _, rest = address.partition(",")
    street_part = re.sub(r"#\s*\w+\s*$", "", street_part)
    street_part = re.sub(r"\bUnit\s*\w+\s*$", "", street_part, flags=re.I)
    street_part = re.sub(r"-\s*[A-Za-z][A-Za-z ]*$", "", street_part)
    street_part = street_part.strip(" -")
    return f"{street_part},{rest}" if rest else street_part


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
