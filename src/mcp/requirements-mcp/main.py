"""Travel requirements MCP server with mocked data.

Run with:
    uv run mcp dev main.py
"""

from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

from requirements_service import requirements_router


mcp = FastMCP("TravelRequirements", port=8010)


@mcp.tool()
def get_airport_security_rules(
    airport_code: Optional[str] = None,
    country_code: Optional[str] = None,
    airline: Optional[str] = None,
    cabin_class: Optional[str] = None,
) -> Dict[str, Any]:
    """Get prohibited and restricted items rules for an airport or airline."""
    return requirements_router.get_security_rules(airport_code, country_code, airline, cabin_class)


@mcp.tool()
def get_visa_requirements(
    nationality: str,
    destination_country: str,
    stay_length_days: int = 7,
) -> Dict[str, Any]:
    """Return visa and entry guidance for a traveller."""
    return requirements_router.get_visa_requirements(nationality, destination_country, stay_length_days)


@mcp.tool()
def check_baggage_allowance(
    airline: str,
    cabin_class: str = "economy",
) -> Dict[str, Any]:
    """Return baggage weight/size allowances for an airline."""
    return requirements_router.check_baggage_allowance(airline, cabin_class)


@mcp.resource("requirements://summary/{nationality}/{destination}")
def get_requirements_resource(nationality: str, destination: str) -> str:
    """Formatted summary of visa and security rules."""
    return requirements_router.format_requirements_resource(nationality, destination)


@mcp.prompt()
def documents_checklist_prompt(nationality: str, destination: str) -> str:
    """Prompt for documents/visa checklist."""
    return requirements_router.get_required_documents_prompt(nationality, destination)


if __name__ == "__main__":
    mcp.run("streamable-http")

