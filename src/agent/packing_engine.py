"""
Packing Engine - Core logic for generating travel packing lists

This module contains the main algorithms and rules for:
- Trip length scaling 
- Weather adaptation
- Activity-based items
- Transport constraints  
- Capacity/weight fitting
"""

import math
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from packing_models import (
    PackingListItem, PackingListRequest, PackingListResponse, TripParameters,
    PackingConstraints, WeatherForecast, SafetyStatus, Priority, WeightClass,
    ActivityType, WeatherCondition, CategorySummary, CapacityAnalysis
)

class PackingEngine:
    """Core packing list generation engine"""
    
    def __init__(self):
        self.base_items = self._load_base_items()
        self.activity_items = self._load_activity_items()
        self.weather_items = self._load_weather_items()
        
    def generate_packing_list(self, request: PackingListRequest) -> PackingListResponse:
        """Generate a complete packing list based on request parameters"""
        
        # Step 1: Generate base items with trip length scaling
        items = self._generate_base_items(request.trip_parameters, request.constraints)
        
        # Step 2: Add weather-specific items
        if request.weather_forecast:
            weather_items = self._generate_weather_items(request.weather_forecast, request.trip_parameters)
            items.extend(weather_items)
        
        # Step 3: Add activity-specific items
        activity_items = self._generate_activity_items(request.trip_parameters)
        items.extend(activity_items)
        
        # Step 4: Apply transport constraints and security restrictions
        items = self._apply_transport_constraints(items, request.constraints)
        
        # Step 5: Fit within capacity and weight constraints
        items, violations = self._fit_constraints(items, request.constraints)
        
        # Step 6: Calculate totals and analysis
        total_weight = sum(item.estimated_weight_g for item in items)
        total_volume = sum(item.estimated_volume_ml for item in items)
        
        # Step 7: Generate category summaries
        category_summaries = self._generate_category_summaries(items)
        
        return PackingListResponse(
            items=items,
            total_estimated_weight_g=total_weight,
            total_estimated_volume_ml=total_volume,
            fits_constraints=len(violations) == 0,
            constraint_violations=violations,
            category_summaries=category_summaries,
            generation_mode="full"
        )
    
    def _generate_base_items(self, trip: TripParameters, constraints: PackingConstraints) -> List[PackingListItem]:
        """Generate base items with trip length scaling"""
        items = []
        
        # Clothing items with trip length scaling
        clothing_items = [
            ("underwear", 30, 10, "essential daily item", Priority.ESSENTIAL),
            ("socks", 25, 15, "essential daily item", Priority.ESSENTIAL), 
            ("t-shirt", 150, 200, "basic clothing", Priority.ESSENTIAL),
            ("pants/jeans", 400, 800, "basic clothing", Priority.ESSENTIAL),
            ("sweater/hoodie", 300, 600, "layering piece", Priority.IMPORTANT),
            ("sleepwear", 100, 150, "comfort item", Priority.IMPORTANT),
        ]
        
        for name, weight_g, volume_ml, reason, priority in clothing_items:
            # Scale quantity based on trip length and laundry access
            if name in ["underwear", "socks"]:
                # Daily items - scale with laundry access
                base_qty = min(trip.trip_length_days, 7) if constraints.has_laundry_access else trip.trip_length_days
                quantity = max(3, min(base_qty, 10))  # At least 3, max 10
            elif name in ["t-shirt"]:
                # Scale shirts with diminishing returns
                quantity = max(2, math.ceil(trip.trip_length_days / 3)) if constraints.has_laundry_access else math.ceil(trip.trip_length_days / 2)
                quantity = min(quantity, 6)
            else:
                # Other clothing - minimal scaling
                quantity = 1 if trip.trip_length_days <= 3 else 2
                
            items.append(PackingListItem(
                name=name,
                category="clothing",
                quantity=quantity,
                estimated_weight_g=weight_g * quantity,
                estimated_volume_ml=volume_ml * quantity,
                safety_status=SafetyStatus.SAFE,
                priority=priority,
                weight_class=self._calculate_weight_class(weight_g * quantity),
                reason=f"{reason} (quantity for {trip.trip_length_days} days)",
                source_rule="base_clothing_with_trip_scaling"
            ))
        
        # Essential non-clothing items
        essential_items = [
            ("passport", 50, 20, "required travel document", "documents", Priority.ESSENTIAL),
            ("phone", 150, 100, "essential communication", "electronics", Priority.ESSENTIAL),
            ("phone charger", 100, 80, "essential for phone", "electronics", Priority.ESSENTIAL),
            ("toothbrush", 20, 30, "basic hygiene", "toiletries", Priority.ESSENTIAL),
            ("toothpaste", 100, 75, "basic hygiene", "toiletries", Priority.ESSENTIAL),
            ("medications", 50, 50, "health maintenance", "health", Priority.ESSENTIAL),
        ]
        
        for name, weight_g, volume_ml, reason, category, priority in essential_items:
            items.append(PackingListItem(
                name=name,
                category=category,
                quantity=1,
                estimated_weight_g=weight_g,
                estimated_volume_ml=volume_ml,
                safety_status=SafetyStatus.SAFE,
                priority=priority,
                weight_class=self._calculate_weight_class(weight_g),
                reason=reason,
                source_rule="base_essentials"
            ))
        
        return items
    
    def _generate_weather_items(self, weather: WeatherForecast, trip: TripParameters) -> List[PackingListItem]:
        """Generate weather-specific items"""
        items = []
        
        # Temperature-based items
        temp_min = weather.temperature_range_c.get("min", 15)
        temp_max = weather.temperature_range_c.get("max", 25)
        
        if temp_max > 25:  # Hot weather
            hot_items = [
                ("sunglasses", 50, 100, "UV protection in hot weather", Priority.IMPORTANT),
                ("sunscreen", 100, 75, "essential UV protection", Priority.ESSENTIAL),
                ("hat/cap", 80, 200, "sun protection", Priority.IMPORTANT),
                ("shorts", 120, 150, "comfortable in heat", Priority.IMPORTANT),
            ]
            for name, weight_g, volume_ml, reason, priority in hot_items:
                items.append(PackingListItem(
                    name=name, category="weather_gear", quantity=1,
                    estimated_weight_g=weight_g, estimated_volume_ml=volume_ml,
                    safety_status=SafetyStatus.SAFE, priority=priority,
                    weight_class=self._calculate_weight_class(weight_g),
                    reason=reason, source_rule="hot_weather_adaptation"
                ))
        
        if temp_min < 10:  # Cold weather  
            cold_items = [
                ("warm jacket", 600, 1200, "essential warmth in cold", Priority.ESSENTIAL),
                ("gloves", 50, 100, "hand protection from cold", Priority.IMPORTANT),
                ("warm hat/beanie", 40, 80, "head warmth", Priority.IMPORTANT),
                ("scarf", 100, 150, "neck warmth", Priority.IMPORTANT),
            ]
            for name, weight_g, volume_ml, reason, priority in cold_items:
                items.append(PackingListItem(
                    name=name, category="weather_gear", quantity=1,
                    estimated_weight_g=weight_g, estimated_volume_ml=volume_ml,
                    safety_status=SafetyStatus.SAFE, priority=priority,
                    weight_class=self._calculate_weight_class(weight_g),
                    reason=reason, source_rule="cold_weather_adaptation"
                ))
        
        # Precipitation items
        if weather.precipitation_probability > 0.3 or WeatherCondition.RAINY in weather.conditions:
            rain_items = [
                ("rain jacket/poncho", 200, 300, "protection from rain", Priority.IMPORTANT),
                ("umbrella", 300, 400, "rain protection", Priority.IMPORTANT),
            ]
            for name, weight_g, volume_ml, reason, priority in rain_items:
                items.append(PackingListItem(
                    name=name, category="weather_gear", quantity=1,
                    estimated_weight_g=weight_g, estimated_volume_ml=volume_ml,
                    safety_status=SafetyStatus.SAFE, priority=priority,
                    weight_class=self._calculate_weight_class(weight_g),
                    reason=reason, source_rule="rain_weather_adaptation"
                ))
        
        return items
    
    def _generate_activity_items(self, trip: TripParameters) -> List[PackingListItem]:
        """Generate activity-specific items"""
        items = []
        
        for activity in trip.activities:
            activity_items = self.activity_items.get(activity, [])
            
            for name, weight_g, volume_ml, reason, category, priority in activity_items:
                items.append(PackingListItem(
                    name=name, category=category, quantity=1,
                    estimated_weight_g=weight_g, estimated_volume_ml=volume_ml,
                    safety_status=SafetyStatus.SAFE, priority=Priority(priority),
                    weight_class=self._calculate_weight_class(weight_g),
                    reason=f"{reason} (for {activity.value} activities)",
                    source_rule=f"activity_{activity.value}"
                ))
        
        # Time-of-day specific items
        if "night" in trip.time_of_day_activities:
            night_items = [
                ("flashlight/headlamp", 100, 80, "visibility in dark", "accessories", Priority.IMPORTANT),
                ("evening wear", 200, 400, "appropriate night attire", "clothing", Priority.NICE_TO_HAVE),
            ]
            for name, weight_g, volume_ml, reason, category, priority in night_items:
                items.append(PackingListItem(
                    name=name, category=category, quantity=1,
                    estimated_weight_g=weight_g, estimated_volume_ml=volume_ml,
                    safety_status=SafetyStatus.SAFE, priority=Priority(priority),
                    weight_class=self._calculate_weight_class(weight_g),
                    reason=reason, source_rule="night_time_activities"
                ))
        
        return items
    
    def _apply_transport_constraints(self, items: List[PackingListItem], constraints: PackingConstraints) -> List[PackingListItem]:
        """Apply airline and transport-specific constraints"""
        modified_items = []
        
        for item in items:
            # Apply liquid restrictions (3-1-1 rule)
            if constraints.liquid_restrictions and item.category == "toiletries" and "liquid" in item.name.lower():
                # Replace large liquids with travel sizes
                if item.estimated_volume_ml > 100:
                    item.name = f"travel-size {item.name}"
                    item.estimated_volume_ml = min(100, item.estimated_volume_ml)
                    item.estimated_weight_g = int(item.estimated_weight_g * 0.6)  # Travel size is lighter
                    item.reason += " (travel-size for liquid restrictions)"
                    item.restrictions = "Must fit in 3-1-1 liquid bag"
            
            # Check for potentially restricted items
            restricted_keywords = ["knife", "blade", "battery", "lighter", "scissors"]
            if any(keyword in item.name.lower() for keyword in restricted_keywords):
                item.safety_status = SafetyStatus.RESTRICTED
                item.restrictions = "Check airline/TSA restrictions before packing"
            
            modified_items.append(item)
        
        return modified_items
    
    def _fit_constraints(self, items: List[PackingListItem], constraints: PackingConstraints) -> Tuple[List[PackingListItem], List[str]]:
        """Fit items within capacity and weight constraints using greedy + knapsack approach"""
        violations = []
        
        # If no constraints, return all items
        if not constraints.capacity_liters and not constraints.max_weight_kg:
            return items, violations
        
        # Convert capacity to ml for comparison
        capacity_ml = constraints.capacity_liters * 1000 if constraints.capacity_liters else float('inf')
        max_weight_g = constraints.max_weight_kg * 1000 if constraints.max_weight_kg else float('inf')
        
        # Calculate current totals
        total_volume = sum(item.estimated_volume_ml for item in items)
        total_weight = sum(item.estimated_weight_g for item in items)
        
        # Check if we exceed constraints
        exceeds_volume = total_volume > capacity_ml
        exceeds_weight = total_weight > max_weight_g
        
        if not exceeds_volume and not exceeds_weight:
            return items, violations  # All items fit
        
        # Need to remove items - use value-based greedy approach
        # Sort by value/volume ratio (priority score / volume)
        priority_scores = {
            Priority.ESSENTIAL: 100,
            Priority.IMPORTANT: 70,
            Priority.NICE_TO_HAVE: 40,
            Priority.LUXURY: 10
        }
        
        # Calculate value density for each item
        valued_items = []
        for item in items:
            priority_score = priority_scores[item.priority]
            volume_penalty = item.estimated_volume_ml
            weight_penalty = item.estimated_weight_g * 0.001  # Convert to lighter penalty
            
            # Higher priority and lower volume/weight = higher value density
            value_density = priority_score / (volume_penalty + weight_penalty)
            valued_items.append((item, value_density))
        
        # Sort by value density (highest first)
        valued_items.sort(key=lambda x: x[1], reverse=True)
        
        # Greedy selection within constraints
        selected_items = []
        running_volume = 0
        running_weight = 0
        
        for item, value_density in valued_items:
            new_volume = running_volume + item.estimated_volume_ml
            new_weight = running_weight + item.estimated_weight_g
            
            # Include item if it fits within constraints
            if new_volume <= capacity_ml and new_weight <= max_weight_g:
                selected_items.append(item)
                running_volume = new_volume
                running_weight = new_weight
            else:
                # Record what was removed and why
                violated_constraint = []
                if new_volume > capacity_ml:
                    violated_constraint.append(f"volume limit ({capacity_ml/1000:.1f}L)")
                if new_weight > max_weight_g:
                    violated_constraint.append(f"weight limit ({max_weight_g/1000:.1f}kg)")
                
                violations.append(f"Removed '{item.name}' - exceeds {', '.join(violated_constraint)}")
        
        return selected_items, violations
    
    def _generate_category_summaries(self, items: List[PackingListItem]) -> Dict[str, Dict[str, Any]]:
        """Generate summary statistics by category"""
        categories = {}
        
        for item in items:
            if item.category not in categories:
                categories[item.category] = {
                    "item_count": 0,
                    "total_weight_g": 0,
                    "total_volume_ml": 0,
                    "priorities": {},
                    "safety_statuses": {}
                }
            
            cat = categories[item.category]
            cat["item_count"] += 1
            cat["total_weight_g"] += item.estimated_weight_g
            cat["total_volume_ml"] += item.estimated_volume_ml
            
            # Track priority distribution
            priority_str = item.priority.value
            cat["priorities"][priority_str] = cat["priorities"].get(priority_str, 0) + 1
            
            # Track safety status distribution
            safety_str = item.safety_status.value
            cat["safety_statuses"][safety_str] = cat["safety_statuses"].get(safety_str, 0) + 1
        
        return categories
    
    def _calculate_weight_class(self, weight_g: int) -> WeightClass:
        """Calculate weight class based on weight in grams"""
        if weight_g < 50:
            return WeightClass.NEGLIGIBLE
        elif weight_g < 200:
            return WeightClass.LIGHT
        elif weight_g < 500:
            return WeightClass.MEDIUM
        elif weight_g < 1000:
            return WeightClass.HEAVY
        else:
            return WeightClass.VERY_HEAVY
    
    def _load_base_items(self) -> Dict[str, Any]:
        """Load base item database - in a real system this might come from a file/DB"""
        return {}  # Defined inline in generation methods for now
    
    def _load_activity_items(self) -> Dict[ActivityType, List[Tuple]]:
        """Load activity-specific items database"""
        return {
            ActivityType.BUSINESS: [
                ("business suit", 800, 1500, "professional appearance", "clothing", "important"),
                ("dress shoes", 600, 800, "professional footwear", "clothing", "important"),
                ("laptop", 1500, 2000, "work requirements", "electronics", "essential"),
                ("business cards", 20, 10, "networking", "accessories", "important"),
            ],
            ActivityType.HIKING: [
                ("hiking boots", 800, 1200, "foot protection and grip", "clothing", "essential"),
                ("hiking backpack", 1200, 2500, "gear transport", "accessories", "essential"),
                ("water bottle", 200, 500, "hydration during hikes", "accessories", "essential"),
                ("first aid kit", 300, 400, "emergency medical care", "health", "important"),
            ],
            ActivityType.BEACH: [
                ("swimwear", 100, 150, "beach activities", "clothing", "essential"),
                ("beach towel", 400, 800, "drying and comfort", "accessories", "important"),
                ("flip flops", 200, 400, "beach footwear", "clothing", "important"),
                ("beach bag", 200, 1000, "carrying beach items", "accessories", "nice-to-have"),
            ],
            ActivityType.FORMAL: [
                ("formal dress/suit", 600, 1200, "formal events", "clothing", "essential"),
                ("dress shoes", 600, 800, "formal footwear", "clothing", "essential"),
                ("formal accessories", 100, 100, "completing formal look", "accessories", "important"),
            ]
        }
    
    def _load_weather_items(self) -> Dict[str, Any]:
        """Load weather-specific items database"""
        return {}  # Defined inline in generation methods for now