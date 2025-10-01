"""
Tourist Attractions MCP Server - Discover and book attractions worldwide.

To run this server:
    uv run mcp dev main.py

Uses World Tourist Attractions API to provide information about tourist attractions
and booking capabilities.
"""

from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from attractions_service import (
    get_attraction_details_data,
    search_attractions_data, 
    get_random_attraction_data,
    get_world_wonders_data,
    book_attraction_data,
    get_attraction_categories_data,
    format_attraction_resource,
    get_booking_summary_prompt,
    format_search_results
)

mcp = FastMCP("Attractions")

# tools
@mcp.tool()
def get_attraction_details(attraction_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific tourist attraction
    
    Args:
        attraction_id: Unique ID of the attraction
        
    Returns:
        AttractionDetails object as dictionary with attraction info, facilities, and visiting tips
    """
    return get_attraction_details_data(attraction_id)

@mcp.tool()
def search_attractions(
    location: Optional[str] = None, 
    category: Optional[str] = None, 
    limit: int = 20,
    disability_accessible: Optional[bool] = None,
    outdoors: Optional[bool] = None,
    group_size: Optional[str] = None,
    age_recommendation: Optional[str] = None,
    age_restriction: Optional[str] = None,
    budget: Optional[str] = None,
    time_needed: Optional[str] = None,
    pet_friendly: Optional[bool] = None,
    wifi_available: Optional[bool] = None,
    photogenic: Optional[bool] = None,
    mood: Optional[str] = None,
    recommended_packing_list: Optional[str] = None
) -> Dict[str, Any]:
    """Search for tourist attractions with advanced filters
    
    Args:
        location: Location to search in (e.g., "Paris", "India", "Italy")
        category: Category filter - "historical", "natural", etc.
        limit: Maximum number of results (1-100, default: 20)
        disability_accessible: Only show accessible attractions
        outdoors: Only show outdoor/indoor attractions
        group_size: Filter by group size (e.g., "1-10")
        age_recommendation: Filter by recommended age (e.g., "All ages", "12+")
        age_restriction: Filter by age restriction (e.g., "18+ only")
        budget: Filter by budget (e.g., "Low", "Medium", "High")
        time_needed: Filter by time needed (e.g., "2-3 hours")
        pet_friendly: Only show pet-friendly attractions
        wifi_available: Only show attractions with wifi
        photogenic: Only show photogenic attractions
        mood: Filter by mood (e.g., "Romantic", "Adventurous")
        recommended_packing_list: Filter by required packing item (e.g., "Camera")
    Returns:
        AttractionsList object as dictionary with matching attractions
    """
    # Use the existing search_attractions_data, then filter results in-memory for advanced fields
    base_results = search_attractions_data(location, category, limit)
    if "attractions" not in base_results:
        return base_results
    filtered = []
    for attr in base_results["attractions"]:
        if disability_accessible is not None and attr.get("disability_accessible") != disability_accessible:
            continue
        if outdoors is not None and attr.get("outdoors") != outdoors:
            continue
        if group_size and attr.get("group_size") != group_size:
            continue
        if age_recommendation and attr.get("age_recommendation") != age_recommendation:
            continue
        if age_restriction and attr.get("age_restriction") != age_restriction:
            continue
        if budget and attr.get("budget") != budget:
            continue
        if time_needed and attr.get("time_needed") != time_needed:
            continue
        if pet_friendly is not None and attr.get("pet_friendly") != pet_friendly:
            continue
        if wifi_available is not None and attr.get("wifi_available") != wifi_available:
            continue
        if photogenic is not None and attr.get("photogenic") != photogenic:
            continue
        if mood and attr.get("mood") != mood:
            continue
        if recommended_packing_list:
            packing = attr.get("recommended_packing_list") or []
            if recommended_packing_list not in packing:
                continue
        filtered.append(attr)
    base_results["attractions"] = filtered
    base_results["total_count"] = len(filtered)
    return base_results

# Add a generic filter tool for advanced search
@mcp.tool()
def filter_attractions(
    field: str,
    value: Any,
    location: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """Filter attractions by any field and value (advanced search)"""
    base_results = search_attractions_data(location, category, limit)
    if "attractions" not in base_results:
        return base_results
    filtered = [a for a in base_results["attractions"] if a.get(field) == value]
    base_results["attractions"] = filtered
    base_results["total_count"] = len(filtered)
    return base_results

@mcp.tool()
def get_random_attraction(region: str = "famous") -> Dict[str, Any]:
    """Get a random tourist attraction for inspiration
    
    Args:
        region: Region type - "famous" for world famous attractions, "india" for Indian attractions
        
    Returns:
        Attraction object as dictionary with random attraction details
    """
    return get_random_attraction_data(region)

@mcp.tool()
def book_attraction(
    attraction_id: int,
    visitor_name: str,
    email: str,
    visit_date: str,
    num_visitors: int = 1,
    phone: Optional[str] = None,
    special_requirements: Optional[str] = None
) -> Dict[str, Any]:
    """Book a visit to a tourist attraction
    
    Args:
        attraction_id: ID of the attraction to book
        visitor_name: Name of the primary visitor
        email: Email address for booking confirmation
        visit_date: Visit date in YYYY-MM-DD format
        num_visitors: Number of visitors (1-50, default: 1)
        phone: Optional phone number
        special_requirements: Optional special requirements or requests
        
    Returns:
        BookingResponse object as dictionary with booking confirmation details
    """
    return book_attraction_data(
        attraction_id, visitor_name, email, visit_date, 
        num_visitors, phone, special_requirements
    )

@mcp.tool()
def search_and_format_attractions(
    location: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> str:
    """Search for attractions and return formatted results for easy reading
    
    Args:
        location: Location to search in (e.g., "Paris", "India", "Italy")  
        category: Category filter (e.g., "historical", "natural", "cultural")
        limit: Maximum number of results (1-20, default: 10)
        
    Returns:
        Formatted string with attraction search results
    """
    if limit > 20:
        limit = 20
    
    search_data = search_attractions_data(location, category, limit)
    return format_search_results(search_data)

# resources  
@mcp.resource("attraction://{attraction_id}")
def get_attraction_resource(attraction_id: int) -> str:
    """Get attraction information as a formatted resource"""
    return format_attraction_resource(attraction_id)

@mcp.resource("attractions://search/{location}")
def get_attractions_by_location_resource(location: str) -> str:
    """Get attractions for a location as a formatted resource"""
    search_data = search_attractions_data(location=location, limit=10)
    return format_search_results(search_data)

@mcp.resource("attractions://category/{category}")
def get_attractions_by_category_resource(category: str) -> str:
    """Get attractions by category as a formatted resource"""
    search_data = search_attractions_data(category=category, limit=10)
    return format_search_results(search_data)

@mcp.resource("attractions://category")
def get_attractions() -> str:
    """Get 10 attractions by formatted resource"""
    search_data = search_attractions_data(limit=10)
    return format_search_results(search_data)

@mcp.resource("attractions://categories")
def get_attraction_categories_resource() -> str:
    """Get list of available attraction categories as a formatted resource"""
    return get_attraction_categories_data()

@mcp.resource("attractions://wonders")
def get_world_wonders_resource() -> str:
    """Get list of the Wonders of the World attractions as a formatted resource"""
    return get_world_wonders_data()

# prompts
@mcp.prompt()
def attraction_booking_prompt(location: str, category: Optional[str] = None) -> str:
    """Generate a prompt for attraction booking assistance"""
    return get_booking_summary_prompt(location, category)

@mcp.prompt()
def travel_planning_prompt(location: str, days: int = 3) -> str:
    """Generate a prompt for travel planning with attractions"""
    return f"""Please help plan a {days}-day itinerary for {location}, including:
1. Top must-see attractions and landmarks
2. Best time to visit each attraction
3. Recommended booking strategies and timing
4. Transportation between attractions
5. Estimated costs and budgeting tips
6. Cultural considerations and local customs
7. Alternative attractions if main ones are crowded

Focus on creating a balanced mix of historical, cultural, and recreational activities suitable for different interests."""

@mcp.prompt()
def attraction_comparison_prompt(attraction_ids: str) -> str:
    """Generate a prompt for comparing multiple attractions"""
    return f"""Please provide a detailed comparison of these attractions (IDs: {attraction_ids}), including:
1. Unique features and highlights of each
2. Best times to visit and crowd levels  
3. Entry requirements and booking procedures
4. Approximate visit duration
5. Nearby attractions and activities
6. Accessibility and facilities
7. Value for money assessment
8. Personal recommendations based on different travel styles

Help decide which attractions to prioritize based on time, budget, and interests."""

if __name__ == "__main__":
    mcp.run()