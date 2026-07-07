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

# Expansion beyond the original 12 USC-specific sources: legitimate property
# management companies (not aggregators) operating in Mid City, DTLA,
# Koreatown, Hollywood, Culver City, and Santa Monica, found the same way as
# the original 12 - checked each candidate's own site for AppFolio branding,
# then confirmed the *.appfolio.com/listings subdomain is live and returns
# real listing cards before adding it here. "lotus.appfolio.com" was found
# during discovery but excluded - its listings are all in Arizona, so it's
# an unrelated company that happened to share a subdomain guess, not the LA
# firm ("Lotus West Properties") the search results implied.
NEIGHBORHOOD_APPFOLIO_SOURCES = [
    {"site_name": "MGMT Group", "domain": "mgmtla.com", "appfolio_subdomain": "mgmtrentalgroup"},
    {"site_name": "DTLA MGMT", "domain": "dtlamgmt.com", "appfolio_subdomain": "dtlamanagement"},
    {"site_name": "Winstar Properties", "domain": None, "appfolio_subdomain": "winstarproperties"},
    {"site_name": "EGL Properties", "domain": "eglproperties.com", "appfolio_subdomain": "eglproperties"},
    {"site_name": "LAPMG", "domain": "losangelespropertymanagementgroup.com", "appfolio_subdomain": "lapmg"},
    {"site_name": "Ben Leeds Properties", "domain": "benleedsproperties.com", "appfolio_subdomain": "benleedsproperties"},
    {"site_name": "Stern Property Management", "domain": "sternmanagement.com", "appfolio_subdomain": "sternproperty"},
    {"site_name": "Scott Properties Group", "domain": "scott-properties.com", "appfolio_subdomain": "scottproperties"},
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
