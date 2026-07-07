"""
Phase 2: pull structured listing data directly from AppFolio's public listings
page for a confirmed company subdomain (e.g. https://orion.appfolio.com/listings).

AppFolio does not expose an unauthenticated listings.json endpoint (confirmed by
direct request - see project notes). What IS public and unauthenticated is the
server-rendered /listings page itself, which every AppFolio-hosted property
manager uses to advertise vacancies on their own website. Each listing card is
rendered with stable CSS hooks (js-listing-address, js-listing-pet-policy, the
detail-box__label/__value pairs, etc). We parse that HTML directly rather than
scraping an aggregator - this is the property manager's own first-party page.
"""

import re
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from schema import Listing
from geo import is_la_county_address

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html",
}


def _parse_money(text: Optional[str]) -> Optional[float]:
    if not text:
        return None
    digits = re.sub(r"[^\d.]", "", text)
    if not digits:
        return None
    value = float(digits)
    # Some property managers post "$0" as a placeholder when rent isn't set
    # yet (e.g. a "Leasing Special" card with no unit details) - that's not
    # a real price, so treat it as missing rather than a $0/mo listing.
    return value if value > 0 else None


def _parse_bed_bath(text: Optional[str]):
    """'7 bd / 4 ba' -> (7.0, 4.0). 'Studio / 1 ba' -> (0.0, 1.0)."""
    if not text:
        return None, None
    text = text.strip()

    bed_match = re.search(r"([\d.]+)\s*bd", text, re.I)
    if bed_match:
        bedrooms = float(bed_match.group(1))
    elif re.search(r"studio", text, re.I):
        bedrooms = 0.0
    else:
        bedrooms = None

    bath_match = re.search(r"([\d.]+)\s*ba", text, re.I)
    bathrooms = float(bath_match.group(1)) if bath_match else None

    return bedrooms, bathrooms


def fetch_appfolio_listings(site_name: str, subdomain: str, timeout: int = 20) -> List[Listing]:
    """Fetch and parse the public /listings page for one AppFolio company."""
    url = f"https://{subdomain}.appfolio.com/listings"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as exc:
        print(f"[{site_name}] request failed: {exc}. Skipping source.")
        return []

    if resp.status_code != 200:
        print(f"[{site_name}] non-200 response ({resp.status_code}) from {url}. Skipping source.")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("div.listing-item.result")
    if not cards:
        print(f"[{site_name}] 0 listing cards found on {url}. Skipping source.")
        return []

    total_before = len(cards)
    listings = []
    for card in cards:
        address_el = card.select_one(".js-listing-address")
        address = address_el.get_text(strip=True) if address_el else None

        # Geo hard filter runs first, before any other field is parsed - the
        # AppFolio feed has no city/state/zip query param (checked the search
        # form: only bedrooms/bathrooms/rent range/pets/move-in date/property
        # autocomplete are supported), so out-of-area cards like Orion's
        # Greeley, CO property are dropped here instead of at Phase 5.
        if not is_la_county_address(address):
            continue

        facts = {}
        for item in card.select(".detail-box__item"):
            label_el = item.select_one(".detail-box__label")
            value_el = item.select_one(".detail-box__value")
            if label_el and value_el:
                facts[label_el.get_text(strip=True).lower()] = value_el.get_text(strip=True)

        rent = _parse_money(facts.get("rent"))
        bedrooms, bathrooms = _parse_bed_bath(facts.get("bed / bath"))
        square_feet = _parse_money(facts.get("square feet"))
        available_date = facts.get("available")

        pet_el = card.select_one(".js-listing-pet-policy")
        pet_policy = None
        if pet_el:
            pet_policy = pet_el.get_text(strip=True).replace("Pet Policy:", "").strip() or None

        detail_link = card.select_one(".js-link-to-detail")
        listing_url = f"https://{subdomain}.appfolio.com{detail_link['href']}" if detail_link else None

        listings.append(Listing(
            address=address,
            rent=rent,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            available_date=available_date,
            pet_policy=pet_policy,
            url=listing_url,
            square_feet=square_feet,
            source=site_name,
        ))

    total_after = len(listings)
    dropped = total_before - total_after
    print(f"[{site_name}] geo filter: {total_before} listings before -> "
          f"{total_after} after ({dropped} out-of-LA-County listing(s) dropped)")

    return listings
