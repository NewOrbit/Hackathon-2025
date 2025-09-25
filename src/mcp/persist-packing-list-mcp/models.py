"""
Packing list data models - Data classes for packing list objects.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class PackingStatus(Enum):
    """Status of packing items"""
    NOT_PACKED = "not_packed"
    PACKED = "packed"
    OPTIONAL = "optional"


class ItemCategory(Enum):
    """Categories for packing items"""
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"
    TOILETRIES = "toiletries"
    DOCUMENTS = "documents"
    MEDICATIONS = "medications"
    ENTERTAINMENT = "entertainment"
    FOOD_SNACKS = "food_snacks"
    SPORTS_OUTDOOR = "sports_outdoor"
    MISCELLANEOUS = "miscellaneous"


@dataclass
class PackingItem:
    """Individual packing list item"""
    id: Optional[int] = None
    name: str = ""
    category: ItemCategory = ItemCategory.MISCELLANEOUS
    quantity: int = 1
    status: PackingStatus = PackingStatus.NOT_PACKED
    notes: Optional[str] = None
    priority: int = 1  # 1-5 scale, 5 being highest priority
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class PackingList:
    """Travel packing list"""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    destination: Optional[str] = None
    travel_start_date: Optional[datetime] = None
    travel_end_date: Optional[datetime] = None
    items: List[PackingItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def add_item(self, item: PackingItem) -> None:
        """Add an item to the packing list"""
        self.items.append(item)
    
    def remove_item(self, item_id: int) -> bool:
        """Remove an item from the packing list by ID"""
        initial_length = len(self.items)
        self.items = [item for item in self.items if item.id != item_id]
        return len(self.items) < initial_length
    
    def get_packed_count(self) -> int:
        """Get count of packed items"""
        return len([item for item in self.items if item.status == PackingStatus.PACKED])
    
    def get_total_count(self) -> int:
        """Get total count of items (excluding optional)"""
        return len([item for item in self.items if item.status != PackingStatus.OPTIONAL])
    
    def get_completion_percentage(self) -> float:
        """Get packing completion percentage"""
        total = self.get_total_count()
        if total == 0:
            return 0.0
        return (self.get_packed_count() / total) * 100


@dataclass
class PackingListSummary:
    """Summary information for a packing list"""
    id: int
    name: str
    destination: Optional[str]
    travel_start_date: Optional[datetime]
    item_count: int
    packed_count: int
    completion_percentage: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]