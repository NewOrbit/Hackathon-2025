from typing import Any, Dict, Optional
from config import CUISINES, RESTAURANTS

def get_cuisines_data() -> str:
    """Get list of available cuisines as formatted string
    
    Returns:
        Formatted string with cuisine codes and display names
    """
    try:
        result = "**Available Cuisines**\n\n"
        result += f"Total Cuisines: {len(CUISINES)}\n\n"
        
        for code, display_name in CUISINES.items():
            result += f"• **{code}**: {display_name}\n"
        
        result += "\n*Use these cuisine codes when searching for restaurants.*"
        return result
        
    except Exception as e:
        return f"Error: Failed to get cuisines: {str(e)}"

def get_locations_data() -> str:
    """Get list of available locations as formatted string
    
    Returns:
        Formatted string with location names
    """
    try:
        locations = {restaurant["location"] for restaurant in RESTAURANTS}
        result = "**Available Locations**\n\n"
        result += f"Total Locations: {len(locations)}\n\n"
        
        for location in sorted(locations):
            result += f"• {location}\n"
        
        result += "\n*Use these locations when searching for restaurants.*"
        return result
        
    except Exception as e:
        return f"Error: Failed to get locations: {str(e)}"
    
def get_restaurant_by_id(restaurant_id: int) -> Optional[Dict[str, Any]]:
    """Get restaurant details by ID from mock data"""
    for restaurant in RESTAURANTS:
        if restaurant["id"] == restaurant_id:
            return restaurant
    return None
    
def get_restaurant_cuisine_by_id(restaurant_id: int) -> Optional[Dict[str, Any]]:
    """Get restaurant details by ID from mock data"""
    for restaurant in RESTAURANTS:
        if restaurant["id"] == restaurant_id:
            return restaurant["cuisine"]
    return None
    
def get_restaurant_menu_by_id(restaurant_id: int) -> Optional[Dict[str, Any]]:
    """Get restaurant details by ID from mock data"""
    for restaurant in RESTAURANTS:
        if restaurant["id"] == restaurant_id:
            return restaurant["menu"]
    return None

def filter_restaurants(cuisine: Optional[str], location: Optional[str], venue: Optional[str]) -> list:
    """Filter restaurants by cuisine and location from mock data
    
    Args:
        cuisine: The cuisine code to filter by (optional).
        location: The location to filter by (optional).
    
    Returns:
        A list of restaurants matching the criteria.
    """
    filtered_restaurants = []
    
    for restaurant in RESTAURANTS:
        if (cuisine is None or cuisine in restaurant["cuisine"]) and \
           (location is None or restaurant["location"] == location) and \
           (venue is None or restaurant["venues"] == venue):
            filtered_restaurants.append(restaurant)
    
    return filtered_restaurants