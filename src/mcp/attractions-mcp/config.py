"""
Tourist attractions MCP configuration constants.
"""

# World Tourist Attractions API configuration
ATTRACTIONS_BASE_URL = "https://www.world-tourist-attractions-api.com"
API_VERSION = "v1"

# API Endpoints
ENDPOINTS = {
    "attraction_by_id": f"/api/{API_VERSION}/attraction",
    "random_famous": f"/api/{API_VERSION}/random/famous",
    "random_india": f"/api/{API_VERSION}/random/india", 
    "wonders": f"/api/{API_VERSION}/wonders",
    "search": f"/api/{API_VERSION}/search",
    "categories": f"/api/{API_VERSION}/categories"
}

# Attraction categories
ATTRACTION_CATEGORIES = {
    "historical": "Historical Sites",
    "natural": "Natural Wonders", 
    "cultural": "Cultural Sites",
    "religious": "Religious Sites",
    "modern": "Modern Attractions",
    "museums": "Museums",
    "parks": "Parks & Gardens",
    "beaches": "Beaches",
    "mountains": "Mountains",
    "architecture": "Architecture",
    "entertainment": "Entertainment",
    "adventure": "Adventure Sports"
}

# Popular countries/regions
POPULAR_REGIONS = [
    "India", "France", "Italy", "Spain", "Greece", "Egypt", 
    "Thailand", "Japan", "China", "USA", "UK", "Germany",
    "Turkey", "Morocco", "Brazil", "Peru", "Australia"
]

# Booking status codes
BOOKING_STATUS = {
    "pending": "Pending Confirmation",
    "confirmed": "Confirmed", 
    "cancelled": "Cancelled",
    "completed": "Completed"
}

# Default values
DEFAULT_SEARCH_LIMIT = 20
MAX_SEARCH_LIMIT = 100
DEFAULT_RATING_MIN = 3.0
