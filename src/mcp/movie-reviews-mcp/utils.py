"""
Utility functions for tourist movies operations.
"""

import requests
import random
import string
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from config import MOVIE_GENRES, MOCK_MOVIES
from models import Coordinates, Location, Attraction


def make_api_request(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make an API request with error handling"""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def get_movie_by_id(movie_id: int) -> Optional[Dict[str, Any]]:
    """Get movie details by ID from mock data"""
    for movie in MOCK_MOVIES:
        if movie["id"] == movie_id:
            return movie
    return None


def search_movies(
    title: Optional[str] = None,
    genre: Optional[str] = None,
    limit: int = 20
) -> Optional[Dict[str, Any]]:
    """Search for movies with filters using mock data"""
    filtered_movies = []

    for movie in MOCK_MOVIES:

        # Filter by genre
        genre_match = True
        if genre:
            genre_match = movie["genre"] == genre.lower()

        if genre_match:
            filtered_movies.append(movie)

    # Apply limit
    filtered_movies = filtered_movies[:limit]

    return {
        "movies": filtered_movies,
        "total": len(filtered_movies)
    }





def parse_coordinates(lat: float, lon: float) -> Coordinates:
    """Create coordinates object from lat/lon"""
    return Coordinates(lat=lat, lon=lon)


def parse_location_data(data: Dict[str, Any]) -> Location:
    """Parse location data from API response"""
    coords = None
    if data.get("latitude") and data.get("longitude"):
        coords = parse_coordinates(data["latitude"], data["longitude"])

    return Location(
        city=data.get("city", ""),
        country=data.get("country", ""),
        region=data.get("region", ""),
        coordinates=coords
    )


def parse_movie_data(data: Dict[str, Any]) -> Attraction:
    """Parse movie data from API response"""
    location = parse_location_data(data.get("location", {}))

    return Attraction(
        id=data.get("id", 0),
        name=data.get("name", ""),
        description=data.get("description", ""),
        genre=data.get("genre", ""),
        location=location,
        rating=data.get("rating"),
        image_url=data.get("image_url"),
        website=data.get("website"),
        opening_hours=data.get("opening_hours"),
        entry_fee=data.get("entry_fee")
    )


def format_movie_name(movie: Attraction) -> str:
    """Format movie name with location"""
    name = movie.name
    if movie.location.city:
        name += f", {movie.location.city}"
    if movie.location.country:
        name += f", {movie.location.country}"
    return name


def get_genre_display_name(genre: str) -> str:
    """Get display name for genre"""
    return ATTRACTION_CATEGORIES.get(genre.lower(), genre.title())


def generate_booking_id() -> str:
    """Generate a unique booking ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ATT-{timestamp}-{random_part}"


def generate_confirmation_code() -> str:
    """Generate a confirmation code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def validate_visit_date(date_str: str) -> bool:
    """Validate that visit date is in the future"""
    try:
        visit_date = datetime.strptime(date_str, "%Y-%m-%d")
        return visit_date.date() > datetime.now().date()
    except ValueError:
        return False


def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]


def calculate_estimated_cost(num_visitors: int, entry_fee: Optional[str] = None) -> Optional[float]:
    """Calculate estimated cost based on number of visitors"""
    if not entry_fee or "free" in entry_fee.lower():
        return 0.0

    # Simple cost calculation - in reality this would be more complex
    try:
        # Extract number from entry fee string (e.g., "$15", "₹500")
        import re
        numbers = re.findall(r'\d+\.?\d*', entry_fee)
        if numbers:
            base_cost = float(numbers[0])
            return base_cost * num_visitors
    except (ValueError, IndexError):
        pass

    return None


def format_movie_details(movie: Attraction) -> str:
    """Format movie details as a readable string"""
    location_str = f"{movie.location.city}, {movie.location.country}" if movie.location.city else movie.location.country

    details = f"🏛️ {movie.name}\n"
    details += f"📍 Location: {location_str}\n"
    details += f"🏷️ Category: {get_genre_display_name(movie.genre)}\n"

    if movie.rating:
        details += f"⭐ Rating: {movie.rating}/5.0\n"

    if movie.opening_hours:
        details += f"🕒 Hours: {movie.opening_hours}\n"

    if movie.entry_fee:
        details += f"💰 Entry Fee: {movie.entry_fee}\n"

    if movie.description:
        details += f"\n📝 Description: {movie.description}\n"

    if movie.website:
        details += f"🌐 Website: {movie.website}\n"

    return details
