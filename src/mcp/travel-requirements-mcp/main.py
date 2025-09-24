"""
Travel Requirements MCP Server - Mock travel requirements data for packing list agent.

To run this server:
    uv run main.py

Phase 1: All data is mocked/offline - no external HTTP calls.
"""

from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from models import (
    BaggageRule, SecurityRestriction, VisaRequirement, 
    TravelDocument, BaggageRulesRequest, SecurityRestrictionsRequest,
    VisaRequirementsRequest, TravelDocumentsRequest
)
from travel_requirements_service import (
    get_baggage_rules_mock, get_security_restrictions_mock,
    get_visa_requirements_mock, get_travel_documents_mock
)
from config import OFFLINE_MODE, USE_MOCKS

mcp = FastMCP("TravelRequirements", port=8010)

@mcp.tool()
def check_baggage_rules(
    airline: str,
    cabin_class: str = "economy", 
    route: str = "international"
) -> Dict[str, Any]:
    """Check baggage allowances and restrictions for specific airline and route
    
    Args:
        airline: Airline code or name (e.g., "AA", "Delta", "British Airways")
        cabin_class: Cabin class (economy, business, first)
        route: Route type (domestic, international, regional)
    
    Returns:
        Dict containing baggage rules, weight limits, size restrictions, fees
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    return get_baggage_rules_mock(airline, cabin_class, route)

@mcp.tool()
def check_security_restrictions(
    departure_country: str,
    arrival_country: str,
    items: List[str] = None
) -> Dict[str, Any]:
    """Check airport security restrictions for specific items and routes
    
    Args:
        departure_country: Country code of departure (e.g., "US", "GB", "JP")
        arrival_country: Country code of arrival
        items: Optional list of specific items to check (e.g., ["laptop", "liquids", "batteries"])
    
    Returns:
        Dict containing security restrictions, prohibited items, quantity limits
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    return get_security_restrictions_mock(departure_country, arrival_country, items or [])

@mcp.tool()
def check_visa_requirements(
    passport_country: str,
    destination_country: str,
    trip_duration_days: int,
    purpose: str = "tourism"
) -> Dict[str, Any]:
    """Check visa requirements for travel between countries
    
    Args:
        passport_country: Country code of passport holder (e.g., "US", "GB")
        destination_country: Country code of destination (e.g., "JP", "FR")
        trip_duration_days: Length of stay in days
        purpose: Purpose of travel (tourism, business, transit)
    
    Returns:
        Dict containing visa requirements, processing time, fees, documents needed
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    return get_visa_requirements_mock(passport_country, destination_country, trip_duration_days, purpose)

@mcp.tool() 
def check_travel_documents(
    destination_country: str,
    passport_country: str,
    departure_date: str,
    return_date: str = None
) -> Dict[str, Any]:
    """Check required travel documents and validity requirements
    
    Args:
        destination_country: Country code of destination (e.g., "JP", "AU")
        passport_country: Country code of passport holder 
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Optional return date in YYYY-MM-DD format
    
    Returns:
        Dict containing document requirements, validity periods, additional documents
    """
    if not OFFLINE_MODE or not USE_MOCKS:
        raise RuntimeError("Phase 1: Only offline/mock mode is permitted")
    
    return get_travel_documents_mock(destination_country, passport_country, departure_date, return_date)

if __name__ == "__main__":
    import uvicorn
    print("🛂 Starting Travel Requirements MCP Server on http://localhost:8010/mcp/")
    print("⚠️  Phase 1: Running in OFFLINE/MOCK mode only")
    uvicorn.run("main:mcp.app", host="127.0.0.1", port=8010, reload=True)