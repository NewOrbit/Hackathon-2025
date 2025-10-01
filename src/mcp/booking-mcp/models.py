"""Pydantic models for Booking MCP Server"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

class BookingStatus(str, Enum):
    AVAILABLE = "available"
    HELD = "held"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class FlightClass(str, Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"

class Flight(BaseModel):
    """Flight search result"""
    flight_id: str
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    flight_class: FlightClass
    price_usd: float
    seats_available: int
    baggage_included: Dict[str, str]
    cancellation_policy: str

class Hotel(BaseModel):
    """Hotel search result"""
    hotel_id: str
    name: str
    address: str
    city: str
    country: str
    rating_stars: float
    price_per_night_usd: float
    total_price_usd: float  
    amenities: List[str]
    cancellation_policy: str
    check_in_date: date
    check_out_date: date
    room_type: str

class Activity(BaseModel):
    """Activity search result"""
    activity_id: str
    name: str
    description: str
    location: str
    duration_hours: float
    price_per_person_usd: float
    max_participants: int
    available_slots: int
    categories: List[str]  # ["museum", "outdoor", "cultural", etc.]
    cancellation_policy: str
    booking_date: date
    start_time: str

class BookingHold(BaseModel):
    """Booking hold information"""
    hold_id: str
    booking_type: str  # "flight", "hotel", "activity"
    item_id: str
    hold_expires_at: datetime
    total_price_usd: float
    cancellation_policy: str
    special_terms: Optional[str] = None

class BookingConfirmation(BaseModel):
    """Booking confirmation details"""
    confirmation_id: str
    booking_type: str
    item_id: str
    status: BookingStatus
    total_price_usd: float
    booking_date: datetime
    contact_info: Dict[str, str]
    special_instructions: Optional[str] = None

# Request models
class FlightSearchRequest(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_date: date
    return_date: Optional[date] = None
    passengers: int = 1
    flight_class: FlightClass = FlightClass.ECONOMY

class HotelSearchRequest(BaseModel):
    city: str
    country: str
    check_in_date: date
    check_out_date: date
    guests: int = 1
    rooms: int = 1

class ActivitySearchRequest(BaseModel):
    location: str
    date: date
    categories: List[str] = []
    max_price_usd: Optional[float] = None

class HoldBookingRequest(BaseModel):
    booking_type: str
    item_id: str
    passenger_details: Optional[Dict[str, Any]] = None

class ConfirmBookingRequest(BaseModel):
    hold_id: str
    payment_info: Dict[str, str]  # Mock payment info