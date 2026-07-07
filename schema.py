"""Standard listing schema shared by every source (confirmed feed or LLM fallback)."""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Listing:
    address: Optional[str]
    rent: Optional[float]
    bedrooms: Optional[float]
    bathrooms: Optional[float]
    available_date: Optional[str]
    pet_policy: Optional[str]
    square_feet: Optional[float]
    source: str
    url: Optional[str] = None

    def to_dict(self):
        return asdict(self)
