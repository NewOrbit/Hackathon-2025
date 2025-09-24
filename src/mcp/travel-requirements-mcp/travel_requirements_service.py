"""Travel Requirements Service - Mock data provider for Phase 1"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from config import ensure_offline_mode, MOCK_SOURCES

def get_baggage_rules_mock(airline: str, cabin_class: str, route: str) -> Dict[str, Any]:
    """Get mock baggage rules data"""
    ensure_offline_mode()
    
    # Mock baggage data for different airlines
    baggage_data = {
        "AA": {"carry_on_kg": 10, "checked_kg": 23, "dimensions": "56x36x23"},
        "Delta": {"carry_on_kg": 10, "checked_kg": 23, "dimensions": "56x35x23"},
        "British Airways": {"carry_on_kg": 8, "checked_kg": 23, "dimensions": "56x40x23"},
        "ANA": {"carry_on_kg": 10, "checked_kg": 20, "dimensions": "55x40x25"},
        "default": {"carry_on_kg": 8, "checked_kg": 20, "dimensions": "55x40x20"}
    }
    
    data = baggage_data.get(airline, baggage_data["default"])
    
    # Adjust for cabin class
    if cabin_class.lower() == "business":
        data["checked_kg"] += 9  # Business gets extra weight
    elif cabin_class.lower() == "first":
        data["checked_kg"] += 17  # First gets even more
        
    return {
        "airline": airline,
        "cabin_class": cabin_class,
        "route_type": route,
        "carry_on": {
            "weight_limit_kg": data["carry_on_kg"],
            "dimensions_cm": data["dimensions"],
            "quantity": 1
        },
        "checked": {
            "weight_limit_kg": data["checked_kg"],
            "dimensions_cm": "158cm total linear dimensions",
            "included_bags": 1,
            "excess_fee_per_kg": 20.0
        },
        "prohibited_items": [
            "flammable liquids", "weapons", "explosives", "lithium batteries >100Wh",
            "compressed gases", "toxic substances"
        ],
        "liquid_restrictions": {
            "carry_on_limit_ml": 100,
            "total_liquids_limit_l": 1.0,
            "container_requirement": "clear plastic bag"
        },
        "source": MOCK_SOURCES["airline_policies"],
        "mock_data": True
    }

def get_security_restrictions_mock(departure_country: str, arrival_country: str, items: List[str]) -> Dict[str, Any]:
    """Get mock security restrictions data"""
    ensure_offline_mode()
    
    # Common security restrictions
    common_restrictions = {
        "liquids": {
            "status": "restricted",
            "carry_on_allowed": True,
            "checked_allowed": True,
            "quantity_limit": "containers ≤100ml, total ≤1L",
            "special_instructions": "Must be in clear plastic bag"
        },
        "laptop": {
            "status": "allowed",
            "carry_on_allowed": True,
            "checked_allowed": True,
            "special_instructions": "May need to be removed for screening"
        },
        "batteries": {
            "status": "restricted", 
            "carry_on_allowed": True,
            "checked_allowed": False,
            "quantity_limit": "lithium <100Wh carry-on only",
            "special_instructions": "Spare batteries must be in carry-on"
        },
        "knife": {
            "status": "prohibited",
            "carry_on_allowed": False,
            "checked_allowed": True,
            "special_instructions": "Must be packed in checked luggage"
        },
        "medication": {
            "status": "allowed",
            "carry_on_allowed": True,  
            "checked_allowed": True,
            "special_instructions": "Bring prescription or doctor's note"
        }
    }
    
    # Country-specific variations
    country_variations = {
        "US": {"additional_screening": ["electronics >tablet size", "food items"]},
        "GB": {"additional_screening": ["powders >350ml"]},
        "JP": {"additional_screening": ["certain medications require permits"]},
        "AU": {"additional_screening": ["biological materials", "wooden items"]}
    }
    
    restrictions = {}
    for item in items:
        item_lower = item.lower()
        # Find matching restriction
        for key, restriction in common_restrictions.items():
            if key in item_lower:
                restrictions[item] = restriction
                break
        else:
            # Default for unknown items
            restrictions[item] = {
                "status": "unknown",
                "carry_on_allowed": None,
                "checked_allowed": None,
                "special_instructions": "Check with airline/TSA for specific item"
            }
    
    return {
        "departure_country": departure_country,
        "arrival_country": arrival_country,
        "restrictions": restrictions,
        "general_rules": {
            "liquid_limit_ml": 100,
            "total_liquid_limit_l": 1.0,
            "electronics_screening": "May require separate screening",
            "sharp_objects": "Prohibited in carry-on"
        },
        "country_specific": country_variations.get(departure_country, {}),
        "source": MOCK_SOURCES["tsa"],
        "mock_data": True
    }

def get_visa_requirements_mock(passport_country: str, destination_country: str, trip_duration_days: int, purpose: str) -> Dict[str, Any]:
    """Get mock visa requirements data"""
    ensure_offline_mode()
    
    # Mock visa requirements (simplified)
    visa_free_countries = {
        "US": ["GB", "FR", "DE", "JP", "AU", "CA"],  # US passport holders
        "GB": ["US", "FR", "DE", "JP", "AU"],        # UK passport holders  
        "JP": ["US", "GB", "FR", "DE", "AU"],        # Japanese passport holders
    }
    
    visa_required = destination_country not in visa_free_countries.get(passport_country, [])
    
    if not visa_required:
        return {
            "passport_country": passport_country,
            "destination_country": destination_country,
            "visa_required": False,
            "max_stay_days": 90 if purpose == "tourism" else 30,
            "entry_requirements": ["Valid passport", "Return ticket", "Proof of funds"],
            "source": MOCK_SOURCES["embassy"],
            "mock_data": True
        }
    
    # Mock visa requirements for countries that need visas
    return {
        "passport_country": passport_country,
        "destination_country": destination_country,
        "visa_required": True,
        "visa_type": "tourist" if purpose == "tourism" else "business",
        "processing_time_days": 10,
        "fee_usd": 60.0,
        "documents_required": [
            "Valid passport (6+ months validity)",
            "Completed visa application",
            "Passport photos",
            "Proof of accommodation",
            "Return flight tickets",
            "Bank statements"
        ],
        "max_stay_days": 30,
        "source": MOCK_SOURCES["embassy"],
        "mock_data": True
    }

def get_travel_documents_mock(destination_country: str, passport_country: str, departure_date: str, return_date: str = None) -> Dict[str, Any]:
    """Get mock travel documents requirements"""
    ensure_offline_mode()
    
    departure_dt = datetime.fromisoformat(departure_date)
    
    # Basic document requirements
    documents = [
        {
            "document_type": "passport",
            "required": True,
            "validity_months_required": 6,
            "special_requirements": f"Must be valid for 6 months beyond {departure_date}"
        }
    ]
    
    # Add visa if required (simplified logic)
    visa_required_destinations = ["CN", "RU", "IN", "BR"]  # Example countries
    if destination_country in visa_required_destinations:
        documents.append({
            "document_type": "visa",
            "required": True,
            "validity_months_required": None,
            "special_requirements": "Must be obtained before travel"
        })
    
    # Add health requirements for certain destinations  
    health_cert_destinations = ["BR", "KE", "TZ", "ZA"]  # Example countries requiring yellow fever cert
    if destination_country in health_cert_destinations:
        documents.append({
            "document_type": "vaccination_certificate",
            "required": True,
            "validity_months_required": None,
            "special_requirements": "Yellow fever vaccination required"
        })
        
    return {
        "destination_country": destination_country,
        "passport_country": passport_country,
        "departure_date": departure_date,
        "return_date": return_date,
        "documents_required": documents,
        "additional_recommendations": [
            "Travel insurance",
            "Emergency contact information",
            "Copies of important documents",
            "Credit/debit cards with travel notification"
        ],
        "source": MOCK_SOURCES["embassy"],
        "mock_data": True
    }