from typing import Any, Dict
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

@mcp.prompt()
def menu_summary_prompt(restaurantId: int, include_highlight: bool = False, include_dietary_info: bool = False) -> str:
    """Generate a prompt for menu summary"""
    return get_menu_summary_prompt(restaurantId, include_highlight, include_dietary_info)

    
if __name__ == "__main__":
    mcp.run("streamable-http")