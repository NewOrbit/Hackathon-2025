from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

from menu_service import (
    get_menu_data,
    get_menu_summary_prompt
)

from models import Menu

# Create an MCP server
# you can add the port here so that it doesnt clash with other mcp servers
mcp = FastMCP("Menu", port=8011)

# Add an addition tool
@mcp.tool()
def get_menu(restaurantId: int) -> Menu | str:
    """Get menu information for a specific restaurant

    Args:
        restaurantId: The ID of the restaurant

    Returns:
        A dictionary containing the menu information or an error message
    """
    return get_menu_data(restaurantId)

@mcp.tool()
def get_all_menus() -> Dict[str, Any]:
    """Get all menus"""
    from menu_service import get_all_menus
    return get_all_menus()

@mcp.tool()
def get_popular_menu_items() -> Dict[str, Any]:
    """Get popular menu items across all restaurants"""
    from menu_service import get_popular_menu_items
    return get_popular_menu_items()

@mcp.tool()
def get_vegetarian_menu_items() -> Dict[str, Any]:
    """Get vegetarian menu items across all restaurants"""
    from menu_service import get_vegetarian_menu_items
    return get_vegetarian_menu_items()

@mcp.tool()
def get_gluten_free_menu_items() -> Dict[str, Any]:
    """Get gluten-free menu items across all restaurants"""
    from menu_service import get_gluten_free_menu_items
    return get_gluten_free_menu_items()

@mcp.tool()
def get_menu_items_by_price_range(min_price: float, max_price: float, limit: int = 10) -> Dict[str, Any]:
    """Get menu items within a specific price range across all restaurants"""
    from menu_service import get_menu_items_by_price_range
    return get_menu_items_by_price_range(min_price, max_price, limit)

@mcp.prompt()
def menu_summary_prompt(restaurantId: int, include_highlight: bool = False, include_dietary_info: bool = False) -> str:
    """Generate a prompt for menu summary"""
    return get_menu_summary_prompt(restaurantId, include_highlight, include_dietary_info)

    
if __name__ == "__main__":
    mcp.run("streamable-http")