"""
Restaurant Service

Handles all restaurant-related business logic and data operations.
"""

from typing import Any, Dict, List, Optional
from config import MOCK_RESTAURANTS, MOCK_MENUS


def search_restaurants(
    cuisine: Optional[str] = None,
    location: Optional[str] = None,
    average_price: Optional[float] = None,
    rating_min: Optional[float] = None,
    opens_at: Optional[int] = None,
    closes_at: Optional[int] = None
) -> List[Dict[str, Any]]:

    filtered_restaurants = MOCK_RESTAURANTS.copy()

    # Apply filters if provided
    if cuisine:
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r.get("cuisine", "").lower() == cuisine.lower()
        ]

    if location:
        filtered_restaurants = [
            r for r in filtered_restaurants
            if location.lower() in r.get("location", "").lower()
        ]

    if average_price:
        filtered_restaurants = [
            r for r in filtered_restaurants 
            if r.get("average_price", 0) <= average_price
        ]

    if rating_min:
        filtered_restaurants = [
            r for r in filtered_restaurants 
            if r.get("rating", 0) >= rating_min
        ]

    if opens_at:
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r.get("opens_at", 0) >= opens_at
        ]

    if  closes_at:
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r.get("closes_at", 23) <= closes_at
        ]

    return filtered_restaurants


def get_restaurant_by_id(restaurant_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific restaurant by ID
    
    Args:
        restaurant_id: The restaurant ID to search for
        
    Returns:
        Restaurant data if found, None otherwise
    """
    for restaurant in MOCK_RESTAURANTS:
        if restaurant.get("id") == restaurant_id:
            return restaurant
    return None


def get_restaurant_menu(restaurant_id: str) -> Optional[Dict[str, Any]]:
    """Get menu for a specific restaurant
    
    Args:
        restaurant_id: The restaurant ID to get menu for
        
    Returns:
        Menu data if restaurant found, None otherwise
    """
    # Check if restaurant exists first
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return None
    
    # Return menu from config if available
    return get_menu_items_by_restaurant(restaurant_id)


def get_menu_items_by_restaurant(restaurant_id: str) -> Dict[str, Any]:
    """Get all menu items for a specific restaurant"""
    for menu in MOCK_MENUS:
        if menu["restaurant_id"] == restaurant_id:
            return menu
    return None