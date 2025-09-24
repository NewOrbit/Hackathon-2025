"""
Utility functions for tourist movies operations.
"""

import requests
import random
import string
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from config import MOVIE_GENRES, MOCK_MOVIES, MOCK_REVIEWS
from models import Movie


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
    genre: Optional[str] = None,
    limit: int = 20
) -> Optional[Dict[str, Any]]:
    """Search for movies with filters using mock data"""
    filtered_movies = []

    for movie in MOCK_MOVIES:

        # Filter by genre
        genre_match = True
        if genre:
            genre_match = movie["genres"] == genre.lower()

        if genre_match:
            filtered_movies.append(movie)

    # Apply limit
    filtered_movies = filtered_movies[:limit]

    return {
        "movies": filtered_movies,
        "total": len(filtered_movies)
    }

def get_random_famous_movie() -> Optional[Dict[str, Any]]:
    """Get a random famous movie from mock data"""
    if not MOCK_MOVIES:
        return None
    return random.choice(MOCK_MOVIES)


def parse_movie_data(data: Dict[str, Any]) -> Movie:
    """Parse movie data from API response"""

    return Movie(
        id=data.get("id", 0),
        title=data.get("title", ""),
        synopsis=data.get("synopsis", ""),
        genre=data.get("genre", ""),
        rating=data.get("rating"),
        durationMins=data.get("durationMins", 0),
        year=data.get("year", 0)
    )


def get_genre_display_name(genre: str) -> str:
    """Get display name for genre"""
    return MOVIE_GENRES.get(genre.lower(), genre.title())


def format_duration(minutes: int) -> str:
    """Format duration from minutes to hours and minutes"""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def get_movie_rating_from_mock_reviews(movie: Movie) -> str:
    """Get movie rating from mock reviews"""

    ratings = []

    for review in MOCK_REVIEWS:
        if review["movie_id"] == movie.id:
            ratings.append(review["rating"])

    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        return f"{avg_rating:.1f}/5.0"

    return "Not Rated"


def format_movie_details(movie: Movie) -> str:
    """Format movie details as a readable string"""

    details = f"🎞️ {movie.title}\n"
    details += f"🏷️ Genre: {get_genre_display_name(movie.genre)}\n"

    if movie.rating:
        details += f"⭐ Rating:  {get_movie_rating_from_mock_reviews(movie)}\n"

    if movie.synopsis:
        details += f"\n📝 Synopsis: {movie.synopsis}\n"

    if movie.durationMins:
        details += f"⏳ Duration: {format_duration(movie.durationMins)}\n"

    return details
