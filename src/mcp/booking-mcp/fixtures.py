"""Mock fixtures supporting the booking MCP server."""

BOOKING_FIXTURES = {
    "paris": {
        "flights": [
            {
                "id": "FL-001",
                "summary": "Morning departure from Warsaw",
                "price": 220.0,
                "currency": "EUR",
            }
        ],
        "hotels": [
            {
                "id": "HT-101",
                "name": "Hotel Mock Louvre",
                "price": 150.0,
                "currency": "EUR",
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

