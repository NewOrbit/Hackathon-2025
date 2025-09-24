"""
Trivia MCP Server - Local secrets and insider information about attractions.

To run this server:
    uv run mcp dev main.py

Provides local secrets, celebrity sightings, and insider tips about attractions.
"""

from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from trivia_service import (
    get_attraction_secret,
    get_insider_tip,
    get_celebrity_drama,
    get_all_attraction_secrets,
    get_available_attractions,
    format_attraction_secrets,
)

mcp = FastMCP("Trivia", port=8013)


# tools
@mcp.tool()
def get_attraction_secret_tool(attraction_id: str) -> Dict[str, Any]:
    """Get a random secret, celebrity sighting, or insider tip for an attraction

    Args:
        attraction_id: ID of the attraction (e.g., "space_needle", "pike_place", "times_square")

    Returns:
        SecretResponse object as dictionary with random secret/sighting/tip
    """
    return get_attraction_secret(attraction_id)


@mcp.tool()
def get_insider_tip_tool(
    attraction_id: str, tip_type: Optional[str] = None
) -> Dict[str, Any]:
    """Get insider tips for a specific attraction, optionally filtered by type

    Args:
        attraction_id: ID of the attraction
        tip_type: Optional tip category filter ("photo", "food", "timing", "access", "local")

    Returns:
        List of insider tips as dictionary
    """
    return get_insider_tip(attraction_id, tip_type)


@mcp.tool()
def get_celebrity_drama_tool(location: str) -> Dict[str, Any]:
    """Get celebrity sightings and drama for a location

    Args:
        location: Location name (e.g., "space_needle", "pike_place", "times_square")

    Returns:
        Celebrity sightings and drama as dictionary
    """
    return get_celebrity_drama(location)


@mcp.tool()
def get_all_attraction_secrets_tool(attraction_id: str) -> Dict[str, Any]:
    """Get all secrets, celebrity sightings, and insider tips for an attraction

    Args:
        attraction_id: ID of the attraction

    Returns:
        Complete AttractionSecret object as dictionary
    """
    return get_all_attraction_secrets(attraction_id)


@mcp.tool()
def get_available_attractions_tool() -> Dict[str, Any]:
    """Get list of all attractions with secrets available

    Returns:
        List of available attractions as dictionary
    """
    return get_available_attractions()


# resources
@mcp.resource("trivia://attraction/{attraction_id}")
def get_attraction_secrets_resource(attraction_id: str) -> str:
    """Get all secrets for an attraction as a formatted resource"""
    return format_attraction_secrets(attraction_id)


@mcp.resource("trivia://attractions")
def get_available_attractions_resource() -> str:
    """Get list of available attractions as a formatted resource"""
    data = get_available_attractions()
    if "error" in data:
        return f"Error: {data['error']}"

    result = "🎯 **Available Attractions with Secrets**\n\n"
    result += f"Total Attractions: {data['total_attractions']}\n\n"

    for attraction in data["attractions"]:
        result += f"• **{attraction.replace('_', ' ').title()}**\n"

    result += f"\n**Tip Categories:** {', '.join(data['tip_categories'])}\n"
    result += f"**Secret Types:** {', '.join(data['secret_types'])}\n"

    return result


# prompts
@mcp.prompt()
def attraction_secrets_prompt(attraction_id: str) -> str:
    """Generate a prompt for discovering attraction secrets"""
    return f"""Please help discover and share local secrets about {attraction_id.replace('_', ' ').title()}, including:
1. Hidden local secrets and legends
2. Celebrity sightings and drama
3. Insider tips for the best experience
4. Secret spots and hidden areas
5. Local customs and traditions
6. Best times to visit for unique experiences
7. Secret menu items or hidden services

Focus on providing insider knowledge that only locals would know."""


@mcp.prompt()
def travel_secrets_prompt(location: str) -> str:
    """Generate a prompt for discovering travel secrets for a location"""
    return f"""Please help uncover the hidden secrets of {location}, including:
1. Local legends and urban myths
2. Celebrity sightings and famous visitors
3. Insider tips for avoiding crowds
4. Secret photo spots and hidden viewpoints
5. Local food secrets and hidden restaurants
6. Best times to visit for unique experiences
7. Cultural secrets and local customs
8. Hidden historical facts and stories

Share the kind of knowledge that makes you feel like a local insider."""


@mcp.prompt()
def celebrity_hunting_prompt(location: str) -> str:
    """Generate a prompt for celebrity spotting and drama"""
    return f"""Please help with celebrity hunting in {location}, including:
1. Recent celebrity sightings and encounters
2. Famous people who frequent this location
3. Celebrity drama and gossip
4. Best spots for celebrity spotting
5. Local celebrity stories and legends
6. Famous visitors and their experiences
7. Celebrity-related local traditions
8. Insider tips for increasing celebrity encounter chances

Focus on the juiciest celebrity gossip and most interesting encounters."""


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
