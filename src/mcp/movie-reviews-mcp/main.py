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

mcp = FastMCP("Attractions", port=8008)

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
    limit: int = 20
) -> Dict[str, Any]:
    """Search for tourist attractions with optional filters
    
    Args:
        location: Location to search in (e.g., "Paris", "India", "Italy")
        category: Category filter - "historical", "natural", "cultural", "religious", "modern", "museums", "parks", "beaches", "mountains", "architecture", "entertainment", "adventure"
        limit: Maximum number of results (1-100, default: 20)
        
    Returns:
        AttractionsList object as dictionary with matching attractions
    """
    return search_attractions_data(location, category, limit)

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
    mcp.run(transport="streamable-http")