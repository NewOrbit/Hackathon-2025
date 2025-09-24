"""
Movies service with MCP tools and API logic.
"""

from typing import Dict, Any, List
from dataclasses import asdict
from datetime import datetime

from config import DEFAULT_SEARCH_LIMIT, MOVIE_GENRES, MOCK_REVIEWS

from models import (
    Movie, MovieReview, MovieReviewList, MoviesList
)
from utils import (
    format_movie_details,
    get_genre_display_name,
    get_movie_by_id,
    parse_movie_data,
    search_movies,
    get_random_famous_movie
)


def search_movies_data(
    title: str = None,
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

        data = search_movies(title, genre, limit)
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

def get_movie_details_data(movie_id: int):
    """Get details for a specific movie

    Args:
        movie_id: ID of the movie
    Returns:
        Movie object as dictionary or error dict
    """
    try:
        movie_data = get_movie_by_id(movie_id)
        if not movie_data:
            return {"error": f"Movie with ID {movie_id} not found"}

        movie = parse_movie_data(asdict(movie_data))
        return {"movie": asdict(movie)}

    except Exception as e:
        return {"error": f"Failed to get movie details: {str(e)}"}

def format_movie_resource(movie_id: int) -> str:
    """Get movie information as a formatted resource"""
    data = get_movie_details_data(movie_id)
    if "error" in data:
        return f"Error: {data['error']}"

    movie_data = data['movie']
    movie = parse_movie_data(movie_data)

    return format_movie_details(movie)


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

def get_movie_reviews_data(movie_id: int) -> MovieReviewList:
    """Get reviews for a specific movie

    Args:
        movie_id: ID of the movie
    Returns:
        MovieReviewList object as dictionary or error dict
    """

    movie = get_movie_by_id(movie_id)

    reviews = [review for review in MOCK_REVIEWS if review.movie_id == movie_id]
    review_list = MovieReviewList(
        movie=movie,
        total_count=len(reviews),
        reviews=reviews,
        avg_rating=(sum(r.rating for r in reviews) / len(reviews)) if reviews else None
    )
    return review_list

def format_review_list(review_list: MovieReviewList) -> str:
    """Format movie review list as a readable string"""
    if not review_list.reviews:
        return f"No reviews found for movie: {review_list.movie.title}"

    result = f"📝 Reviews for **{review_list.movie.title}**\n"
    result += f"Total Reviews: {review_list.total_count}\n"
    if review_list.avg_rating:
        result += f"Average Rating: {review_list.avg_rating:.1f}/5.0\n"
    result += "\n"

    for i, review in enumerate(review_list.reviews, 1):
        review_date = review.reviewDate.strftime("%Y-%m-%d")
        result += f"{i}. ⭐ {review.rating}/5.0 on {review_date} by {review.reviewer}\n"
        result += f"   \"{review.comment}\"\n\n"

    return result.strip()