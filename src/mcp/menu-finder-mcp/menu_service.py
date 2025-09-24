from typing import Any, Dict
from dataclasses import asdict

from models import (Menu, MenuItem)

from utils import get_menu_by_id, parse_menu_data

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