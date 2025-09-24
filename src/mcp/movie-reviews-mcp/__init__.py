"""
Movie Reviews MCP Package - Discover list of movies and reviews
"""

from movie_service import (
    get_movie_details_data,
    search_movies_data,
    get_random_famous_movie_data,
    get_movie_reviews_data,
    format_movie_resource
)
from models import (
    Movie, MovieReview, MovieList
)
from utils import (
    get_movie_by_id, search_movies, parse_movie_data,
    format_attraction_name, get_category_display_name, generate_booking_id,
    validate_visit_date, validate_email, format_attraction_details
)

__version__ = "1.0.0"
__all__ = [
    # Service functions
    "parse_movie_data",
    "search_movies_data",
    "get_random_famous_movie_data",
    "get_movie_details_data",
    "get_movie_reviews_data",
    "format_movie_resource",
    # Models
    "Movie",
    "MovieList",
    "MovieReview",
    # Utilities
    "get_movie_by_id",
    "search_attractions",
    "parse_attraction_data",
    "format_attraction_name",
    "get_category_display_name",
    "generate_booking_id",
    "validate_visit_date",
    "validate_email",
    "format_attraction_details"
]
