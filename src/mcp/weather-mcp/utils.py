"""
Utility functions for weather operations.
"""

import requests
from typing import Dict, Any, Optional

from config import WEATHER_CODES, GEOCODING_BASE_URL
from models import Coordinates, Location


def make_api_request(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make an API request with error handling"""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def get_coordinates(location: str) -> Optional[Location]:
    """Get latitude and longitude for a location using Open-Meteo Geocoding API"""
    url = f"{GEOCODING_BASE_URL}/search"
    params = {"name": location, "count": 1, "language": "en", "format": "json"}
    
    data = make_api_request(url, params)
    if not data.get("results"):
        return None
    
    result = data["results"][0]
    coords = Coordinates(lat=result["latitude"], lon=result["longitude"])
    return Location(
        name=result["name"],
        country=result.get("country", ""),
        admin1=result.get("admin1", ""),
        timezone=result.get("timezone", ""),
        coordinates=coords
    )


def format_location_name(location: Location) -> str:
    """Format location name with state/country"""
    name = location.name
    if location.admin1:
        name += f", {location.admin1}"
    if location.country:
        name += f", {location.country}"
    return name


def get_weather_description(code: int) -> str:
    """Get weather description from code"""
    return WEATHER_CODES.get(code, f"Unknown weather code: {code}")
