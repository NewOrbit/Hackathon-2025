from typing import Any, Dict
from models import Menu, MenuItem

from config import MOCK_MENUS

def parse_menu_data(data: Dict[str, Any]) -> Menu:
    """Parse menu data from API response"""
    return Menu(
        id=data.get("id", 0),
        name=data.get("name", ""),
        cuisine=data.get("cuisine", ""),
        location=data.get("location", ""),
        items=[MenuItem(**item) for item in data.get("menu_items", [])]
    )

def get_menu_by_id(restaurantId: int) -> Dict[str, Any] | None:
    """Mock function to simulate fetching menu data by restaurant ID"""
    for menu in MOCK_MENUS:
        if menu["id"] == restaurantId:
            return menu
    return None