"""
Tourist Attractions MCP Server - Discover and book attractions worldwide.

To run this server:
    uv run mcp dev main.py

Uses World Tourist Attractions API to provide information about tourist attractions
and booking capabilities.
"""

from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from movie_service import (
    get_movie_genres_data,
    get_random_movie_data,
    parse_movie_data,
    search_movies_data,
    get_movie_details_data,
    get_movie_reviews_data,
    format_movie_resource,
    format_search_results,
    format_review_list
)

mcp = FastMCP("MovieReviews", port=8011)

# tools
@mcp.tool()
def get_movie_details(movie_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific movie

    Args:
        movie_id: Unique ID of the movie

    Returns:
        MovieDetails object as dictionary with movie info, reviews, and related movies
    """
    return get_movie_details_data(movie_id)

@mcp.tool()
def search_movies(
    genre: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """Search for movies with optional filters

    Args:
        genre: Genre filter - "action", "comedy", "drama", etc.
        limit: Maximum number of results (1-100, default: 20)

    Returns:
        MoviesList object as dictionary with matching movies
    """
    return search_movies_data(genre, limit)

@mcp.tool()
def get_random_movie() -> Dict[str, Any]:
    """Get a random movie for inspiration

    Args:
        genre: Genre type - "famous" for world famous movies, "india" for Indian movies

    Returns:
        Movie object as dictionary with random movie details
    """
    return get_random_movie_data()



@mcp.tool()
def search_and_format_movies(
    genre: Optional[str] = None,
    limit: int = 10
) -> str:
    """Search for movies and return formatted results for easy reading

    Args:
        genre: Genre filter (e.g., "action", "comedy", "drama")
        limit: Maximum number of results (1-20, default: 10)

    Returns:
        Formatted string with movie search results
    """
    if limit > 20:
        limit = 20

    search_data = search_movies_data(genre, limit)
    return format_search_results(search_data)


@mcp.tool()
def get_movie_reviews_by_title(title: string) -> str:
    """Get reviews for a movie by its title and return formatted results

    Args:
        title: Title of the movie

    Returns:
        Formatted string with movie reviews
    """
    # First, search for the movie by title to get its ID
    search_data = search_movies(title=title, limit=1)
    if not search_data or "movies" not in search_data or not search_data["movies"]:
        return f"No movie found with title '{title}'."

    movie_id = search_data["movies"][0]["id"]
    reviews_data = get_movie_reviews_data(movie_id)
    return format_review_list(reviews_data)

# resources
@mcp.resource("movie://{movie_id}")
def get_movie_resource(movie_id: int) -> str:
    """Get movie information as a formatted resource"""
    return format_movie_resource(movie_id)

@mcp.resource("movies://genre/{genre}")
def get_movies_by_genre_resource(genre: str) -> str:
    """Get movies by genre as a formatted resource"""
    search_data = search_movies_data(genre=genre, limit=10)
    return format_search_results(search_data)

@mcp.resource("movies://genre")
def get_movies() -> str:
    """Get 10 movies by formatted resource"""
    search_data = search_movies_data(limit=10)
    return format_search_results(search_data)

@mcp.resource("movies://genres")
def get_movie_genres_resource() -> str:
    """Get list of available movie genres as a formatted resource"""
    return get_movie_genres_data()


# prompts

# @mcp.prompt()
# def travel_planning_prompt(location: str, days: int = 3) -> str:
#     """Generate a prompt for travel planning with attractions"""
#     return f"""Please help plan a {days}-day itinerary for {location}, including:
# 1. Top must-see attractions and landmarks
# 2. Best time to visit each attraction
# 3. Recommended booking strategies and timing
# 4. Transportation between attractions
# 5. Estimated costs and budgeting tips
# 6. Cultural considerations and local customs
# 7. Alternative attractions if main ones are crowded

# Focus on creating a balanced mix of historical, cultural, and recreational activities suitable for different interests."""

# @mcp.prompt()
# def attraction_comparison_prompt(attraction_ids: str) -> str:
#     """Generate a prompt for comparing multiple attractions"""
#     return f"""Please provide a detailed comparison of these attractions (IDs: {attraction_ids}), including:
# 1. Unique features and highlights of each
# 2. Best times to visit and crowd levels
# 3. Entry requirements and booking procedures
# 4. Approximate visit duration
# 5. Nearby attractions and activities
# 6. Accessibility and facilities
# 7. Value for money assessment
# 8. Personal recommendations based on different travel styles

# Help decide which attractions to prioritize based on time, budget, and interests."""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")