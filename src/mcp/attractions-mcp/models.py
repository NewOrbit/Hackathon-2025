"""
Tourist attractions data models - Data classes for attractions objects.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Coordinates:
    lat: float
    lon: float


@dataclass
class Location:
    city: str
    country: str
    region: Optional[str] = ""
    coordinates: Optional[Coordinates] = None


@dataclass
class Attraction:
    id: int
    name: str
    description: str
    category: str
    location: Location
    rating: Optional[float] = None
    image_url: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[str] = None
    entry_fee: Optional[str] = None
    # Restrictions and additional info
    disability_accessible: Optional[bool] = None
    outdoors: Optional[bool] = None
    group_size: Optional[str] = None  # e.g. "1-10", "Large groups"
    age_recommendation: Optional[str] = None  # e.g. "All ages", "12+"
    age_restriction: Optional[str] = None  # e.g. "18+ only"
    budget: Optional[str] = None  # e.g. "Low", "Medium", "High"
    time_needed: Optional[str] = None  # e.g. "2-3 hours"
    pet_friendly: Optional[bool] = None
    wifi_available: Optional[bool] = None
    photogenic: Optional[bool] = None
    mood: Optional[str] = None  # e.g. "Romantic", "Adventurous"
    recommended_packing_list: Optional[List[str]] = None


@dataclass
class AttractionDetails:
    attraction: Attraction
    reviews_count: Optional[int] = None
    facilities: Optional[List[str]] = None
    best_time_to_visit: Optional[str] = None
    duration: Optional[str] = None
    # Extended restrictions (for details endpoint)
    disability_accessible: Optional[bool] = None
    outdoors: Optional[bool] = None
    group_size: Optional[str] = None
    age_recommendation: Optional[str] = None
    age_restriction: Optional[str] = None
    budget: Optional[str] = None
    time_needed: Optional[str] = None
    open_hours: Optional[str] = None
    pet_friendly: Optional[bool] = None
    wifi_available: Optional[bool] = None
    photogenic: Optional[bool] = None
    mood: Optional[str] = None
    recommended_packing_list: Optional[List[str]] = None


@dataclass
class BookingRequest:
    attraction_id: int
    visitor_name: str
    email: str
    visit_date: str
    num_visitors: int = 1
    phone: Optional[str] = None
    special_requirements: Optional[str] = None


@dataclass
class BookingResponse:
    booking_id: str
    attraction_id: int
    visitor_name: str
    visit_date: str
    num_visitors: int
    total_cost: Optional[float] = None
    booking_status: str = "confirmed"
    confirmation_code: Optional[str] = None


@dataclass
class AttractionsList:
    category: str
    location: Optional[str] = None
    total_count: int = 0
    attractions: List[Attraction] = None


@dataclass
class SearchFilters:
    location: Optional[str] = None
    category: Optional[str] = None
    rating_min: Optional[float] = None
    free_entry: Optional[bool] = None
