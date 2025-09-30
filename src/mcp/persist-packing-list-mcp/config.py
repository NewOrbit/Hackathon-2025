"""
Configuration settings for the persist-packing-list MCP server.
"""

import os
from pathlib import Path

# Storage configuration
STORAGE_PATH = os.getenv(
    "PACKING_LIST_DB_PATH", 
    str(Path(__file__).parent / "persist-packing-list.md")
)

# Create storage directory if it doesn't exist
Path(STORAGE_PATH).parent.mkdir(parents=True, exist_ok=True)

# Server configuration
SERVER_NAME = "Persist Packing List"
SERVER_VERSION = "1.0.0"
DEFAULT_PORT = 8009

# Application settings
MAX_LISTS_PER_USER = 50
MAX_ITEMS_PER_LIST = 200
DEFAULT_LIST_NAME = "My Packing List"