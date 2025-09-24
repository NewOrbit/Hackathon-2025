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
    get_movie_by_id, get_movie_by_natural_id, search_movie_presentations, get_current_movies,
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


def get_movie_details_data(
    title: str,
    date: Optional[str] = None,
    time: Optional[str] = None,
    room: Optional[str] = None
) -> Dict[str, Any]:
    """Get detailed information about a specific movie presentation
    
    Args:
        title: Movie title (partial match allowed)
        date: Date in YYYY-MM-DD format (optional, helps narrow results)
        time: Time in HH:MM or HH:MM AM/PM format (optional, helps narrow results)
        room: Room identifier like 'theater_a' or 'Theater A' (optional, helps narrow results)
        
    Returns:
        MovieShowing object as dictionary or error dict
    """
    try:
        movie_data = get_movie_by_natural_id(title, date, time, room)
        if not movie_data:
            error_msg = f"No movie found with title containing '{title}'"
            if date or time or room:
                filters = []
                if date: filters.append(f"date: {date}")
                if time: filters.append(f"time: {time}")
                if room: filters.append(f"room: {room}")
                error_msg += f" and filters: {', '.join(filters)}"
            return {"error": error_msg}
        
        movie = parse_movie_data(movie_data)
        room_info = CINEMA_ROOMS.get(movie.room, {})
        
        return {
            "movie": {
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


# In-memory storage for reservations (in production, this would be a database)
RESERVATIONS: List[MovieReservation] = []

def create_reservation_data(
    title: str,
    date: str,
    time: str,
    room: str,
    seats_count: int,
    customer_name: str,
    customer_email: str,
    customer_phone: Optional[str] = None,
    special_requests: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new movie reservation
    
    Args:
        title: Exact movie title
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format  
        room: Room identifier
        seats_count: Number of seats to reserve
        customer_name: Customer's full name
        customer_email: Customer's email address
        customer_phone: Customer's phone number (optional)
        special_requests: Any special requests (optional)
        
    Returns:
        Reservation confirmation details or error dict
    """
    try:
        # Find the movie showing
        movie_data = get_movie_by_natural_id(title, date, time, room)
        if not movie_data:
            return {"error": f"No movie found: '{title}' on {date} at {time} in {room}"}
        
        movie = parse_movie_data(movie_data)
        
        # Check seat availability
        if seats_count <= 0:
            return {"error": "Number of seats must be greater than 0"}
        
        if seats_count > movie.seats_remaining:
            return {"error": f"Not enough seats available. Only {movie.seats_remaining} seats remaining"}
        
        # Validate contact info
        if not customer_name or not customer_name.strip():
            return {"error": "Customer name is required"}
        
        if not customer_email or not customer_email.strip():
            return {"error": "Customer email is required"}
        
        # Basic email validation
        if "@" not in customer_email or "." not in customer_email:
            return {"error": "Please provide a valid email address"}
        
        # Create contact info
        contact_info = ContactInfo(
            name=customer_name.strip(),
            email=customer_email.strip().lower(),
            phone=customer_phone.strip() if customer_phone else None
        )
        
        # Parse date and time
        try:
            reservation_date = datetime.strptime(date, "%Y-%m-%d").date()
            reservation_time = datetime.strptime(time, "%H:%M").time()
        except ValueError as e:
            return {"error": f"Invalid date or time format: {str(e)}"}
        
        # Create reservation
        reservation = MovieReservation(
            movie_title=title,
            movie_date=reservation_date,
            movie_time=reservation_time,
            room=room,
            seats_reserved=seats_count,
            contact_info=contact_info,
            reservation_datetime=datetime.now(),
            status="confirmed",
            special_requests=special_requests.strip() if special_requests else None
        )
        
        # Add to storage
        RESERVATIONS.append(reservation)
        
        # Update movie booking count (simulate booking the seats)
        movie_data["seats_booked"] = movie_data.get("seats_booked", 0) + seats_count
        
        # Generate confirmation
        room_name = CINEMA_ROOMS.get(room, {}).get("name", room)
        genre_name = MOVIE_GENRES.get(movie.genre, movie.genre)
        
        return {
            "confirmation": {
                "reservation_id": len(RESERVATIONS),  # Simple ID based on list length
                "status": "confirmed",
                "reservation_datetime": reservation.reservation_datetime.isoformat()
            },
            "movie_details": {
                "title": title,
                "date": date,
                "time": time,
                "room": room_name,
                "genre": genre_name,
                "duration_minutes": movie.duration_minutes
            },
            "booking_details": {
                "seats_reserved": seats_count,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "customer_phone": customer_phone,
                "special_requests": special_requests
            },
            "pricing": {
                "price_per_seat": movie_data.get("price_per_seat", 0),
                "total_price": movie_data.get("price_per_seat", 0) * seats_count
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to create reservation: {str(e)}"}


def get_customer_reservations_data(customer_email: str) -> Dict[str, Any]:
    """Get all reservations for a customer by email
    
    Args:
        customer_email: Customer's email address
        
    Returns:
        List of customer's reservations or error dict
    """
    try:
        if not customer_email or not customer_email.strip():
            return {"error": "Customer email is required"}
        
        email = customer_email.strip().lower()
        customer_reservations = [
            res for res in RESERVATIONS 
            if res.customer_email.lower() == email
        ]
        
        if not customer_reservations:
            return {"error": f"No reservations found for {customer_email}"}
        
        reservations_list = []
        for i, reservation in enumerate(customer_reservations, 1):
            room_name = CINEMA_ROOMS.get(reservation.room, {}).get("name", reservation.room)
            
            reservations_list.append({
                "reservation_number": i,
                "movie_title": reservation.movie_title,
                "date": reservation.movie_date.isoformat(),
                "time": reservation.movie_time.strftime("%H:%M"),
                "room": room_name,
                "seats_reserved": reservation.seats_reserved,
                "status": reservation.status,
                "reservation_made": reservation.reservation_datetime.isoformat(),
                "special_requests": reservation.special_requests
            })
        
        return {
            "customer_email": customer_email,
            "total_reservations": len(reservations_list),
            "reservations": reservations_list
        }
        
    except Exception as e:
        return {"error": f"Failed to get customer reservations: {str(e)}"}


def cancel_reservation_data(
    customer_email: str,
    title: str,
    date: str,
    time: str,
    room: str
) -> Dict[str, Any]:
    """Cancel a reservation
    
    Args:
        customer_email: Customer's email address
        title: Movie title
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        room: Room identifier
        
    Returns:
        Cancellation confirmation or error dict
    """
    try:
        if not customer_email or not customer_email.strip():
            return {"error": "Customer email is required"}
        
        email = customer_email.strip().lower()
        
        # Parse date and time for comparison
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            target_time = datetime.strptime(time, "%H:%M").time()
        except ValueError as e:
            return {"error": f"Invalid date or time format: {str(e)}"}
        
        # Find the reservation
        reservation_to_cancel = None
        for reservation in RESERVATIONS:
            if (reservation.customer_email.lower() == email and 
                reservation.movie_title.lower() == title.lower() and
                reservation.movie_date == target_date and
                reservation.movie_time == target_time and
                reservation.room.lower() == room.lower() and
                reservation.status == "confirmed"):
                reservation_to_cancel = reservation
                break
        
        if not reservation_to_cancel:
            return {"error": f"No confirmed reservation found for {customer_email} for '{title}' on {date} at {time} in {room}"}
        
        # Cancel the reservation
        reservation_to_cancel.status = "cancelled"
        
        # Free up the seats (simulate returning seats to availability)
        movie_data = get_movie_by_natural_id(title, date, time, room)
        if movie_data:
            movie_data["seats_booked"] = max(0, movie_data.get("seats_booked", 0) - reservation_to_cancel.seats_reserved)
        
        room_name = CINEMA_ROOMS.get(room, {}).get("name", room)
        
        return {
            "cancellation_confirmed": True,
            "cancelled_reservation": {
                "movie_title": title,
                "date": date,
                "time": time,
                "room": room_name,
                "seats_freed": reservation_to_cancel.seats_reserved,
                "customer_email": customer_email
            },
            "message": f"Reservation cancelled successfully. {reservation_to_cancel.seats_reserved} seats have been freed up."
        }
        
    except Exception as e:
        return {"error": f"Failed to cancel reservation: {str(e)}"}