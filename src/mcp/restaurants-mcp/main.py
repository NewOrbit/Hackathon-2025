"""
Restaurant MCP Server

To run this server:
    uv run mcp dev main.py
"""

from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Restaurants", port=8010)

@mcp.tool()
def search_restaurants(filters: str) -> str:
    return ""

@mcp.resource("restaurant://{restaurant_id}")
def get_menu(restaurant_id : int) -> Dict[str, Any]:
    return 

if __name__ == "__main__":
    mcp.run(transport="streamable-http")