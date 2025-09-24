from typing import Any, Dict
from dataclasses import asdict

from models import (Menu, MenuItem)

from utils import parse_menu_data

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

def get_menu_summary_prompt(restaurantId: int, include_highlight: bool, include_dietary_info: bool) -> str:
    """Generate a prompt for menu summary"""
    prompt = f"Provide a summary of the menu for a restaurant with ID {restaurantId}."
    if include_highlight:
        prompt += " Include popular dishes and their prices."
    if include_dietary_info:
        prompt += " Include dietary information for each dish."
    return prompt

def get_menu_by_id(restaurantId: int) -> Dict[str, Any]:
    # Mock function to simulate fetching menu data by restaurant ID
    mock_menus = {
        1: {
            "id": 1,
            "name": "The Gourmet Kitchen",
            "location": "123 Food St, Flavor Town",
            "cuisine": "Italian",
            "menu_items": [
                {"name": "Margherita Pizza", "price": 12.99, "description": "Classic pizza with fresh tomatoes, mozzarella, and basil."},
                {"name": "Pasta Carbonara", "price": 14.99, "description": "Creamy pasta with pancetta and parmesan."}
            ],
            "reviews_count": 150,
            "facilities": ["WiFi", "Outdoor Seating"],
            "best_time_to_visit": "Evenings",
            "duration": "1-2 hours"
        },
        2: {
            "id": 2,
            "name": "Sushi World",
            "location": "456 Ocean Ave, Seaside City",
            "cuisine": "Japanese",
            "menu_items": [
                {"name": "California Roll", "price": 8.99, "description": "Crab, avocado, and cucumber roll."},
                {"name": "Spicy Tuna Roll", "price": 9.99, "description": "Tuna with spicy mayo."}
            ],
            "reviews_count": 200,
            "facilities": ["Parking", "Reservations"],
            "best_time_to_visit": "Lunch",
            "duration": "1 hour"
        }
    }
    return mock_menus.get(restaurantId, {})