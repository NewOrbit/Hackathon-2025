from typing import Any, Dict
from dataclasses import asdict

from models import (Menu, MenuItem)

from utils import get_menu_by_cuisine, get_menu_by_id, parse_menu_data

def get_menu_data(restaurantId: int) -> Menu | str:
    """Get menu information for a specific restaurant

    Args:
        restaurantId: The ID of the restaurant

    Returns:
        A dictionary containing the menu information or an error message
    """
    try:
        data = get_menu_by_id(restaurantId)
        if not data:
            return f"Restaurant with ID {restaurantId} not found"
        
        menu = parse_menu_data(data)
        
        return menu
        
    except Exception as e:
        return f"Failed to get menu details: {str(e)}"
    
def get_menu_items_by_cuisine(cuisine: str) -> Menu | str:
    """Get menu items by cuisine type

    Args:
        cuisine: The type of cuisine (e.g., "Italian", "Japanese")

    Returns:
        A Menu object containing items of the specified cuisine or an error message
    """
    try:
        data = get_menu_by_cuisine(cuisine)
        if not data:
            return f"No menu found for cuisine: {cuisine}"
        
        menu = parse_menu_data(data)

        return menu
    
    except Exception as e:
        return f"Failed to get menu by cuisine: {str(e)}"
    
def get_all_menus() -> Dict[str, Any]:
    """Get all menus"""
    from utils import get_all_menus
    return get_all_menus()

def get_popular_menu_items() -> Dict[str, Any]:
    """Get popular menu items across all restaurants"""
    from utils import get_popular_menu_items
    return get_popular_menu_items()

def get_vegetarian_menu_items() -> Dict[str, Any]:
    """Get vegetarian menu items across all restaurants"""
    from utils import get_vegetarian_menu_items
    return get_vegetarian_menu_items()

def get_gluten_free_menu_items() -> Dict[str, Any]:
    """Get gluten-free menu items across all restaurants"""
    from utils import get_gluten_free_menu_items
    return get_gluten_free_menu_items()

def get_menu_items_by_price_range(min_price: float, max_price: float, limit: int = 10) -> Dict[str, Any]:
    """Get menu items within a specific price range across all restaurants

    Args:
        min_price: Minimum price
        max_price: Maximum price
        limit: Maximum number of items to return

    Returns:
        A dictionary containing menu items within the price range and the total count
    """
    from utils import get_menu_items_by_price_range
    return get_menu_items_by_price_range(min_price, max_price, limit)

def get_menu_summary_prompt(restaurantId: int, include_highlight: bool, include_dietary_info: bool) -> str:
    """Generate a prompt for menu summary"""
    prompt = f"Provide a summary of the menu for a restaurant with ID {restaurantId}."
    if include_highlight:
        prompt += " Include popular dishes and their prices."
    if include_dietary_info:
        prompt += " Include dietary information for each dish."
    return prompt