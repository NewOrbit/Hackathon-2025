"""
Nutrition Trivia MCP configuration and in-memory database.
"""

# Keep the old database for backward compatibility (empty for now)
SECRET_DATABASE = {}

# Tip categories for organized retrieval
TIP_CATEGORIES = {
    "photo": "Photography tips and best spots",
    "food": "Secret menu items and hidden restaurants",
    "timing": "Best times to visit and avoid crowds",
    "access": "Secret entrances and hidden areas",
    "local": "Local customs and insider knowledge",
}

# Secret types
SECRET_TYPES = ["secrets", "celebrity_sightings", "insider_tips"]