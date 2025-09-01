"""
Utility functions for tourist attractions operations.
"""

import requests
import random
import string
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from config import ATTRACTIONS_BASE_URL, ENDPOINTS, ATTRACTION_CATEGORIES, MOCK_ATTRACTIONS, WORLD_WONDERS
from models import Coordinates, Location, Attraction


def make_api_request(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make an API request with error handling"""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def get_attraction_by_id(attraction_id: int) -> Optional[Dict[str, Any]]:
    """Get attraction details by ID from mock data"""
    for attraction in MOCK_ATTRACTIONS:
        if attraction["id"] == attraction_id:
            return attraction
    return None


def search_attractions(
    location: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
) -> Optional[Dict[str, Any]]:
    """Search for attractions with filters using mock data"""
    filtered_attractions = []
    
    for attraction in MOCK_ATTRACTIONS:
        # Filter by location (check city, country, or region)
        location_match = True
        if location:
            location_lower = location.lower()
            attr_location = attraction["location"]
            location_match = (
                location_lower in attr_location.get("city", "").lower() or
                location_lower in attr_location.get("country", "").lower() or
                location_lower in attr_location.get("region", "").lower()
            )
        
        # Filter by category
        category_match = True
        if category:
            category_match = attraction["category"] == category.lower()
            
        if location_match and category_match:
            filtered_attractions.append(attraction)
    
    # Apply limit
    filtered_attractions = filtered_attractions[:limit]
    
    return {
        "attractions": filtered_attractions,
        "total": len(filtered_attractions)
    }


def get_random_famous_attraction() -> Optional[Dict[str, Any]]:
    """Get a random famous attraction from mock data"""
    if MOCK_ATTRACTIONS:
        return random.choice(MOCK_ATTRACTIONS)
    return None


def get_random_india_attraction() -> Optional[Dict[str, Any]]:
    """Get a random tourist attraction in India from mock data"""
    indian_attractions = [attr for attr in MOCK_ATTRACTIONS if attr["location"]["country"] == "India"]
    if indian_attractions:
        return random.choice(indian_attractions)
    return None


def get_wonders_of_world() -> Optional[Dict[str, Any]]:
    """Get wonders of the world attractions from mock data"""
    wonders = [attr for attr in MOCK_ATTRACTIONS if attr["id"] in WORLD_WONDERS]
    return {
        "attractions": wonders,
        "total": len(wonders)
    }


def parse_coordinates(lat: float, lon: float) -> Coordinates:
    """Create coordinates object from lat/lon"""
    return Coordinates(lat=lat, lon=lon)


def parse_location_data(data: Dict[str, Any]) -> Location:
    """Parse location data from API response"""
    coords = None
    if data.get("latitude") and data.get("longitude"):
        coords = parse_coordinates(data["latitude"], data["longitude"])
    
    return Location(
        city=data.get("city", ""),
        country=data.get("country", ""),
        region=data.get("region", ""),
        coordinates=coords
    )


def parse_attraction_data(data: Dict[str, Any]) -> Attraction:
    """Parse attraction data from API response"""
    location = parse_location_data(data.get("location", {}))
    
    return Attraction(
        id=data.get("id", 0),
        name=data.get("name", ""),
        description=data.get("description", ""),
        category=data.get("category", ""),
        location=location,
        rating=data.get("rating"),
        image_url=data.get("image_url"),
        website=data.get("website"),
        opening_hours=data.get("opening_hours"),
        entry_fee=data.get("entry_fee")
    )


def format_attraction_name(attraction: Attraction) -> str:
    """Format attraction name with location"""
    name = attraction.name
    if attraction.location.city:
        name += f", {attraction.location.city}"
    if attraction.location.country:
        name += f", {attraction.location.country}"
    return name


def get_category_display_name(category: str) -> str:
    """Get display name for category"""
    return ATTRACTION_CATEGORIES.get(category.lower(), category.title())


def generate_booking_id() -> str:
    """Generate a unique booking ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ATT-{timestamp}-{random_part}"


def generate_confirmation_code() -> str:
    """Generate a confirmation code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def validate_visit_date(date_str: str) -> bool:
    """Validate that visit date is in the future"""
    try:
        visit_date = datetime.strptime(date_str, "%Y-%m-%d")
        return visit_date.date() > datetime.now().date()
    except ValueError:
        return False


def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]


def calculate_estimated_cost(num_visitors: int, entry_fee: Optional[str] = None) -> Optional[float]:
    """Calculate estimated cost based on number of visitors"""
    if not entry_fee or "free" in entry_fee.lower():
        return 0.0
    
    # Simple cost calculation - in reality this would be more complex
    try:
        # Extract number from entry fee string (e.g., "$15", "₹500")
        import re
        numbers = re.findall(r'\d+\.?\d*', entry_fee)
        if numbers:
            base_cost = float(numbers[0])
            return base_cost * num_visitors
    except (ValueError, IndexError):
        pass
    
    return None


def format_attraction_details(attraction: Attraction) -> str:
    """Format attraction details as a readable string"""
    location_str = f"{attraction.location.city}, {attraction.location.country}" if attraction.location.city else attraction.location.country
    
    details = f"🏛️ {attraction.name}\n"
    details += f"📍 Location: {location_str}\n"
    details += f"🏷️ Category: {get_category_display_name(attraction.category)}\n"
    
    if attraction.rating:
        details += f"⭐ Rating: {attraction.rating}/5.0\n"
    
    if attraction.opening_hours:
        details += f"🕒 Hours: {attraction.opening_hours}\n"
        
    if attraction.entry_fee:
        details += f"💰 Entry Fee: {attraction.entry_fee}\n"
    
    if attraction.description:
        details += f"\n📝 Description: {attraction.description}\n"
        
    if attraction.website:
        details += f"🌐 Website: {attraction.website}\n"
    
    return details
