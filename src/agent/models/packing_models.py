"""Shared data models for DeepseekTravels packing domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class SafetyStatus(str, Enum):
    SAFE = "safe"
    RESTRICTED = "restricted"
    PROHIBITED = "prohibited"


class Priority(str, Enum):
    MUST_HAVE = "must_have"
    NICE_TO_HAVE = "nice_to_have"


class WeightClass(str, Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class ItemCategory(str, Enum):
    CLOTHING = "clothing"
    TOILETRIES = "toiletries"
    ELECTRONICS = "electronics"
    DOCUMENTS = "documents"
    HEALTH = "health"
    ACCESSORIES = "accessories"


@dataclass
class PackingItem:
    """Representation of a single item in the packing list."""

    name: str
    quantity: int = 1
    category: ItemCategory = ItemCategory.ACCESSORIES
    safety_status: SafetyStatus = SafetyStatus.SAFE
    priority: Priority = Priority.MUST_HAVE
    weight_class: WeightClass = WeightClass.LIGHT
    estimated_volume_l: float = 0.0
    estimated_weight_kg: float = 0.0
    flags: List[str] = field(default_factory=list)
    reason: Optional[str] = None


@dataclass
class PackingContext:
    """Input context describing the traveller and trip constraints."""

    destination: str
    trip_length_days: int
    activities: List[str]
    time_of_day_usage: List[str]
    origin_city: Optional[str] = None
    start_date: Optional[str] = None
    capacity_liters: Optional[float] = None
    max_weight_kg: Optional[float] = None
    budget_total: Optional[float] = None
    budgets_by_category: Optional[dict[str, float]] = None
    nationality: Optional[str] = None
    destination_country: Optional[str] = None
    carrying_children: Optional[int] = None
    carrying_infants: Optional[int] = None
    traveling_adults: Optional[int] = None
    traveling_pets: Optional[int] = None
    airline: Optional[str] = None
    transportation_cabin_class: Optional[str] = None


__all__ = [
    "SafetyStatus",
    "Priority",
    "WeightClass",
    "ItemCategory",
    "PackingItem",
    "PackingContext",
]

