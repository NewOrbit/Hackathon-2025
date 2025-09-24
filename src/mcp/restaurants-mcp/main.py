"""
Restaurant MCP Server

To run this server:
    uv run mcp dev main.py
"""

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from config import MOCK_RESTAURANTS

mcp = FastMCP("Restaurants", port=8010)

@mcp.tool()
def search_restaurants() -> List[Dict[str, Any]]:
    """Search for restaurants with optional filters
        
    Returns:
        RestaurantsList object as dictionary with matching restaurants
    """
    return MOCK_RESTAURANTS

@mcp.resource("restaurant://{restaurant_id}")
def get_menu(restaurant_id : int) -> Dict[str, Any]:
    return 

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

