from typing import Any, Dict
from models import Menu, MenuItem

def parse_menu_data(data: Dict[str, Any]) -> Menu:
    """Parse menu data from API response"""
    return Menu(
        id=data.get("id", 0),
        name=data.get("name", ""),
        items=[MenuItem(**item) for item in data.get("menu_items", [])]
    )