"""Unit tests for the packing engine and data models"""

import pytest
from datetime import date, datetime
from src.agent.packing_engine import PackingEngine
from src.agent.packing_models import (
    PackingListRequest, TripParameters, PackingConstraints, WeatherForecast,
    ActivityType, WeatherCondition, Priority, SafetyStatus, WeightClass
)

class TestPackingEngine:
    """Test cases for PackingEngine class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = PackingEngine()
        
        # Basic trip parameters
        self.basic_trip = TripParameters(
            destination="Paris",
            departure_date=date(2025, 11, 1),
            return_date=date(2025, 11, 5),
            trip_length_days=4,
            activities=[ActivityType.CASUAL, ActivityType.CULTURAL],
            accommodation_type="hotel"
        )
        
        # Basic constraints
        self.basic_constraints = PackingConstraints(
            capacity_liters=28,
            max_weight_kg=15.0,
            airline="Delta",
            cabin_class="economy",
            has_laundry_access=False,
            liquid_restrictions=True
        )
        
        # Weather forecast
        self.paris_weather = WeatherForecast(
            location="Paris",
            conditions=[WeatherCondition.COOL, WeatherCondition.RAINY],
            temperature_range_c={"min": 8, "max": 15},
            precipitation_probability=0.6
        )
    
    def test_basic_packing_list_generation(self):
        """Test basic packing list generation"""
        request = PackingListRequest(
            trip_parameters=self.basic_trip,
            constraints=self.basic_constraints
        )
        
        response = self.engine.generate_packing_list(request)
        
        # Basic assertions
        assert len(response.items) > 0
        assert response.total_estimated_weight_g > 0
        assert response.total_estimated_volume_ml > 0
        assert response.generation_mode == "full"
        
        # Check essential items are present
        item_names = [item.name for item in response.items]
        assert "passport" in item_names
        assert "phone" in item_names
        assert "underwear" in item_names
    
    def test_trip_length_scaling(self):
        """Test that trip length affects item quantities"""
        # Short trip (2 days)
        short_trip = TripParameters(
            destination="London",
            departure_date=date(2025, 11, 1),
            return_date=date(2025, 11, 3),
            trip_length_days=2,
            activities=[ActivityType.CASUAL]
        )
        
        # Long trip (10 days)
        long_trip = TripParameters(
            destination="London", 
            departure_date=date(2025, 11, 1),
            return_date=date(2025, 11, 11),
            trip_length_days=10,
            activities=[ActivityType.CASUAL]
        )
        
        short_request = PackingListRequest(trip_parameters=short_trip, constraints=self.basic_constraints)
        long_request = PackingListRequest(trip_parameters=long_trip, constraints=self.basic_constraints)
        
        short_response = self.engine.generate_packing_list(short_request)
        long_response = self.engine.generate_packing_list(long_request)
        
        # Find underwear quantities
        short_underwear = next((item for item in short_response.items if item.name == "underwear"), None)
        long_underwear = next((item for item in long_response.items if item.name == "underwear"), None)
        
        assert short_underwear is not None
        assert long_underwear is not None
        assert long_underwear.quantity > short_underwear.quantity
    
    def test_weather_adaptation(self):
        """Test that weather conditions add appropriate items"""
        # Cold weather
        cold_weather = WeatherForecast(
            location="Oslo",
            conditions=[WeatherCondition.COLD, WeatherCondition.SNOWY],
            temperature_range_c={"min": -5, "max": 2},
            precipitation_probability=0.8
        )
        
        request = PackingListRequest(
            trip_parameters=self.basic_trip,
            constraints=self.basic_constraints,
            weather_forecast=cold_weather
        )
        
        response = self.engine.generate_packing_list(request)
        item_names = [item.name for item in response.items]
        
        # Should include cold weather items
        assert "warm jacket" in item_names
        assert "gloves" in item_names
        assert any("rain" in name for name in item_names)  # Rain gear for snow
    
    def test_activity_items(self):
        """Test that activities add specific items"""
        business_trip = TripParameters(
            destination="Tokyo",
            departure_date=date(2025, 11, 1),
            return_date=date(2025, 11, 4),
            trip_length_days=3,
            activities=[ActivityType.BUSINESS, ActivityType.FORMAL]
        )
        
        request = PackingListRequest(
            trip_parameters=business_trip,
            constraints=self.basic_constraints
        )
        
        response = self.engine.generate_packing_list(request)
        item_names = [item.name for item in response.items]
        
        # Should include business items
        assert "business suit" in item_names
        assert "laptop" in item_names
        assert "dress shoes" in item_names
    
    def test_capacity_constraints(self):
        """Test that capacity constraints are respected"""
        # Very restrictive constraints
        tight_constraints = PackingConstraints(
            capacity_liters=10,  # Very small backpack
            max_weight_kg=5.0,   # Very light
            liquid_restrictions=True
        )
        
        request = PackingListRequest(
            trip_parameters=self.basic_trip,
            constraints=tight_constraints
        )
        
        response = self.engine.generate_packing_list(request)
        
        # Should fit within constraints
        assert response.total_estimated_volume_ml <= 10000  # 10L = 10000ml
        assert response.total_estimated_weight_g <= 5000    # 5kg = 5000g
        
        # Should have violations recorded if items were removed
        if not response.fits_constraints:
            assert len(response.constraint_violations) > 0
    
    def test_liquid_restrictions(self):
        """Test that liquid restrictions are applied"""
        request = PackingListRequest(
            trip_parameters=self.basic_trip,
            constraints=self.basic_constraints
        )
        
        response = self.engine.generate_packing_list(request)
        
        # Find toiletry items
        toiletry_items = [item for item in response.items if item.category == "toiletries"]
        
        # Liquid items should be travel-size or have restrictions noted
        for item in toiletry_items:
            if "liquid" in item.name.lower() or "toothpaste" in item.name.lower():
                assert item.estimated_volume_ml <= 100 or item.restrictions is not None
    
    def test_priority_assignment(self):
        """Test that items have appropriate priority assignments"""
        request = PackingListRequest(
            trip_parameters=self.basic_trip,
            constraints=self.basic_constraints
        )
        
        response = self.engine.generate_packing_list(request)
        
        # Essential items should have highest priority
        passport_item = next((item for item in response.items if item.name == "passport"), None)
        assert passport_item is not None
        assert passport_item.priority == Priority.ESSENTIAL
        
        # Check that we have items across different priorities
        priorities = {item.priority for item in response.items}
        assert Priority.ESSENTIAL in priorities
        assert len(priorities) > 1  # Should have multiple priority levels
    
    def test_weight_class_calculation(self):
        """Test weight class calculation"""
        # Test the weight class calculation method
        assert self.engine._calculate_weight_class(30) == WeightClass.NEGLIGIBLE
        assert self.engine._calculate_weight_class(100) == WeightClass.LIGHT
        assert self.engine._calculate_weight_class(300) == WeightClass.MEDIUM
        assert self.engine._calculate_weight_class(700) == WeightClass.HEAVY
        assert self.engine._calculate_weight_class(1500) == WeightClass.VERY_HEAVY
    
    def test_category_summaries(self):
        """Test category summary generation"""
        request = PackingListRequest(
            trip_parameters=self.basic_trip,
            constraints=self.basic_constraints
        )
        
        response = self.engine.generate_packing_list(request)
        
        # Should have category summaries
        assert len(response.category_summaries) > 0
        
        # Check clothing category exists and has expected structure
        if "clothing" in response.category_summaries:
            clothing_summary = response.category_summaries["clothing"]
            assert "item_count" in clothing_summary
            assert "total_weight_g" in clothing_summary
            assert "total_volume_ml" in clothing_summary
            assert clothing_summary["item_count"] > 0


class TestPackingModels:
    """Test cases for Pydantic models"""
    
    def test_packing_list_item_creation(self):
        """Test PackingListItem model validation"""
        from src.agent.packing_models import PackingListItem
        
        item = PackingListItem(
            name="test item",
            category="test",
            quantity=2,
            estimated_weight_g=100,
            estimated_volume_ml=50,
            safety_status=SafetyStatus.SAFE,
            priority=Priority.IMPORTANT,
            weight_class=WeightClass.LIGHT,
            reason="test reason",
            source_rule="test_rule"
        )
        
        assert item.name == "test item"
        assert item.quantity == 2
        assert item.estimated_weight_g == 100
        assert item.priority == Priority.IMPORTANT
    
    def test_trip_parameters_validation(self):
        """Test TripParameters model validation"""
        trip = TripParameters(
            destination="Test City",
            departure_date=date(2025, 11, 1),
            return_date=date(2025, 11, 5),
            trip_length_days=4,
            activities=[ActivityType.CASUAL, ActivityType.BUSINESS]
        )
        
        assert trip.destination == "Test City"
        assert trip.trip_length_days == 4
        assert len(trip.activities) == 2
    
    def test_packing_constraints_defaults(self):
        """Test PackingConstraints model with defaults"""
        constraints = PackingConstraints()
        
        # Test default values
        assert constraints.capacity_liters is None
        assert constraints.max_weight_kg is None
        assert constraints.cabin_class == "economy"
        assert constraints.has_laundry_access is False
        assert constraints.liquid_restrictions is True