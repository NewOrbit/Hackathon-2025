"""
Utility functions for the persist-packing-list MCP server.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from config import STORAGE_PATH
from models import PackingList, PackingItem, PackingStatus, ItemCategory, PackingListSummary

def datetime_to_str(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to string for database storage"""
    if dt is None:
        return None
    return dt.isoformat()


def str_to_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """Convert string from database to datetime"""
    if dt_str is None:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None


def format_packing_list_response(packing_list: PackingList) -> Dict[str, Any]:
    """Format a packing list for API response"""
    return {
        "id": packing_list.id,
        "name": packing_list.name,
        "description": packing_list.description,
        "destination": packing_list.destination,
        "travel_start_date": datetime_to_str(packing_list.travel_start_date),
        "travel_end_date": datetime_to_str(packing_list.travel_end_date),
        "items": [format_packing_item_response(item) for item in packing_list.items],
        "total_items": len(packing_list.items),
        "packed_items": packing_list.get_packed_count(),
        "completion_percentage": round(packing_list.get_completion_percentage(), 2),
        "created_at": datetime_to_str(packing_list.created_at),
        "updated_at": datetime_to_str(packing_list.updated_at)
    }


def format_packing_item_response(item: PackingItem) -> Dict[str, Any]:
    """Format a packing item for API response"""
    return {
        "id": item.id,
        "name": item.name,
        "category": item.category.value if item.category else ItemCategory.MISCELLANEOUS.value,
        "quantity": item.quantity,
        "status": item.status.value if item.status else PackingStatus.NOT_PACKED.value,
        "notes": item.notes,
        "priority": item.priority,
        "created_at": datetime_to_str(item.created_at),
        "updated_at": datetime_to_str(item.updated_at)
    }


def format_list_summary_response(summary: PackingListSummary) -> Dict[str, Any]:
    """Format a packing list summary for API response"""
    return {
        "id": summary.id,
        "name": summary.name,
        "destination": summary.destination,
        "travel_start_date": datetime_to_str(summary.travel_start_date),
        "item_count": summary.item_count,
        "packed_count": summary.packed_count,
        "completion_percentage": round(summary.completion_percentage, 2),
        "created_at": datetime_to_str(summary.created_at),
        "updated_at": datetime_to_str(summary.updated_at)
    }


def validate_item_category(category: str) -> ItemCategory:
    """Validate and convert string to ItemCategory enum"""
    try:
        return ItemCategory(category.lower())
    except ValueError:
        return ItemCategory.MISCELLANEOUS


def validate_packing_status(status: str) -> PackingStatus:
    """Validate and convert string to PackingStatus enum"""
    try:
        return PackingStatus(status.lower())
    except ValueError:
        return PackingStatus.NOT_PACKED