"""
Cinema service with MCP tools and API logic.
"""

from typing import Dict, Any, List, Optional
from dataclasses import asdict
from datetime import datetime, date, time

from config import (
    MOCK_MOVIE_PRESENTATIONS, CINEMA_ROOMS, MOVIE_GENRES, 
    DEFAULT_SEARCH_LIMIT, POPULAR_MOVIES
)
from models import MovieShowing, ContactInfo, MovieReservation
from utils import (
    get_movie_by_id, search_movie_presentations, get_current_movies,
    get_movies_by_date, search_movies_by_title, format_movie_details, parse_movie_data
)


def get_current_movies_data() -> Dict[str, Any]:
    """Get all currently playing movies
    
    Returns:
        List of currently playing movies with their details
    """
    try:
        current_movies = get_current_movies()
        
        if not current_movies:
            return {"error": "No movies currently playing"}
        
        movies_list = []
        for movie_data in current_movies:
            movie = parse_movie_data(movie_data)
            movies_list.append({
                "id": movie_data["id"],
                "title": movie.title,
                "description": movie.description,
                "date": movie.date.isoformat(),
                "time": movie.time.strftime("%H:%M"),
                "room": CINEMA_ROOMS.get(movie.room, {}).get("name", movie.room),
                "seats_remaining": movie.seats_remaining,
                "seats_total": movie.seats_available,
                "duration_minutes": movie.duration_minutes,
                "genre": MOVIE_GENRES.get(movie.genre, movie.genre),
                "rating": movie.rating,
                "price_per_seat": movie_data.get("price_per_seat"),
                "director": movie_data.get("director"),
                "cast": movie_data.get("cast", []),
                "is_sold_out": movie.is_sold_out,
                "occupancy_percentage": round(movie.occupancy_percentage, 1)
            })
        
        return {
            "cinema_name": "MovieMagic Cinema",
            "total_movies": len(movies_list),
            "movies": movies_list
        }
        
    except Exception as e:
        return {"error": f"Failed to get current movies: {str(e)}"}


def get_movie_details_data(movie_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific movie
    
    Args:
        movie_id: Unique ID of the movie showing
        
    Returns:
        MovieShowing object as dictionary or error dict
    """
    try:
        movie_data = get_movie_by_id(movie_id)
        if not movie_data:
            return {"error": f"Movie with ID {movie_id} not found"}
        
        movie = parse_movie_data(movie_data)
        room_info = CINEMA_ROOMS.get(movie.room, {})
        
        return {
            "movie": {
                "id": movie_data["id"],
                "title": movie.title,
                "description": movie.description,
                "date": movie.date.isoformat(),
                "time": movie.time.strftime("%H:%M"),
                "duration_minutes": movie.duration_minutes,
                "genre": MOVIE_GENRES.get(movie.genre, movie.genre),
                "rating": movie.rating,
                "director": movie_data.get("director"),
                "cast": movie_data.get("cast", []),
                "poster_url": movie_data.get("poster_url")
            },
            "showing_details": {
                "room": room_info.get("name", movie.room),
                "room_type": room_info.get("type", "standard"),
                "seats_total": movie.seats_available,
                "seats_booked": movie.seats_booked,
                "seats_remaining": movie.seats_remaining,
                "is_sold_out": movie.is_sold_out,
                "occupancy_percentage": round(movie.occupancy_percentage, 1),
                "price_per_seat": movie_data.get("price_per_seat")
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to get movie details: {str(e)}"}


def search_movies_data(
    title: Optional[str] = None,
    genre: Optional[str] = None,
    date: Optional[str] = None, 
    room: Optional[str] = None,
    available_seats_min: Optional[int] = None,
    limit: int = DEFAULT_SEARCH_LIMIT
) -> Dict[str, Any]:
    """Search for movie presentations with filters
    
    Args:
        title: Movie title to search for (partial match, case-insensitive)
        genre: Movie genre filter (e.g., "action", "comedy", "drama")
        date: Date filter in YYYY-MM-DD format
        room: Cinema room filter
        available_seats_min: Minimum available seats required
        limit: Maximum number of results (default: 20, max: 100)
        
    Returns:
        Filtered list of movie presentations or error dict
    """
    try:
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 1
        
        # Convert date string to date object if provided
        date_filter = None
        if date:
            try:
                date_filter = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        movies = search_movie_presentations(
            title=title,
            genre=genre,
            date=date_filter,
            room=room,
            available_seats_min=available_seats_min,
            limit=limit
        )
        
        if not movies:
            return {"error": "No movies found matching the criteria"}
        
        movies_list = []
        for movie_data in movies:
            movie = parse_movie_data(movie_data)
            movies_list.append({
                "id": movie_data["id"],
                "title": movie.title,
                "date": movie.date.isoformat(),
                "time": movie.time.strftime("%H:%M"),
                "room": CINEMA_ROOMS.get(movie.room, {}).get("name", movie.room),
                "genre": MOVIE_GENRES.get(movie.genre, movie.genre),
                "rating": movie.rating,
                "seats_remaining": movie.seats_remaining,
                "price_per_seat": movie_data.get("price_per_seat"),
                "is_sold_out": movie.is_sold_out
            })
        
        # Build filter summary
        filters_applied = []
        if title:
            filters_applied.append(f"Title: {title}")
        if genre:
            filters_applied.append(f"Genre: {MOVIE_GENRES.get(genre, genre)}")
        if date:
            filters_applied.append(f"Date: {date}")
        if room:
            filters_applied.append(f"Room: {CINEMA_ROOMS.get(room, {}).get('name', room)}")
        if available_seats_min:
            filters_applied.append(f"Min available seats: {available_seats_min}")
        
        return {
            "search_criteria": filters_applied if filters_applied else ["No filters applied"],
            "total_found": len(movies_list),
            "movies": movies_list
        }
        
    except Exception as e:
        return {"error": f"Failed to search movies: {str(e)}"}


def get_movies_by_date_data(date: str) -> Dict[str, Any]:
    """Get all movies playing on a specific date
    
    Args:
        date: Date in YYYY-MM-DD format
        
    Returns:
        List of movies for the specified date
    """
    try:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        movies = get_movies_by_date(target_date)
        
        if not movies:
            return {"error": f"No movies scheduled for {date}"}
        
        movies_list = []
        for movie_data in movies:
            movie = parse_movie_data(movie_data)
            movies_list.append({
                "id": movie_data["id"],
                "title": movie.title,
                "time": movie.time.strftime("%H:%M"),
                "room": CINEMA_ROOMS.get(movie.room, {}).get("name", movie.room),
                "genre": MOVIE_GENRES.get(movie.genre, movie.genre),
                "duration_minutes": movie.duration_minutes,
                "seats_remaining": movie.seats_remaining,
                "price_per_seat": movie_data.get("price_per_seat"),
                "is_sold_out": movie.is_sold_out
            })
        
        # Sort by time
        movies_list.sort(key=lambda x: x["time"])
        
        return {
            "date": date,
            "total_showings": len(movies_list),
            "movies": movies_list
        }
        
    except Exception as e:
        return {"error": f"Failed to get movies for date: {str(e)}"}


def search_movies_by_title_data(title: str) -> Dict[str, Any]:
    """Search for movies by title only
    
    Args:
        title: Movie title to search for (partial match, case-insensitive)
        
    Returns:
        List of movies matching the title search
    """
    try:
        if not title or not title.strip():
            return {"error": "Title is required for search"}
        
        movies = search_movies_by_title(title.strip())
        
        if not movies:
            return {"error": f"No movies found with title containing '{title}'"}
        
        movies_list = []
        for movie_data in movies:
            movie = parse_movie_data(movie_data)
            movies_list.append({
                "id": movie_data["id"],
                "title": movie.title,
                "date": movie.date.isoformat(),
                "time": movie.time.strftime("%H:%M"),
                "room": CINEMA_ROOMS.get(movie.room, {}).get("name", movie.room),
                "genre": MOVIE_GENRES.get(movie.genre, movie.genre),
                "rating": movie.rating,
                "seats_remaining": movie.seats_remaining,
                "price_per_seat": movie_data.get("price_per_seat"),
                "director": movie_data.get("director"),
                "is_sold_out": movie.is_sold_out
            })
        
        return {
            "search_title": title,
            "total_found": len(movies_list),
            "movies": movies_list
        }
        
    except Exception as e:
        return {"error": f"Failed to search movies by title: {str(e)}"}