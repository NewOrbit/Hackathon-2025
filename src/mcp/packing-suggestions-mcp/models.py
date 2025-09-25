"""
Packing lists data models - Data classes for packing list objects.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PackingList:
    """Comprehensive packing list for an activity"""
    activity: str
    base_items: List[str]
    cold_threshold_c: int
    cold_items: List[str]
    rain_items: List[str]
    description: Optional[str] = None


@dataclass
class ActivityInfo:
    """Information about a supported activity"""
    name: str
    description: str
    category: str
    typical_duration: Optional[str] = None


@dataclass
class ActivityList:
    """List of supported activities"""
    total_count: int
    activities: List[ActivityInfo]
    categories: List[str]