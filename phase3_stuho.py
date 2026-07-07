"""
Phase 3 re-extraction for Stuho (stuho.com).

First pass (superseded) scraped the visible "$X - $Y" price range text on
each /for-rent-building/<slug> page and took the low end as a representative
listing per building. That was wrong: the range spans ALL unit configs Stuho
has ever listed for that address, most of which are not actually available
right now. Each building page embeds a real per-unit JSON array (UBeds,
UBaths, URent, UActive, ...) - UActive:true is the one field that means "this
specific unit is currently for rent." Of 43 buildings, only 23 individual
units across 13 buildings are UActive:true; the other 30 buildings have zero
current availability despite still rendering historical pricing on the page.
This module lists only those 23 real, currently-active units, each with its
own accurate rent/bed/bath/sqft/available-date and its own unit-specific URL.
Pet policy is still null across the board - Stuho does not publish it.
"""

from schema import Listing

STUHO_LISTINGS = [
    Listing(
        address='1140-1166 W. 36th Pl., Los Angeles, CA 90007', rent=1695.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-04-16', pet_policy=None,
        square_feet=1165.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1140-1166-W-36th-Pl-Unit-1154-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1140-1166 W. 36th Pl., Los Angeles, CA 90007', rent=4500.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-04-16', pet_policy=None,
        square_feet=1165.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1140-1166-W-36th-Pl-Unit-1154-1-2-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1140-1166 W. 36th Pl., Los Angeles, CA 90007', rent=2100.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-04-16', pet_policy=None,
        square_feet=226.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1140-1166-W-36th-Pl-Unit-1153-3-4-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1140-1166 W. 36th Pl., Los Angeles, CA 90007', rent=2100.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-04-16', pet_policy=None,
        square_feet=226.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1140-1166-W-36th-Pl-Unit-1153-1-2-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1200 W. 30th St., Los Angeles, CA 90007', rent=3350.0,
        bedrooms=2.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=500.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1200-W-30th-St-Unit-1220-1-2-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1201 W. 27th St, Los Angeles, CA 90007', rent=3900.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=980.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1201-W-27th-St-Unit-1201-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1223 1/2 W. 23rd St., Los Angeles, CA 90007', rent=1435.0,
        bedrooms=0.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=250.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1223-1-2-W-23rd-St-Unit-1223-1-2-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1239 W 30th St, Los Angeles, Ca 90007', rent=3195.0,
        bedrooms=2.0, bathrooms=2.5,
        available_date=None, pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1239-W-30th-St-Unit-1-Los-Angeles-Ca-90007-USA'),
    Listing(
        address='1239 W 30th St, Los Angeles, Ca 90007', rent=3195.0,
        bedrooms=2.0, bathrooms=2.5,
        available_date=None, pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1239-W-30th-St-Unit-2-Los-Angeles-Ca-90007-USA'),
    Listing(
        address='1239 W 30th St, Los Angeles, Ca 90007', rent=3195.0,
        bedrooms=2.0, bathrooms=2.5,
        available_date=None, pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1239-W-30th-St-Unit-3-Los-Angeles-Ca-90007-USA'),
    Listing(
        address='1239 W 30th St, Los Angeles, Ca 90007', rent=3195.0,
        bedrooms=2.0, bathrooms=2.5,
        available_date=None, pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1239-W-30th-St-Unit-4-Los-Angeles-Ca-90007-USA'),
    Listing(
        address='1239 W 30th St, Los Angeles, Ca 90007', rent=3195.0,
        bedrooms=2.0, bathrooms=2.5,
        available_date=None, pet_policy=None,
        square_feet=1200.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1239-W-30th-St-Unit-5-Los-Angeles-Ca-90007-USA'),
    Listing(
        address='1355 W. 29th St., Los Angeles, CA 90007', rent=5340.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1100.0, source="Stuho",
        url='https://stuho.com/for-rent-building/1355-W-29th-St-Unit-1355-Los-Angeles-CA-90007-USA'),
    Listing(
        address='1355 W. 29th St., Los Angeles, CA 90007', rent=5375.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/1355-W-29th-St-Unit-1357-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2318 Portland St., Los Angeles, CA 90007', rent=6000.0,
        bedrooms=6.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1709.0, source="Stuho",
        url='https://stuho.com/for-rent-building/2318-Portland-St-Unit-2318-Los-Angeles-CA-90007-USA'),
    Listing(
        address='2595 Hoover St., Los Angeles, CA 90007', rent=4350.0,
        bedrooms=3.0, bathrooms=3.0,
        available_date='2026-01-07', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/2595-Hoover-St-Unit-Townhome-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3006 Royal St., Los Angeles, CA 90007', rent=2095.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-07-31', pet_policy=None,
        square_feet=365.0, source="Stuho",
        url='https://stuho.com/for-rent-building/3006-Royal-St-Unit-1-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3010 Shrine Pl., Los Angeles, CA 90007', rent=5600.0,
        bedrooms=4.0, bathrooms=3.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=1070.0, source="Stuho",
        url='https://stuho.com/for-rent-building/3010-Shrine-Pl-Unit-3010-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3030 Shrine Place, Los Angeles, CA 90007', rent=2195.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/3030-Shrine-Place-Unit-1BR-1BA-Pisa-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3030 Shrine Place, Los Angeles, CA 90007', rent=3000.0,
        bedrooms=2.0, bathrooms=2.0,
        available_date='2026-06-05', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/3030-Shrine-Place-Unit-2BR-2BA-Chez-Ronnee-Los-Angeles-CA-90007-USA'),
    Listing(
        address='3030 Shrine Place, Los Angeles, CA 90007', rent=3000.0,
        bedrooms=2.0, bathrooms=2.0,
        available_date='2026-06-05', pet_policy=None,
        square_feet=None, source="Stuho",
        url='https://stuho.com/for-rent-building/3030-Shrine-Place-Unit-2BR-2BA-Habitat-Soozee-I-Los-Angeles-CA-90007-USA'),
    Listing(
        address='738-42 W. 27th St., Los Angeles, CA 90007', rent=2100.0,
        bedrooms=2.0, bathrooms=2.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=707.0, source="Stuho",
        url='https://stuho.com/for-rent-building/738-42-W-27th-St-Unit-2-Los-Angeles-CA-90007-USA'),
    Listing(
        address='738-42 W. 27th St., Los Angeles, CA 90007', rent=2100.0,
        bedrooms=1.0, bathrooms=1.0,
        available_date='2025-08-01', pet_policy=None,
        square_feet=325.0, source="Stuho",
        url='https://stuho.com/for-rent-building/738-42-W-27th-St-Unit-33-Los-Angeles-CA-90007-USA'),
]
