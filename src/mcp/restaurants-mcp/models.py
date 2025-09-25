"""
Restaurant data models for the restaurants-mcp service.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, date, time


@dataclass
class Ingredient:
    """Represents an ingredient in a menu item."""
    name: str
    quantity: str
    calories_per_unit: float
    protein: float  # grams
    carbs: float    # grams
    fat: float      # grams
    fiber: float    # grams
    allergens: List[str] = None

    def __post_init__(self):
        if self.allergens is None:
            self.allergens = []


@dataclass
class MenuItem:
    """Represents a menu item with nutritional information."""
    id: str
    name: str
    description: str
    price: float
    currency: str
    category: str  # appetizer, main, dessert, beverage
    ingredients: List[Ingredient]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    total_fiber: float
    allergens: List[str]
    dietary_tags: List[str]  # vegetarian, vegan, gluten-free, etc.
    preparation_time: int  # minutes
    spice_level: int  # 1-5 scale

    def __post_init__(self):
        if self.allergens is None:
            self.allergens = []
        if self.dietary_tags is None:
            self.dietary_tags = []


@dataclass
class Restaurant:
    """Represents a restaurant with location, menu, and booking info."""
    id: str
    name: str
    description: str
    cuisine_type: str
    location: str  # London or Paris
    address: str
    phone: str
    email: str
    rating: float
    price_range: str  # $, $$, $$$, $$$$
    opening_hours: Dict[str, str]  # day -> hours
    menu: List[MenuItem]
    capacity: int
    booking_advance_days: int  # how many days in advance can book
    special_features: List[str]  # outdoor seating, live music, etc.
    coordinates: Dict[str, float]  # lat, lng

    def __post_init__(self):
        if self.special_features is None:
            self.special_features = []


@dataclass
class Reservation:
    """Represents a restaurant reservation."""
    id: str
    restaurant_id: str
    customer_name: str
    customer_email: str
    customer_phone: str
    reservation_date: date
    reservation_time: time
    party_size: int
    special_requests: Optional[str] = None
    status: str = "confirmed"  # confirmed, cancelled, completed
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class BookingResponse:
    """Response for booking operations."""
    success: bool
    reservation_id: Optional[str] = None
    message: str = ""
    confirmation_details: Optional[Dict[str, Any]] = None