"""
Packing service with MCP tools and logic.
"""

from typing import Dict, Any, List, Optional
from dataclasses import asdict

from config import DEFAULT_COLD_THRESHOLD_C, PACKING_LISTS
from models import PackingList, ActivityList
from utils import (
    validate_activity, normalize_activity_name, get_activity_info,
    create_activity_info_list, format_activity_name, get_categories,
    validate_temperature_threshold
)


def get_packing_list_data(
    activity: str, 
    cold_threshold_c: int = DEFAULT_COLD_THRESHOLD_C,
    expect_rain: bool = False
) -> Dict[str, Any]:
    """Generate a packing list for a specific activity
    
    Args:
        activity: The activity type (e.g., "day_hike", "beach_trip")
        cold_threshold_c: Temperature threshold in Celsius below which cold items are added
        expect_rain: Whether to include rain items regardless of temperature
        
    Returns:
        PackingList object as dictionary or error dict
    """
    try:
        normalized_activity = normalize_activity_name(activity)
        
        if not validate_activity(normalized_activity):
            available_activities = ", ".join(PACKING_LISTS.keys())
            return {
                "error": f"Activity '{activity}' not supported. Available activities: {available_activities}"
            }
        
        if not validate_temperature_threshold(cold_threshold_c):
            return {
                "error": f"Invalid temperature threshold: {cold_threshold_c}°C. Must be between -40°C and 40°C"
            }
        
        activity_info = get_activity_info(normalized_activity)
        if not activity_info:
            return {"error": f"No packing list found for activity: {activity}"}
        
        packing_list = PackingList(
            activity=normalized_activity,
            base_items=activity_info["base_items"].copy(),
            cold_threshold_c=cold_threshold_c,
            cold_items=activity_info["cold_items"].copy(),
            rain_items=activity_info["rain_items"].copy(),
            description=activity_info.get("description")
        )
        
        return asdict(packing_list)
        
    except Exception as e:
        return {"error": f"Failed to generate packing list: {str(e)}"}


def list_activities_data(category: Optional[str] = None) -> Dict[str, Any]:
    """Get list of all supported activities with descriptions
    
    Args:
        category: Optional category filter (e.g., "outdoor", "travel", "sports")
        
    Returns:
        ActivityList object as dictionary or error dict
    """
    try:
        activities = create_activity_info_list()
        
        # Filter by category if specified
        if category:
            category_lower = category.lower()
            activities = [a for a in activities if a.category.lower() == category_lower]
            
            if not activities:
                available_categories = ", ".join(get_categories())
                return {
                    "error": f"No activities found for category '{category}'. Available categories: {available_categories}"
                }
        
        activity_list = ActivityList(
            total_count=len(activities),
            activities=activities,
            categories=get_categories()
        )
        
        return asdict(activity_list)
        
    except Exception as e:
        return {"error": f"Failed to list activities: {str(e)}"}


def get_activity_details_data(activity: str) -> Dict[str, Any]:
    """Get detailed information about a specific activity
    
    Args:
        activity: The activity name
        
    Returns:
        Detailed activity information or error dict
    """
    try:
        normalized_activity = normalize_activity_name(activity)
        
        if not validate_activity(normalized_activity):
            available_activities = ", ".join(PACKING_LISTS.keys())
            return {
                "error": f"Activity '{activity}' not supported. Available activities: {available_activities}"
            }
        
        activity_info = get_activity_info(normalized_activity)
        if not activity_info:
            return {"error": f"No information found for activity: {activity}"}
        
        # Return comprehensive activity details
        return {
            "activity": normalized_activity,
            "display_name": format_activity_name(normalized_activity),
            "description": activity_info["description"],
            "category": activity_info["category"],
            "typical_duration": activity_info.get("typical_duration"),
            "base_items_count": len(activity_info["base_items"]),
            "cold_items_count": len(activity_info["cold_items"]),
            "rain_items_count": len(activity_info["rain_items"]),
            "sample_base_items": activity_info["base_items"][:5],  # First 5 items as preview
        }
        
    except Exception as e:
        return {"error": f"Failed to get activity details: {str(e)}"}


def format_packing_list_resource(packing_list: Dict[str, Any]) -> str:
    """Format packing list as a readable resource string"""
    if "error" in packing_list:
        return f"Error: {packing_list['error']}"
    
    activity = format_activity_name(packing_list["activity"])
    
    resource = f"# Packing List for {activity}\n\n"
    
    if packing_list.get("description"):
        resource += f"**Description:** {packing_list['description']}\n\n"
    
    # Base items
    resource += "## Essential Items\n"
    for item in packing_list["base_items"]:
        resource += f"- {item}\n"
    
    # Cold weather items
    if packing_list["cold_items"]:
        threshold = packing_list["cold_threshold_c"]
        resource += f"\n## Cold Weather Items (below {threshold}°C)\n"
        for item in packing_list["cold_items"]:
            resource += f"- {item}\n"
    
    # Rain items
    if packing_list["rain_items"]:
        resource += "\n## Rain Protection Items\n"
        for item in packing_list["rain_items"]:
            resource += f"- {item}\n"
    
    return resource


def get_packing_summary_prompt() -> str:
    """Get prompt for packing list summaries"""
    return """
    You are a helpful packing assistant. When showing packing lists to users:
    
    1. Present the list in a clear, organized format
    2. Group items logically (essentials, weather-specific, etc.)
    3. Explain why certain items might be needed based on the activity
    4. Suggest customizations based on personal preferences or specific conditions
    5. Remind users to check local weather forecasts and regulations
    
    Always be encouraging and help users feel prepared for their adventure!
    """