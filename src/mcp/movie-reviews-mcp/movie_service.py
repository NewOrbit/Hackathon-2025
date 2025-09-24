"""
Movies service with MCP tools and API logic.
"""

from typing import Dict, Any, List
from dataclasses import asdict
from datetime import datetime

from config import DEFAULT_SEARCH_LIMIT, MOVIE_GENRES
from models import (
    Movie, MovieReview, MoviesList
)
from utils import (
    get_genre_display_name,
    parse_movie_data,
    search_movies,
    get_random_famous_movie
)


def search_movies_data(
    genre: str = None,
    limit: int = DEFAULT_SEARCH_LIMIT
) -> Dict[str, Any]:
    """Search for movies with filters

    Args:
        genre: Genre of movies (e.g., "action", "comedy", "drama")
        limit: Maximum number of results (default: 20, max: 100)

    Returns:
        MoviesList object as dictionary or error dict
    """
    try:
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 1

        data = search_movies( genre, limit)
        if not data:
            return {"error": "No movies found matching the criteria"}

        movies = []
        if "movies" in data:
            for item in data["movies"]:
                movie = parse_movie_data(item)
                movies.append(movie)

        movies_list = MoviesList(
            genre=get_genre_display_name(genre) if genre else "All Genres",
            total_count=data.get("total", len(movies)),
            movies=movies
        )

        return asdict(movies_list)

    except Exception as e:
        return {"error": f"Failed to search movies: {str(e)}"}


def get_random_movie_data() -> Dict[str, Any]:
    """Get a random movie


    Returns:
        Movie object as dictionary or error dict
    """
    try:
        data = get_random_famous_movie()

        if not data:
            return {"error": f"No random movie found"}

        movie = parse_movie_data(data)
        return asdict(movie)

    except Exception as e:
        return {"error": f"Failed to get random movie: {str(e)}"}


def get_movie_genres_data() -> str:
    """Get list of available movie genres as formatted string

    Returns:
        Formatted string with genre codes and display names
    """
    try:
        result = "🏛️ **Available Movie Genres**\n\n"
        result += f"Total Genres: {len(MOVIE_GENRES)}\n\n"

        for code, display_name in MOVIE_GENRES.items():
            result += f"• **{code}**: {display_name}\n"

        result += "\n*Use these genre codes when searching for movies.*"
        return result

    except Exception as e:
        return f"Error: Failed to get categories: {str(e)}"


def format_search_results(search_data: Dict[str, Any]) -> str:
    """Format search results as a readable string"""
    if "error" in search_data:
        return f"Error: {search_data['error']}"

    movies = search_data.get('movies', [])
    if not movies:
        return "No movies found matching your criteria."

    result = f"🎯 Found {search_data.get('total_count', len(movies))} movies"
    if search_data.get('genre') != "All Genres":
        result += f" ({search_data['genre']})"
    result += ":\n\n"

    for i, movie_data in enumerate(movies[:10], 1):  # Show first 10
        movie = parse_movie_data(movie_data)

        result += f"{i}. 🎬 **{movie.title}**\n"
        result += f"   🏷️ {get_genre_display_name(movie.genre)}\n"

        if movie.rating:
            result += f"   ⭐ {movie.rating}/5.0\n"
        if movie.durationMins:
            result += f"   ⏳ {movie.durationMins}\n"

        result += "\n"

    if len(movies) > 10:
        result += f"... and {len(movies) - 10} more movies\n"

    return result

