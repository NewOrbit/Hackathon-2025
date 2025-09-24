from typing import Any, Optional
from mcp.server.fastmcp import FastMCP

from restaurants_service import get_cuisines_data, get_restaurant_by_id, get_restaurant_menu_by_id, get_restaurant_cuisine_by_id, filter_restaurants, get_locations_data

# Create an MCP server
# you can add the port here so that it doesnt clash with other mcp servers
mcp = FastMCP("myname")


#tools

@mcp.tool()
def search_restaurants(cuisine: Optional[str] = None, location: Optional[str] = None, venue: Optional[str] = None) -> Any:
    """searches for restaurant based on cuisine or location"""
    return filter_restaurants(cuisine, location, venue)

@mcp.tool()
def get_restaurant_data(restaurant_id: str) -> Any:
    """gets data of restaurant by its id"""
    return get_restaurant_by_id(restaurant_id)

@mcp.tool()
def get_menu(restaurant_id) -> Any:
    """gets menu of restaurant by its id"""
    return get_restaurant_menu_by_id(restaurant_id)

@mcp.tool()
def get_cuisines(restaurant_id) -> Any:
    """get all possible cuisines"""
    return get_restaurant_cuisine_by_id(restaurant_id)

@mcp.tool()
def get_restaurant_cuisines() -> Any:
    """Gets all available cuisines in restaurants"""
    return get_cuisines_data()

@mcp.tool()
def get_restaurant_locations() -> Any:
    """Gets all available locations of restaurants"""
    return get_locations_data()


# resources

@mcp.resource("restaurants://cuisines")
def get_cuisines_resource() -> str:
    """Get list of available cuisines as a formatted resource"""
    return get_cuisines_data()

@mcp.resource("restaurants://locations")
def get_locations_resource() -> str:
    """Get list of available locations as a formatted resource"""
    return get_locations_data()

    
if __name__ == "__main__":
   mcp.run("streamable-http")