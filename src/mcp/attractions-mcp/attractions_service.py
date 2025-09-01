"""
Attractions service with MCP tools and API logic.
"""

from typing import Dict, Any, List
from dataclasses import asdict
from datetime import datetime

from config import DEFAULT_SEARCH_LIMIT, ATTRACTION_CATEGORIES
from models import (
    AttractionDetails, BookingRequest, BookingResponse, 
    AttractionsList, SearchFilters
)
from utils import (
    get_attraction_by_id, search_attractions, get_random_famous_attraction,
    get_random_india_attraction, get_wonders_of_world, parse_attraction_data,
    format_attraction_name, get_category_display_name, generate_booking_id,
    generate_confirmation_code, validate_visit_date, validate_email,
    calculate_estimated_cost, format_attraction_details
)


def get_attraction_details_data(attraction_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific attraction
    
    Args:
        attraction_id: Unique ID of the attraction
        
    Returns:
        AttractionDetails object as dictionary or error dict
    """
    try:
        data = get_attraction_by_id(attraction_id)
        if not data:
            return {"error": f"Attraction with ID {attraction_id} not found"}
        
        attraction = parse_attraction_data(data)
        
        attraction_details = AttractionDetails(
            attraction=attraction,
            reviews_count=data.get("reviews_count"),
            facilities=data.get("facilities", []),
            best_time_to_visit=data.get("best_time_to_visit"),
            duration=data.get("duration")
        )
        
        return asdict(attraction_details)
        
    except Exception as e:
        return {"error": f"Failed to get attraction details: {str(e)}"}


def search_attractions_data(
    location: str = None, 
    category: str = None, 
    limit: int = DEFAULT_SEARCH_LIMIT
) -> Dict[str, Any]:
    """Search for attractions with filters
    
    Args:
        location: Location to search in (e.g., "Paris", "India", "Italy")
        category: Category of attractions (e.g., "historical", "natural", "cultural")
        limit: Maximum number of results (default: 20, max: 100)
        
    Returns:
        AttractionsList object as dictionary or error dict
    """
    try:
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 1
            
        data = search_attractions(location, category, limit)
        if not data:
            return {"error": "No attractions found matching the criteria"}
        
        attractions = []
        if "attractions" in data:
            for item in data["attractions"]:
                attraction = parse_attraction_data(item)
                attractions.append(attraction)
        
        attractions_list = AttractionsList(
            category=get_category_display_name(category) if category else "All Categories",
            location=location or "Worldwide",
            total_count=data.get("total", len(attractions)),
            attractions=attractions
        )
        
        return asdict(attractions_list)
        
    except Exception as e:
        return {"error": f"Failed to search attractions: {str(e)}"}


def get_random_attraction_data(region: str = "famous") -> Dict[str, Any]:
    """Get a random attraction
    
    Args:
        region: Region type - "famous" for world famous attractions, "india" for Indian attractions
        
    Returns:
        Attraction object as dictionary or error dict
    """
    try:
        if region.lower() == "india":
            data = get_random_india_attraction()
        else:
            data = get_random_famous_attraction()
            
        if not data:
            return {"error": f"No random attraction found for region: {region}"}
        
        attraction = parse_attraction_data(data)
        return asdict(attraction)
        
    except Exception as e:
        return {"error": f"Failed to get random attraction: {str(e)}"}


def get_world_wonders_data() -> str:
    """Get list of world wonders attractions as formatted string
    
    Returns:
        Formatted string with world wonders attractions
    """
    try:
        data = get_wonders_of_world()
        if not data:
            return "Error: No world wonders found"
        
        attractions = []
        if "attractions" in data:
            for item in data["attractions"]:
                attraction = parse_attraction_data(item)
                attractions.append(attraction)
        
        result = "🌟 **Wonders of the World**\n\n"
        result += f"Total Wonders: {len(attractions)}\n\n"
        
        for i, attraction in enumerate(attractions, 1):
            location_str = f"{attraction.location.city}, {attraction.location.country}" if attraction.location.city else attraction.location.country
            
            result += f"{i}. 🏛️ **{attraction.name}**\n"
            result += f"   📍 {location_str}\n"
            result += f"   🏷️ {get_category_display_name(attraction.category)}\n"
            
            if attraction.rating:
                result += f"   ⭐ {attraction.rating}/5.0\n"
            if attraction.entry_fee:
                result += f"   💰 {attraction.entry_fee}\n"
            if attraction.description:
                result += f"   📝 {attraction.description}\n"
            
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error: Failed to get world wonders: {str(e)}"


def book_attraction_data(
    attraction_id: int,
    visitor_name: str,
    email: str,
    visit_date: str,
    num_visitors: int = 1,
    phone: str = None,
    special_requirements: str = None
) -> Dict[str, Any]:
    """Book an attraction visit
    
    Args:
        attraction_id: ID of the attraction to book
        visitor_name: Name of the primary visitor
        email: Email address for booking confirmation
        visit_date: Visit date in YYYY-MM-DD format
        num_visitors: Number of visitors (default: 1)
        phone: Optional phone number
        special_requirements: Optional special requirements
        
    Returns:
        BookingResponse object as dictionary or error dict
    """
    try:
        if not visitor_name.strip():
            return {"error": "Visitor name is required"}
        
        if not validate_email(email):
            return {"error": "Invalid email address"}
        
        if not validate_visit_date(visit_date):
            return {"error": "Visit date must be in the future and in YYYY-MM-DD format"}
        
        if num_visitors < 1 or num_visitors > 50:
            return {"error": "Number of visitors must be between 1 and 50"}
        
        # Get attraction details for cost calculation
        attraction_data = get_attraction_by_id(attraction_id)
        if not attraction_data:
            return {"error": f"Attraction with ID {attraction_id} not found"}
        
        attraction = parse_attraction_data(attraction_data)
        
        # Calculate estimated cost
        total_cost = calculate_estimated_cost(num_visitors, attraction.entry_fee)
        
        # Create booking
        booking_id = generate_booking_id()
        confirmation_code = generate_confirmation_code()
        
        booking_response = BookingResponse(
            booking_id=booking_id,
            attraction_id=attraction_id,
            visitor_name=visitor_name,
            visit_date=visit_date,
            num_visitors=num_visitors,
            total_cost=total_cost,
            booking_status="confirmed",
            confirmation_code=confirmation_code
        )
        
        return asdict(booking_response)
        
    except Exception as e:
        return {"error": f"Failed to book attraction: {str(e)}"}


def get_attraction_categories_data() -> str:
    """Get list of available attraction categories as formatted string
    
    Returns:
        Formatted string with category codes and display names
    """
    try:
        result = "🏛️ **Available Attraction Categories**\n\n"
        result += f"Total Categories: {len(ATTRACTION_CATEGORIES)}\n\n"
        
        for code, display_name in ATTRACTION_CATEGORIES.items():
            result += f"• **{code}**: {display_name}\n"
        
        result += "\n*Use these category codes when searching for attractions.*"
        return result
        
    except Exception as e:
        return f"Error: Failed to get categories: {str(e)}"


def format_attraction_resource(attraction_id: int) -> str:
    """Get attraction information as a formatted resource"""
    data = get_attraction_details_data(attraction_id)
    if "error" in data:
        return f"Error: {data['error']}"
    
    attraction_data = data['attraction']
    attraction = parse_attraction_data(attraction_data)
    
    return format_attraction_details(attraction)


def get_booking_summary_prompt(location: str, category: str = None) -> str:
    """Generate a prompt for attraction booking summary"""
    base = f"Please provide a summary of top attractions in {location}"
    if category:
        base += f" focusing on {get_category_display_name(category)} attractions"
    base += ", including booking recommendations, best times to visit, and practical travel advice."
    return base


def format_search_results(search_data: Dict[str, Any]) -> str:
    """Format search results as a readable string"""
    if "error" in search_data:
        return f"Error: {search_data['error']}"
    
    attractions = search_data.get('attractions', [])
    if not attractions:
        return "No attractions found matching your criteria."
    
    result = f"🎯 Found {search_data.get('total_count', len(attractions))} attractions"
    if search_data.get('location') != "Worldwide":
        result += f" in {search_data['location']}"
    if search_data.get('category') != "All Categories":
        result += f" ({search_data['category']})"
    result += ":\n\n"
    
    for i, attraction_data in enumerate(attractions[:10], 1):  # Show first 10
        attraction = parse_attraction_data(attraction_data)
        location_str = f"{attraction.location.city}, {attraction.location.country}" if attraction.location.city else attraction.location.country
        
        result += f"{i}. 🏛️ **{attraction.name}**\n"
        result += f"   📍 {location_str}\n"
        result += f"   🏷️ {get_category_display_name(attraction.category)}\n"
        
        if attraction.rating:
            result += f"   ⭐ {attraction.rating}/5.0\n"
        if attraction.entry_fee:
            result += f"   💰 {attraction.entry_fee}\n"
        
        result += "\n"
    
    if len(attractions) > 10:
        result += f"... and {len(attractions) - 10} more attractions\n"
    
    return result
