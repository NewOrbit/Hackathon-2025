"""
Persist Packing List MCP Server - Manage and persist travel packing lists.

To run this server:
    uv run mcp dev main.py

Provides persistent storage for travel packing lists with full CRUD operations
and status tracking.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from mcp.server.fastmcp import FastMCP
PACKING_LIST_FILE = "persist-packing-list.md"

mcp = FastMCP("Persist Packing List", port=8011)

# Packing List Management Tools

# Get a packing list (resource)
@mcp.tool()
def retrieve_saved_packing_list() -> str:
    """Retrieve the current packing list in a markdown format"""
    try:
        with open(PACKING_LIST_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


# Upsert a packing list (tool)
@mcp.tool()
def update_saved_packing_list(content: str) -> Dict[str, Any]:
    """Create or update the packing list with the provided content

    Args:
        content: The full content of the packing list in markdown format

    Returns:
        Dictionary with success status and message
    """
    try:
        with open(PACKING_LIST_FILE, "w", encoding="utf-8") as file:
            file.write(content)
        return {"success": True, "message": "Packing list saved successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error saving packing list: {e}"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")