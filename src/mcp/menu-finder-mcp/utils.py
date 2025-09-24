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

def get_menu_by_cuisine(cuisine: str) -> Dict[str, Any] | None:
    """Mock function to simulate fetching menu data by cuisine type"""
    for menu in MOCK_MENUS:
        if cuisine.lower() in menu["cuisine"].lower():
            return menu
    return None

def get_all_menus() -> Dict[str, Any]:
    """Mock function to return all menus"""
    return {"menus": MOCK_MENUS, "total": len(MOCK_MENUS)}

def get_popular_menu_items() -> Dict[str, Any]:
    """Mock function to return popular menu items across all restaurants"""
    popular_items = []
    for menu in MOCK_MENUS:
        for item in menu.get("menu_items", []):
            if item.get("is_popular"):
                popular_items.append(item)
    return {"popular_items": popular_items, "total": len(popular_items)}

def get_vegetarian_menu_items() -> Dict[str, Any]:
    """Mock function to return vegetarian menu items across all restaurants"""
    veg_items = []
    for menu in MOCK_MENUS:
        for item in menu.get("menu_items", []):
            if item.get("dietary_info") and "vegetarian" in item["dietary_info"]:
                veg_items.append(item)
    return {"vegetarian_items": veg_items, "total": len(veg_items)}

def get_gluten_free_menu_items() -> Dict[str, Any]:
    """Mock function to return gluten-free menu items across all restaurants"""
    gf_items = []
    for menu in MOCK_MENUS:
        for item in menu.get("menu_items", []):
            if item.get("dietary_info") and "gluten-free" in item["dietary_info"]:
                gf_items.append(item)
    return {"gluten_free_items": gf_items, "total": len(gf_items)}

def get_menu_items_by_price_range(min_price: float, max_price: float, limit: int = 10) -> Dict[str, Any]:
    """Get menu items within a specific price range across all restaurants

    Args:
        min_price: Minimum price
        max_price: Maximum price
        limit: Maximum number of items to return

    Returns:
        A dictionary containing menu items within the price range and the total count
    """
    filtered_items = []
    
    for menu in MOCK_MENUS:
        for item in menu.get("menu_items", []):
            if min_price <= item.get("price", 0) <= max_price:
                filtered_items.append(item)
    
    # Sort by price ascending
    filtered_items.sort(key=lambda x: x.get("price", 0))
    
    # Limit results
    filtered_items = filtered_items[:limit]
    
    return {
        "items": filtered_items,
        "total": len(filtered_items)
    }