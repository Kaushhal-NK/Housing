"""
Phase 1 results: platform detection for the 12 target USC-area housing sites.

Only sites with a CONFIRMED platform + company ID get a direct feed integration
(Phase 2). Everything else is a Phase 3 LLM-extraction fallback candidate.
"""

CONFIRMED_APPFOLIO_SOURCES = [
    {
        "site_name": "Orion Housing",
        "domain": "orionhousing.com",
        "appfolio_subdomain": "orion",
    },
    {
        "site_name": "Nova Student Housing",
        "domain": "novastudenthousing.com",
        "appfolio_subdomain": "nsh",
    },
    {
        "site_name": "Mosaic Student Communities",
        "domain": "livewithmosaic.com",
        "appfolio_subdomain": "mosaicstudent",
    },
]

# Sites where a platform is known/suspected but no usable company ID/feed was
# recoverable, or no platform signal was found at all -> Phase 3 fallback.
FALLBACK_SOURCES = [
    {"site_name": "SC Student Housing", "domain": "southerncalstudenthousing.com",
     "url": "https://southerncalstudenthousing.com", "note": "AppFolio branding, no recoverable subdomain"},
    {"site_name": "Moo Housing", "domain": "moohousing.com",
     "url": "https://moohousing.com", "note": "AppFolio SSO domain, no recoverable subdomain"},
    {"site_name": "Alumni Management", "domain": "alumnimgt.net",
     "url": "https://alumnimgt.net", "note": "no platform signal found"},
    {"site_name": "CDI Management", "domain": "uscspots.com",
     "url": "https://uscspots.com", "note": "RentCafe (out of scope platform)"},
    {"site_name": "Stuho", "domain": "stuho.com",
     "url": "https://stuho.com", "note": "RentCafe (out of scope platform)"},
    {"site_name": "Moxie Management", "domain": "moxieusc.com",
     "url": "https://moxieusc.com", "note": "AppFolio branding, no recoverable subdomain"},
    {"site_name": "Off Campus Universe", "domain": "usc.offcampus-universe.com",
     "url": "https://usc.offcampus-universe.com", "note": "self-built platform"},
    {"site_name": "College Pads", "domain": "rentcollegepads.com",
     "url": "https://rentcollegepads.com", "note": "no embedded feed found"},
    {"site_name": "USC Off Campus Housing Portal", "domain": "nup.och101.com",
     "url": "https://nup.och101.com", "note": "site blocked fetch (403) - may need manual/browser check"},
]
