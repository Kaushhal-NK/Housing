"""
Phase 3 re-extraction for Stuho (stuho.com), upgraded from POOR to usable.
The /search results page only renders SEO boilerplate server-side (which is
why the original Phase 3 pass found addresses but no other fields), but each
individual /for-rent-building/<slug> page embeds a real per-property JSON
payload (price range, bed/bath range, square footage, available date) from
Stuho's backend (a Yardi-adjacent "rentelf"/it49.com system, not one of the 5
target platforms, so still a manual-extraction source rather than a direct feed).
Bed/bath/rent are given as ranges across a building's available units - we take
the low end of each range as the representative listing, same approach used for
Alumni Management's multi-unit-type properties. Pet policy came back as an empty
array ("UPets":[]) on every single property, meaning Stuho simply doesn't publish
pet policy data at all - stored as null, not a guess.
"""

from schema import Listing

STUHO_LISTINGS = [
    Listing(
        address='1021 W. 24th St., Los Angeles, CA 90007', rent=5400.0,
        bedrooms=6.0, bathrooms=3.0,
        available_date='2024-08-01', pet_policy=None,
        square_feet=2373.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1021-W-24th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1025 W 25th St, Los Angeles, CA 90007', rent=899.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date=None, pet_policy=None,
        square_feet=225.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1025-W-25th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1118 W. 25th St., Los Angeles, CA 90007', rent=3150.0,
        bedrooms=3.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=800.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1118-W-25th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1119 W. 29th St., Los Angeles, CA 90007', rent=2095.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=344.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1119-W-29th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1126 W. 36th Pl., Los Angeles, CA 90007', rent=2350.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=865.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1126-W-36th-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1140-1166 W. 36th Pl., Los Angeles, CA 90007', rent=1695.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=1460.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1140-1166-W-36th-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1200 W. 30th St., Los Angeles, CA 90007', rent=3350.0,
        bedrooms=2.0, bathrooms=2.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=1235.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1200-W-30th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1201 W. 27th St, Los Angeles, CA 90007', rent=3900.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=980.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1201-W-27th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1201 W. 30th St., Los Angeles, CA 90007', rent=4200.0,
        bedrooms=3.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=2358.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1201-W-30th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1222 W. 23rd St., Los Angeles, CA 90007', rent=7250.0,
        bedrooms=7.0, bathrooms=3.5,
        available_date='2025-08-01', pet_policy=None,
        square_feet=2136.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1222-W-23rd-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1223 1/2 W. 23rd St., Los Angeles, CA 90007', rent=1435.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=250.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1223-1-2-W-23rd-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1239 W 30th St, Los Angeles, Ca 90007', rent=3195.0,
        bedrooms=2.0, bathrooms=2.5,
        available_date=None, pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1239-W-30th-St-Los-Angeles-Ca-90007-USA'),
    Listing(
        address='1253 W. 36th Pl., Los Angeles, CA 90007', rent=2995.0,
        bedrooms=3.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=846.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1253-W-36th-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1280 W. Jefferson Blvd., Los Angeles, CA 90007', rent=1725.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=803.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1280-W-Jefferson-Blvd-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1283 W. 36th St., Los Angeles, CA 90007', rent=1795.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=490.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1283-W-36th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1293 W. 36th St., Los Angeles, CA 90007', rent=6000.0,
        bedrooms=5.0, bathrooms=4.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1470.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1293-W-36th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1355 W. 29th St., Los Angeles, CA 90007', rent=5340.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1100.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1355-W-29th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2318 Portland St., Los Angeles, CA 90007', rent=1595.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1709.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2318-Portland-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2335 Portland St., Los Angeles, CA 90007', rent=7500.0,
        bedrooms=10.0, bathrooms=4.5,
        available_date='2025-08-01', pet_policy=None,
        square_feet=3286.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2335-Portland-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2356 Portland St., Los Angeles, CA 90007', rent=1995.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1288.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2356-Portland-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2595 Hoover St., Los Angeles, CA 90007', rent=725.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2026-01-07', pet_policy=None,
        square_feet=589.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2595-Hoover-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2601 S. Hoover Street, Los Angeles, CA 90007', rent=1300.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/2601-S-Hoover-Street-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2620 Severance St., Los Angeles, CA 90007', rent=2050.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=615.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2620-Severance-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2633 Ellendale Pl., Los Angeles, CA 90007', rent=1500.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=400.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2633-Ellendale-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2634 Monmouth Ave., Los Angeles, CA 90007', rent=4000.0,
        bedrooms=8.0, bathrooms=8.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=2720.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2634-Monmouth-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2639 Monmouth Ave., Los Angeles, CA 90007', rent=1495.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=294.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2639-Monmouth-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2640 Menlo Ave., Los Angeles, CA 90007', rent=10800.0,
        bedrooms=9.0, bathrooms=7.5,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1026.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2640-Menlo-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2646 Menlo Ave., Los Angeles, CA 90007', rent=12000.0,
        bedrooms=8.0, bathrooms=6.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=3080.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2646-Menlo-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2647 Ellendale Pl., Los Angeles, CA 90007', rent=12995.0,
        bedrooms=8.0, bathrooms=6.5,
        available_date='2025-08-01', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/2647-Ellendale-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2649 Ellendale Pl., Los Angeles, CA 90007', rent=3900.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2649-Ellendale-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2658 Menlo Ave., Los Angeles, CA 90007', rent=3000.0,
        bedrooms=2.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1020.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2658-Menlo-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2660 Magnolia Ave, Los Angeles, CA 90007', rent=2300.0,
        bedrooms=2.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/2660-Magnolia-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2662 1/2 Orchard Ave., Los Angeles, CA 90007', rent=1385.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=222.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2662-1-2-Orchard-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2833 Menlo Ave, Los Angeles, CA 90007', rent=9625.0,
        bedrooms=4.0, bathrooms=4.5,
        available_date='2025-08-01', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/2833-Menlo-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3006 Royal St., Los Angeles, CA 90007', rent=2095.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=365.0, source="Stuho",
        url='https://stuho.com/for-rent-building/3006-Royal-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3010 Shrine Pl., Los Angeles, CA 90007', rent=5600.0,
        bedrooms=4.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1070.0, source="Stuho",
        url='https://stuho.com/for-rent-building/3010-Shrine-Pl-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3030 Shrine Place, Los Angeles, CA 90007', rent=1500.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/3030-Shrine-Place-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3416 Walton Ave., Los Angeles, CA 90007', rent=2395.0,
        bedrooms=3.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=843.0, source="Stuho",
        url='https://stuho.com/for-rent-building/3416-Walton-Ave-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3417 Catalina St., Los Angeles, CA 90007', rent=4895.0,
        bedrooms=5.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1350.0, source="Stuho",
        url='https://stuho.com/for-rent-building/3417-Catalina-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='738-42 W. 27th St., Los Angeles, CA 90007', rent=2000.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=377.0, source="Stuho",
        url='https://stuho.com/for-rent-building/738-42-W-27th-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='841 W. 23rd St., Los Angeles, CA 90007', rent=1250.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=749.0, source="Stuho",
        url='https://stuho.com/for-rent-building/841-W-23rd-St-Los-Angeles-CA-90007-USA'),
    Listing(
        address='949 W. Adams Blvd, Los Angeles, CA 90007', rent=1400.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=390.0, source="Stuho",
        url='https://stuho.com/for-rent-building/949-W-Adams-Blvd-Los-Angeles-CA-90007-USA'),
    Listing(
        address='956 1/2 W. 23rd St., Los Angeles, CA 90007', rent=1395.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=220.0, source="Stuho",
        url='https://stuho.com/for-rent-building/956-1-2-W-23rd-St-Los-Angeles-CA-90007-USA'),
]
