"""Configuration for Booking MCP Server"""

import os
from typing import Dict, Any

# Phase 1: Enforce offline mode
OFFLINE_MODE = os.getenv("DEEPSEEKTRAVELS_OFFLINE", "true").lower() == "true"
USE_MOCKS = os.getenv("DEEPSEEKTRAVELS_USE_MOCKS", "true").lower() == "true"

# Network guard - Phase 1 should never make external HTTP calls
def ensure_offline_mode():
    """Raise exception if trying to make external calls in Phase 1"""
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: External HTTP calls are not permitted. Set DEEPSEEKTRAVELS_OFFLINE=true and DEEPSEEKTRAVELS_USE_MOCKS=true")

# Mock booking data configuration
MOCK_DATA_VERSION = "1.0.0"
MOCK_SOURCES = {
    "flights": "Flight booking APIs (mocked)",
    "hotels": "Hotel booking APIs (mocked)", 
    "activities": "Activity booking APIs (mocked)",
    "pricing": "Mock pricing data for development"
}

# Booking session storage (in-memory for Phase 1)
BOOKING_SESSIONS = {}