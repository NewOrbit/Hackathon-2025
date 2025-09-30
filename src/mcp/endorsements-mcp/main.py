"""
Endorsements MCP Server - Manage endorsements for the travel agent.

To run this server:
    uv run main.py

Provides functionality to add, retrieve, and manage endorsements for the travel agent,
with persistent storage in text files.
"""

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from endorsements_service import (
    add_endorsement_data,
    get_endorsements_data,
    get_endorsement_stats_data,
    remove_endorsement_data,
    get_endorsement_prompt,
    format_endorsement_summary
)
from config import get_port

mcp = FastMCP("Endorsements", port=get_port())

# Tools
@mcp.tool()
def add_endorsement(name: str, comment: str = "") -> Dict[str, Any]:
    """Add a new endorsement for the travel agent
    
    Args:
        name: Name of the person endorsing the travel agent (required)
        comment: Optional comment or testimonial about the travel agent
        
    Returns:
        Dictionary with success status, message, and endorsement details
    """
    return add_endorsement_data(name, comment)


@mcp.tool()
def get_endorsements() -> Dict[str, Any]:
    """Get all endorsements for the travel agent
    
    Returns:
        Dictionary containing list of all endorsements, count, and formatted display
    """
    return get_endorsements_data()


@mcp.tool()
def get_endorsement_stats() -> Dict[str, Any]:
    """Get statistics about endorsements
    
    Returns:
        Dictionary with total count, recent count, and latest endorsement info
    """
    return get_endorsement_stats_data()


@mcp.tool()
def remove_endorsement(name: str) -> Dict[str, Any]:
    """Remove an endorsement by name
    
    Args:
        name: Name of the person whose endorsement should be removed
        
    Returns:
        Dictionary with success status and message
    """
    return remove_endorsement_data(name)


@mcp.tool()
def get_endorsement_invitation() -> str:
    """Get a friendly invitation message for users to add endorsements
    
    Returns:
        A personalized invitation message based on current endorsement status
    """
    return get_endorsement_prompt()


@mcp.tool()
def get_endorsement_summary() -> str:
    """Get a brief summary of endorsements for quick display
    
    Returns:
        Brief summary string with endorsement count and latest endorsement
    """
    return format_endorsement_summary()


# Resources (optional - for providing additional context)
@mcp.resource("endorsements://all")
def endorsements_resource():
    """Resource containing all endorsements data"""
    data = get_endorsements_data()
    return data["formatted_display"]


@mcp.resource("endorsements://stats") 
def endorsements_stats_resource():
    """Resource containing endorsement statistics"""
    stats = get_endorsement_stats_data()
    
    summary = f"Endorsement Statistics:\n"
    summary += f"Total Endorsements: {stats['total_count']}\n"
    summary += f"Recent Endorsements (30 days): {stats['recent_count']}\n"
    
    if stats['latest_endorsement']:
        latest = stats['latest_endorsement']
        summary += f"Latest Endorsement: {latest['name']} on {latest['timestamp']}\n"
        if latest.get('comment'):
            summary += f"Comment: \"{latest['comment']}\"\n"
    
    return summary


if __name__ == "__main__":
    print(f"Starting Endorsements MCP server on port {get_port()}...")
    mcp.run(transport="streamable-http")