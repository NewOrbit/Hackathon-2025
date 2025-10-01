"""
Cinema data models - Data classes for movies and reservations.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, date, time

@dataclass
class MovieShowing:
    """Represents a movie showing in the cinema"""
    title: str
    description: str
    date: date  # Date of the showing
    time: time  # Time of the showing
    room: str   # Cinema room/hall identifier
    seats_available: int  # Total seats available for this showing
    seats_booked: int = 0  # Number of seats already booked
    duration_minutes: Optional[int] = None  # Movie duration in minutes
    genre: Optional[str] = None  # Movie genre
    rating: Optional[str] = None  # Movie rating (PG, PG-13, R, etc.)
    
    @property
    def seats_remaining(self) -> int:
        """Calculate remaining available seats"""
        return max(0, self.seats_available - self.seats_booked)
    
    @property
    def is_sold_out(self) -> bool:
        """Check if the movie showing is sold out"""
        return self.seats_remaining == 0
    
    @property
    def occupancy_percentage(self) -> float:
        """Calculate the occupancy percentage"""
        if self.seats_available == 0:
            return 0.0
        return (self.seats_booked / self.seats_available) * 100

@dataclass
class ContactInfo:
    """Contact information for a reservation"""
    name: str
    email: str
    phone: Optional[str] = None

@dataclass
class MovieReservation:
    """Represents a reservation for a movie showing"""
    movie_title: str  # Title of the movie (for easy reference)
    movie_date: date  # Date of the movie showing
    movie_time: time  # Time of the movie showing
    room: str  # Cinema room
    seats_reserved: int  # Number of seats reserved
    contact_info: ContactInfo  # Customer contact information
    reservation_datetime: datetime  # When the reservation was made
    status: str = "confirmed"  # Status: confirmed, cancelled, completed
    special_requests: Optional[str] = None  # Any special requests or notes
    
    @property
    def is_active(self) -> bool:
        """Check if the reservation is still active"""
        return self.status == "confirmed"
    
    @property
    def customer_name(self) -> str:
        """Get customer name for easy access"""
        return self.contact_info.name
    
    @property
    def customer_email(self) -> str:
        """Get customer email for easy access"""
        return self.contact_info.email
