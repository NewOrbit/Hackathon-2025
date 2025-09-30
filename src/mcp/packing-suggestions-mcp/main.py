"""
Packing Lists MCP Server - Generate comprehensive packing lists for various activities.

To run this server:
    uv run mcp dev main.py

Generates activity-specific packing lists with weather-based recommendations.
"""

from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from packing_service import (
    get_packing_list_data,
    list_activities_data,
    get_activity_details_data,
    format_packing_list_resource,
    get_packing_summary_prompt
)

mcp = FastMCP("Packing", port=8010)

# Tools
@mcp.tool()
def get_suggested_packing_list(
    activity: str, 
    cold_threshold_c: int = 10,
    expect_rain: bool = False
) -> Dict[str, Any]:
    """Generate a comprehensive suggested packing list for a specific activity
    
    Args:
        activity: The activity type (e.g., "day_hike", "beach_trip", "business_travel")
        cold_threshold_c: Temperature threshold in Celsius below which cold items are added (default: 10°C)
        expect_rain: Whether to include rain items regardless of temperature (default: false)
        
    Returns:
        PackingList object as dictionary with activity-specific items and weather considerations
    """
    return get_packing_list_data(activity, cold_threshold_c, expect_rain)


@mcp.tool()
def list_activities(category: Optional[str] = None) -> Dict[str, Any]:
    """Get a list of all supported activities with descriptions
    
    Args:
        category: Optional category filter (e.g., "outdoor", "travel", "sports", "professional")
        
    Returns:
        ActivityList object as dictionary with supported activities and categories
    """
    return list_activities_data(category)


@mcp.tool()
def get_activity_details(activity: str) -> Dict[str, Any]:
    """Get detailed information about a specific activity
    
    Args:
        activity: The activity name to get details for
        
    Returns:
        Detailed activity information including description, category, and item counts
    """
    return get_activity_details_data(activity)


# Packing list resource and prompts
@mcp.resource("packing://activities")
def packing_activities_resource() -> str:
    """Resource providing information about all supported activities"""
    activities = list_activities_data()
    
    if "error" in activities:
        return f"Error loading activities: {activities['error']}"
    
    resource = "# Supported Packing List Activities\n\n"
    resource += f"**Total Activities:** {activities['total_count']}\n"
    resource += f"**Categories:** {', '.join(activities['categories'])}\n\n"
    
    # Group by category
    current_category = None
    for activity in activities['activities']:
        if activity['category'] != current_category:
            current_category = activity['category']
            resource += f"\n## {current_category.title()} Activities\n\n"
        
        duration = f" ({activity['typical_duration']})" if activity['typical_duration'] else ""
        resource += f"- **{activity['name'].replace('_', ' ').title()}**{duration}: {activity['description']}\n"
    
    return resource


@mcp.resource("packing://list/{activity}")
def packing_list_resource(activity: str) -> str:
    """Resource providing formatted packing list for a specific activity"""
    packing_list = get_packing_list_data(activity)
    return format_packing_list_resource(packing_list)


@mcp.prompt("packing-assistant")
def packing_assistant_prompt() -> str:
    """Prompt for acting as a knowledgeable packing assistant"""
    return get_packing_summary_prompt()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")