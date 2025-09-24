"""
Tourist Attractions MCP Package - Discover and book attractions worldwide.
"""

from attractions_service import (
    get_attraction_details_data, 
    search_attractions_data,
    get_random_attraction_data,
    get_world_wonders_data,
    book_attraction_data,
    get_attraction_categories_data
)
from models import (
    Attraction, AttractionDetails, BookingRequest, BookingResponse,
    AttractionsList, SearchFilters, Location, Coordinates
)
from utils import (
    get_attraction_by_id, search_attractions, parse_attraction_data,
    format_attraction_name, get_category_display_name, generate_booking_id,
    validate_visit_date, validate_email, format_attraction_details
)

__version__ = "1.0.0"
__all__ = [
    # Service functions
    "get_attraction_details_data",
    "search_attractions_data", 
    "get_random_attraction_data",
    "get_world_wonders_data",
    "book_attraction_data",
    "get_attraction_categories_data",
    # Models
    "Attraction",
    "AttractionDetails", 
    "BookingRequest",
    "BookingResponse",
    "AttractionsList",
    "SearchFilters",
    "Location",
    "Coordinates",
    # Utilities
    "get_attraction_by_id",
    "search_attractions",
    "parse_attraction_data",
    "format_attraction_name",
    "get_category_display_name",
    "generate_booking_id", 
    "validate_visit_date",
    "validate_email",
    "format_attraction_details"
]
