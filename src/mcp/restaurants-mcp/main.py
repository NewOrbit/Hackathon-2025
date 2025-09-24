"""
Restaurant MCP Server

A Model Context Protocol (MCP) server that provides restaurant search and menu functionality.

Features:
- Search restaurants by cuisine, location, price, and rating
- Get detailed restaurant information
- Access restaurant menus with dietary information

Available Tools:
- search_restaurants: Find restaurants with optional filters
- get_restaurant_details: Get specific restaurant information
- get_menu: Retrieve restaurant menu (MCP resource)

To run this server:
    uv run mcp dev main.py

The server runs on port 8010 with streamable HTTP transport.
"""

from mcp.server.fastmcp import FastMCP

from typing import Any, Dict, List, Optional
from restaurant_service import (
    search_restaurants as search_restaurants_service,
    get_restaurant_menu,
)

mcp = FastMCP("Restaurants", port=8010)


@mcp.tool()
def search_restaurants(
    cuisine: Optional[str] = None,
    location: Optional[str] = None,
    average_price: Optional[float] = None,
    rating_min: Optional[float] = None,
    opens_at: Optional[int] = None,
    closes_at: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Search for restaurants with optional filters

    Args:
        cuisine: Filter by cuisine type (e.g. "italian", "chinese")
        location: City name or place name (e.g., "London", "New York", "Tokyo")
        average_price: Filter by maximum average price per person (e.g. 50)
        rating_min: Minimum rating filter (e.g., 4)
        opens_at: Filter by opening hours (e.g. 700)
        closes_at: Filter by closing hours (e.g. 2100)

    Returns:
        RestaurantsList object as dictionary with matching restaurants
    """
    return search_restaurants_service(
        cuisine,
        location,
        average_price,
        rating_min,
        opens_at,
        closes_at,
    )


@mcp.tool()
def get_menu(restaurant_id: str) -> Dict[str, Any]:
    """Get menu for a specific restaurant

    Args:
        restaurant_id: The ID of the restaurant to get menu for

    Returns:
        Menu data for the restaurant
    """
    menu = get_restaurant_menu(restaurant_id)
    if menu:
        return menu
    else:
        return {"error": f"Restaurant not found"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
