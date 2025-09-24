"""
Booking MCP Server - Mock booking service for flights, hotels, activities.

To run this server:
    uv run main.py

Phase 1: All data is mocked/offline - no external HTTP calls.
"""

from typing import Dict, Any, List, Optional
from datetime import date
from mcp.server.fastmcp import FastMCP
from models import FlightSearchRequest, HotelSearchRequest, ActivitySearchRequest
from booking_service import (
    search_flights_mock, search_hotels_mock, search_activities_mock,
    hold_booking_mock, confirm_booking_mock
)
from config import OFFLINE_MODE, USE_MOCKS

mcp = FastMCP("Booking", port=8011)

@mcp.tool()
def search_flights(
    departure_airport: str,
    arrival_airport: str, 
    departure_date: str,  # YYYY-MM-DD
    return_date: str = None,  # YYYY-MM-DD
    passengers: int = 1,
    flight_class: str = "economy"
) -> Dict[str, Any]:
    """Search for flights between airports
    
    Args:
        departure_airport: IATA airport code (e.g., "LAX", "JFK", "LHR")
        arrival_airport: IATA airport code (e.g., "NRT", "CDG", "SYD")
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Optional return date in YYYY-MM-DD format
        passengers: Number of passengers (default: 1)
        flight_class: Flight class (economy, business, first)
    
    Returns:
        Dict containing flight search results with pricing and schedules
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    departure_date_obj = date.fromisoformat(departure_date)
    return_date_obj = date.fromisoformat(return_date) if return_date else None
    
    return search_flights_mock(
        departure_airport, arrival_airport, departure_date_obj, 
        return_date_obj, passengers, flight_class
    )

@mcp.tool()
def search_hotels(
    city: str,
    country: str,
    check_in_date: str,  # YYYY-MM-DD
    check_out_date: str,  # YYYY-MM-DD
    guests: int = 1,
    rooms: int = 1
) -> Dict[str, Any]:
    """Search for hotels in a city
    
    Args:
        city: City name (e.g., "Paris", "Tokyo", "New York")
        country: Country name or code (e.g., "France", "Japan", "US")
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        guests: Number of guests (default: 1)
        rooms: Number of rooms (default: 1)
    
    Returns:
        Dict containing hotel search results with pricing and amenities
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    check_in_obj = date.fromisoformat(check_in_date)
    check_out_obj = date.fromisoformat(check_out_date)
    
    return search_hotels_mock(city, country, check_in_obj, check_out_obj, guests, rooms)

@mcp.tool()
def search_activities(
    location: str,
    activity_date: str,  # YYYY-MM-DD
    categories: List[str] = None,
    max_price_usd: float = None
) -> Dict[str, Any]:
    """Search for activities and tours in a location
    
    Args:
        location: City or location name (e.g., "Paris", "Rome", "Kyoto")
        activity_date: Activity date in YYYY-MM-DD format
        categories: Optional activity categories (e.g., ["museum", "outdoor", "food"])
        max_price_usd: Optional maximum price per person in USD
    
    Returns:
        Dict containing activity search results with descriptions and pricing
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    activity_date_obj = date.fromisoformat(activity_date)
    
    return search_activities_mock(location, activity_date_obj, categories or [], max_price_usd)

@mcp.tool()
def hold_booking(
    booking_type: str,
    item_id: str,
    passenger_details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Hold a booking for a limited time before confirmation
    
    Args:
        booking_type: Type of booking ("flight", "hotel", "activity")
        item_id: ID of the item to book (from search results)
        passenger_details: Optional passenger/guest details
    
    Returns:
        Dict containing hold details, expiration time, and hold ID for confirmation
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    return hold_booking_mock(booking_type, item_id, passenger_details or {})

@mcp.tool()
def confirm_booking(
    hold_id: str,
    payment_info: Dict[str, str]
) -> Dict[str, Any]:
    """Confirm a held booking with payment information
    
    Args:
        hold_id: Hold ID from hold_booking call
        payment_info: Payment details (mock data for Phase 1)
    
    Returns:
        Dict containing booking confirmation details and confirmation number
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    return confirm_booking_mock(hold_id, payment_info)

if __name__ == "__main__":
    import uvicorn
    print("🎫 Starting Booking MCP Server on http://localhost:8011/mcp/")
    print("⚠️  Phase 1: Running in OFFLINE/MOCK mode only")
    print("⚠️  NO REAL BOOKINGS WILL BE MADE - ALL MOCK DATA")
    uvicorn.run("main:mcp.app", host="127.0.0.1", port=8011, reload=True)