"""
Geographic guard for Phase 2 sources.

Checked the AppFolio listings search form for a city/state/zip query
parameter (it exposes filters[bedrooms], filters[bathrooms],
filters[market_rent_from/to], filters[cats], filters[dogs],
filters[desired_move_in], and a property-name autocomplete field -
no location filter). Since the feed itself can't restrict results
geographically, we drop out-of-area listings (e.g. the Orion "Greeley, CO"
property) right after parsing the address, before rent/bed/bath/etc are
even extracted.
"""

LA_COUNTY_CITIES = {
    "agoura hills", "alhambra", "arcadia", "artesia", "avalon", "azusa",
    "baldwin park", "bell", "bell gardens", "bellflower", "beverly hills",
    "bradbury", "burbank", "calabasas", "carson", "cerritos", "claremont",
    "commerce", "compton", "covina", "cudahy", "culver city", "diamond bar",
    "downey", "duarte", "el monte", "el segundo", "gardena", "glendale",
    "glendora", "hawaiian gardens", "hawthorne", "hermosa beach",
    "hidden hills", "huntington park", "industry", "inglewood", "irwindale",
    "la canada flintridge", "la cañada flintridge", "la habra heights",
    "la mirada", "la puente", "la verne", "lakewood", "lancaster",
    "lawndale", "lomita", "long beach", "los angeles", "lynwood", "malibu",
    "manhattan beach", "maywood", "monrovia", "montebello", "monterey park",
    "norwalk", "palmdale", "palos verdes estates", "paramount", "pasadena",
    "pico rivera", "pomona", "rancho palos verdes", "redondo beach",
    "rolling hills", "rolling hills estates", "rosemead", "san dimas",
    "san fernando", "san gabriel", "san marino", "santa clarita",
    "santa fe springs", "santa monica", "sierra madre", "signal hill",
    "south el monte", "south gate", "south pasadena", "temple city",
    "torrance", "vernon", "walnut", "west covina", "west hollywood",
    "westlake village", "whittier",
    # common unincorporated LA County communities near USC / South LA
    "east los angeles", "marina del rey", "athens", "florence-graham",
    "willowbrook", "view park-windsor hills", "ladera heights", "del aire",
    "westmont", "walnut park", "west athens", "lennox",
    # LA neighborhoods that show up as their own "city" value in listing data
    # rather than under "Los Angeles" - added for the Mid City/DTLA/Koreatown/
    # Hollywood/Culver City/Santa Monica expansion. Note Koreatown, Mid City,
    # and DTLA listings already come through under the generic "Los Angeles"
    # city label, so they don't need separate entries here. Deliberately NOT
    # adding San Fernando Valley neighborhoods (Sherman Oaks, Van Nuys, Reseda,
    # Encino, Tarzana, Canoga Park, Winnetka, Northridge, North Hollywood,
    # Porter Ranch) or far-north LA County (Castaic, Santa Clarita) - those are
    # real LA County cities/neighborhoods but genuinely far from every target
    # area, so they're excluded on purpose, not missed.
    "hollywood", "west los angeles", "venice", "pacific palisades",
}


def is_la_county_address(address):
    """Parse '<street>, <city>, <ST> <zip>' and check city+state against LA County."""
    if not address:
        return False
    parts = [p.strip() for p in address.split(",")]
    if len(parts) < 3:
        return False

    city = parts[-2].strip().lower()
    state_zip_tokens = parts[-1].split()
    state = state_zip_tokens[0].lower() if state_zip_tokens else ""

    return state == "ca" and city in LA_COUNTY_CITIES
