"""Static fixtures powering Phase 1 mock MCP clients."""

from __future__ import annotations

WEATHER_FIXTURES = {
    "default": {
        "location": "Generic Destination",
        "temperature_c": 20.0,
        "condition": "Partly cloudy",
        "humidity": 50,
        "wind_kmh": 10,
    },
    "paris": {
        "location": "Paris, France",
        "temperature_c": 12.3,
        "condition": "Light rain",
        "humidity": 82,
        "wind_kmh": 14,
    },
    "oslo": {
        "location": "Oslo, Norway",
        "temperature_c": 2.0,
        "condition": "Snow showers",
        "humidity": 88,
        "wind_kmh": 18,
    },
}

SECURITY_FIXTURES = {
    "default": {
        "prohibited": ["flammable_liquids", "explosives"],
        "restricted": ["liquids_over_100ml", "power_banks_over_100wh"],
        "notes": ["Follow standard airport security guidelines."],
    }
}

VISA_FIXTURES = {
    "pl-fr": {
        "visa_required": False,
        "passport_validity_months": 3,
        "notes": ["Passport must be valid for 3 months beyond stay."],
    },
    "default": {
        "visa_required": True,
        "passport_validity_months": 6,
        "notes": ["Check embassy for specific visa requirements."],
    },
}

BOOKING_FIXTURES = {
    "paris": {
        "flights": [
            {
                "id": "FL-001",
                "price": 220.0,
                "currency": "EUR",
                "summary": "Mock flight to Paris",
            }
        ],
        "hotels": [
            {
                "id": "HT-101",
                "price": 150.0,
                "currency": "EUR",
                "summary": "Cozy mock hotel near Louvre",
            }
        ],
        "activities": [
            {
                "id": "AC-41",
                "title": "Guided Louvre tour",
                "price": 60.0,
                "currency": "EUR",
            }
        ],
    },
    "default": {
        "flights": [],
        "hotels": [],
        "activities": [],
    },
}

BUDGET_FIXTURES = {
    "default": {
        "laundry_per_load": 8.0,
        "basic_toiletries_kit": 12.5,
        "travel_size_kit": 6.0,
        "checked_bag_fee": 35.0,
    }
}

__all__ = [
    "WEATHER_FIXTURES",
    "SECURITY_FIXTURES",
    "VISA_FIXTURES",
    "BOOKING_FIXTURES",
    "BUDGET_FIXTURES",
]

