"""
Utility functions for the packing lists MCP server.
"""

from typing import Dict, Any, List, Optional
from config import PACKING_LISTS, ACTIVITY_CATEGORIES
from models import ActivityInfo


def get_activity_names() -> List[str]:
    """Get list of all supported activity names"""
    return list(PACKING_LISTS.keys())


def validate_activity(activity: str) -> bool:
    """Validate if an activity is supported"""
    return activity.lower() in PACKING_LISTS


def normalize_activity_name(activity: str) -> str:
    """Normalize activity name to match our keys"""
    return activity.lower().replace(" ", "_").replace("-", "_")


def get_activity_info(activity: str) -> Optional[Dict[str, Any]]:
    """Get activity information from config"""
    normalized = normalize_activity_name(activity)
    return PACKING_LISTS.get(normalized)


def create_activity_info_list() -> List[ActivityInfo]:
    """Create a list of ActivityInfo objects from config"""
    activities = []
    
    for activity_key, data in PACKING_LISTS.items():
        activity_info = ActivityInfo(
            name=activity_key,
            description=data["description"],
            category=data["category"],
            typical_duration=data.get("typical_duration")
        )
        activities.append(activity_info)
    
    return activities


def format_activity_name(activity: str) -> str:
    """Format activity name for display (convert underscores to spaces, title case)"""
    return activity.replace("_", " ").title()


def get_categories() -> List[str]:
    """Get unique list of activity categories"""
    categories = set()
    for data in PACKING_LISTS.values():
        categories.add(data["category"])
    return sorted(list(categories))


def filter_activities_by_category(category: str) -> List[str]:
    """Get activities that belong to a specific category"""
    filtered = []
    for activity_key, data in PACKING_LISTS.items():
        if data["category"].lower() == category.lower():
            filtered.append(activity_key)
    return filtered


def validate_temperature_threshold(temp: int) -> bool:
    """Validate temperature threshold is reasonable"""
    return -40 <= temp <= 40  # Reasonable range in Celsius