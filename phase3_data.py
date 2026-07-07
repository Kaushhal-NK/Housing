"""
Phase 3 (LLM/manual extraction fallback) results for the two sources confirmed
usable after the quality check: Alumni Management (GOOD) and Moo Housing
(POOR but salvageable - real rent, no reliable bed/bath).

Alumni Management (alumnimgt.net/locations): Webflow CMS site. Each of the 10
"property-card" elements lists a building name, address, one or more unit
types (e.g. "1 Bed-1 Bath"), and a matching price per unit type. We take the
first unit type/price pair per property as that property's representative
listing (matches the sample rows already verified with the student).

Moo Housing (moohousing.com): Next.js site. Pricing/bed/bath are NOT in the
visible page text - they're in an embedded RSC JSON payload
(`{"id":...,"bedroomsRange":[...],"bathroomsRange":[...],"priceRange":[...]}`)
found by grepping the raw HTML. That payload actually lists 12 properties;
only 7 have "areas":["USC"] and a matching `/properties/<slug>` link on the
homepage - those 7 are Moo's USC-market listings (the other 5 are UCLA/other
markets, out of scope for this tool). bedrooms/bathrooms are ranges (whole
shared houses rented by the room), not a single unit's bed/bath count, so per
the no-guessing rule they stay null - that's exactly why this source is a
bonus/unscored list rather than a Phase 5 scoring input.
"""

from schema import Listing

ALUMNI_MANAGEMENT_LISTINGS = [
    Listing(address="1042 1/2 W. 23rd St. Los Angeles, CA 90007", rent=2200.0,
            bedrooms=1.0, bathrooms=None, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/annex-chalet-bscve"),
    Listing(address="1029-1031 W. 24th St. Los Angeles, CA 90007", rent=1900.0,
            bedrooms=1.0, bathrooms=1.0, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/the-bennet-house"),
    Listing(address="2821 S. Hoover St. Los Angeles, CA 90007", rent=1700.0,
            bedrooms=0.0, bathrooms=None, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/chateau"),
    Listing(address="131-1137 W. 27th St. Los Angeles, CA 90007", rent=2250.0,
            bedrooms=1.0, bathrooms=1.0, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/christopher"),
    Listing(address="3744 S. Flower St. Los Angeles, CA 90007", rent=1650.0,
            bedrooms=0.0, bathrooms=None, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/garret-gardens-apartments"),
    Listing(address="2611-2613 Monmouth Ave. Los Angeles, CA 90007", rent=2300.0,
            bedrooms=1.0, bathrooms=1.0, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/guilford-apartments"),
    Listing(address="2633 S. Hoover St. Los Angeles, CA 90007", rent=1700.0,
            bedrooms=0.0, bathrooms=None, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/hoover-carriage-house"),
    Listing(address="1121 W. 27th St. Los Angeles, CA 90007", rent=1950.0,
            bedrooms=1.0, bathrooms=None, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/monmouth-avenue-apartments"),
    Listing(address="2644 S. Monmouth Ave. Los Angeles, CA 90007", rent=5000.0,
            bedrooms=3.0, bathrooms=3.0, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/monmouth-house"),
    Listing(address="2815 S. Hoover St. Los Angeles, CA 90007", rent=1650.0,
            bedrooms=0.0, bathrooms=None, available_date=None, pet_policy=None,
            square_feet=None, source="Alumni Management",
            url="https://alumnimgt.net/properties/row-apartments"),
]

MOO_HOUSING_LISTINGS = [
    Listing(address="1186 W 37th Pl, Los Angeles, CA", rent=1099.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/1186-w-37th-pl"),
    Listing(address="3001 Van Buren Pl, Los Angeles, CA", rent=1289.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/3001-van-buren-pl"),
    Listing(address="3430 Walton Ave, Los Angeles, CA", rent=1339.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/3430-walton-ave"),
    Listing(address="1326 W 35th Pl, Los Angeles, CA", rent=1099.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/1326-w-35th-pl"),
    Listing(address="1137 W 37th Dr, Los Angeles, CA", rent=1460.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/1137-w-37th-dr"),
    Listing(address="1348 W 35th Pl, Los Angeles, CA", rent=1280.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/1348-w-35th-pl"),
    Listing(address="1377 W 36th Pl, Los Angeles, CA", rent=1280.0,
            bedrooms=None, bathrooms=None, available_date=None,
            pet_policy="Pet Friendly", square_feet=None, source="Moo Housing",
            url="https://moohousing.com/properties/1377-w-36th-pl"),
]


if __name__ == "__main__":
    print(f"=== Alumni Management: {len(ALUMNI_MANAGEMENT_LISTINGS)} listings ===")
    for l in ALUMNI_MANAGEMENT_LISTINGS:
        d = l.to_dict()
        print(f"  - {d['address']} | rent=${d['rent']} | bed={d['bedrooms']} bath={d['bathrooms']}")

    print(f"\n=== Moo Housing: {len(MOO_HOUSING_LISTINGS)} listings ===")
    for l in MOO_HOUSING_LISTINGS:
        d = l.to_dict()
        print(f"  - {d['address']} | rent=${d['rent']} | pets={d['pet_policy']}")
