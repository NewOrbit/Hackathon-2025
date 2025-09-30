"""
Configuration settings for the Endorsements MCP server.
"""

import os
from pathlib import Path

# Server configuration
DEFAULT_PORT = 8004
HOST = "0.0.0.0"

# Data file configuration
DATA_DIR = Path(__file__).parent
ENDORSEMENTS_FILE = DATA_DIR / "endorsements.txt"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

def get_port():
    """Get the port from environment variable or use default"""
    return int(os.getenv("ENDORSEMENTS_MCP_PORT", DEFAULT_PORT))