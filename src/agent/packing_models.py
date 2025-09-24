"""Pydantic models for the Packing List Agent and DeepseekTravels system"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum

# Enums for standardized values
class SafetyStatus(str, Enum):
    """Airport security status for items"""
    SAFE = "safe"  # Allowed in carry-on and checked
    RESTRICTED = "restricted"  # Allowed with conditions
    PROHIBITED = "prohibited"  # Not allowed in carry-on

class Priority(str, Enum):
    """Item priority for packing"""
    ESSENTIAL = "essential"  # Must-have items
    IMPORTANT = "important"  # Very useful items
    NICE_TO_HAVE = "nice-to-have"  # Optional items
    LUXURY = "luxury"  # Non-essential comfort items

class WeightClass(str, Enum):
    """Weight classification for items"""
    NEGLIGIBLE = "negligible"  # <50g
    LIGHT = "light"  # 50g-200g
    MEDIUM = "medium"  # 200g-500g  
    HEAVY = "heavy"  # 500g-1kg
    VERY_HEAVY = "very-heavy"  # >1kg

class ActivityType(str, Enum):
    """Types of activities affecting packing needs"""
    BUSINESS = "business"
    CASUAL = "casual" 
    OUTDOOR = "outdoor"
    BEACH = "beach"
    FORMAL = "formal"
    HIKING = "hiking"
    CULTURAL = "cultural"
    NIGHTLIFE = "nightlife"

class WeatherCondition(str, Enum):
    """Weather conditions affecting packing"""
    HOT = "hot"  # >25°C
    WARM = "warm"  # 15-25°C
    COOL = "cool"  # 5-15°C
    COLD = "cold"  # <5°C
    RAINY = "rainy"
    SNOWY = "snowy"
    WINDY = "windy"

# Core packing models
class PackingListItem(BaseModel):
    """Individual item in a packing list"""
    name: str
    category: str  # "clothing", "toiletries", "electronics", "documents", etc.
    quantity: int = 1
    estimated_weight_g: int = Field(..., description="Estimated weight in grams")
    estimated_volume_ml: int = Field(..., description="Estimated volume in milliliters")
    safety_status: SafetyStatus
    priority: Priority
    weight_class: WeightClass
    reason: str = Field(..., description="Why this item is recommended")
    alternatives: List[str] = Field(default_factory=list, description="Alternative items if this doesn't fit")
    restrictions: Optional[str] = None  # Security or customs restrictions
    source_rule: str = Field(..., description="Which packing rule generated this item")

class PackingConstraints(BaseModel):
    """User's packing constraints and preferences"""
    capacity_liters: Optional[int] = None
    max_weight_kg: Optional[float] = None
    airline: Optional[str] = None
    cabin_class: str = "economy"
    route_type: str = "international"  # domestic, international, regional
    has_laundry_access: bool = False
    mobility_limitations: List[str] = Field(default_factory=list)
    liquid_restrictions: bool = True  # Follow 3-1-1 rule
    budget_constraints: Optional[Dict[str, float]] = None  # category -> max_spend

class TripParameters(BaseModel):
    """Trip details affecting packing decisions"""
    destination: str
    departure_date: date
    return_date: Optional[date] = None
    trip_length_days: int
    activities: List[ActivityType] = Field(default_factory=list)
    time_of_day_activities: Dict[str, List[str]] = Field(default_factory=dict)  # "day"/"night" -> activities
    accommodation_type: str = "hotel"  # hotel, hostel, camping, airbnb
    transportation_methods: List[str] = Field(default_factory=list)  # flight, train, car, etc.

class WeatherForecast(BaseModel):
    """Weather information for the trip"""
    location: str
    conditions: List[WeatherCondition]
    temperature_range_c: Dict[str, int]  # {"min": 5, "max": 20}
    precipitation_probability: float = 0.0
    special_conditions: List[str] = Field(default_factory=list)  # "high humidity", "strong winds"

class PackingListRequest(BaseModel):
    """Complete request for generating a packing list"""
    trip_parameters: TripParameters
    constraints: PackingConstraints
    weather_forecast: Optional[WeatherForecast] = None
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
    keep_it_simple: bool = False  # Generate minimal checklist only

class PackingListResponse(BaseModel):
    """Generated packing list with analysis"""
    items: List[PackingListItem]
    total_estimated_weight_g: int
    total_estimated_volume_ml: int
    fits_constraints: bool
    constraint_violations: List[str] = Field(default_factory=list)
    category_summaries: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    alternatives_suggested: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.now)
    generation_mode: str = "full"  # "full", "simple"

# Category analysis models
class CategorySummary(BaseModel):
    """Summary of items in a category"""
    category: str
    item_count: int
    total_weight_g: int
    total_volume_ml: int
    priority_distribution: Dict[Priority, int]
    safety_status_distribution: Dict[SafetyStatus, int]

class CapacityAnalysis(BaseModel):
    """Analysis of how items fit within constraints"""
    total_capacity_used_percent: float
    total_weight_used_percent: float
    categories_over_limit: List[str] = Field(default_factory=list)
    suggested_removals: List[str] = Field(default_factory=list)
    suggested_swaps: List[Dict[str, str]] = Field(default_factory=list)  # {"remove": "item", "add": "alternative"}

# Keep-it-simple mode models
class SimplePackingItem(BaseModel):
    """Simplified item for keep-it-simple mode"""
    name: str
    quantity: int = 1
    category: str
    essential: bool = True

class SimplePackingList(BaseModel):
    """Minimal packing checklist"""
    destination: str
    trip_length_days: int
    items: List[SimplePackingItem]
    high_priority_notes: List[str] = Field(default_factory=list, max_items=5)
    generated_at: datetime = Field(default_factory=datetime.now)

# Integration models for MCP tools
class MCPToolResult(BaseModel):
    """Standardized result from MCP tool calls"""
    tool_name: str
    success: bool
    data: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None

class PackingSession(BaseModel):
    """User session for iterative packing list refinement"""
    session_id: str
    user_constraints: PackingConstraints
    trip_parameters: TripParameters
    current_list: Optional[PackingListResponse] = None
    conversation_history: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)