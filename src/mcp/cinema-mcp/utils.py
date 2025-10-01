"""
Utility functions for cinema operations.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, date, time

from config import MOCK_MOVIE_PRESENTATIONS, CINEMA_ROOMS, MOVIE_GENRES
from models import MovieShowing


def get_movie_by_id(movie_id: str) -> Optional[Dict[str, Any]]:
    """Get movie details by ID from mock data"""
    for movie in MOCK_MOVIE_PRESENTATIONS:
        if movie["id"] == movie_id:
            return movie
    return None


def get_current_movies() -> List[Dict[str, Any]]:
    """Get all currently playing movies from mock data"""
    today = date.today()
    current_movies = []
    
    for movie in MOCK_MOVIE_PRESENTATIONS:
        # For demo purposes, show movies from today and next few days
        if movie["date"] >= today:
            current_movies.append(movie)
    
    return current_movies


def get_movies_by_date(target_date: date) -> List[Dict[str, Any]]:
    """Get all movies playing on a specific date"""
    movies_on_date = []
    
    for movie in MOCK_MOVIE_PRESENTATIONS:
        if movie["date"] == target_date:
            movies_on_date.append(movie)
    
    return movies_on_date


def search_movies_by_title(title: str) -> List[Dict[str, Any]]:
    """Search for movie presentations by title (partial match, case-insensitive)"""
    matching_movies = []
    search_title = title.lower()
    
    for movie in MOCK_MOVIE_PRESENTATIONS:
        movie_title = movie.get("title", "").lower()
        if search_title in movie_title:
            matching_movies.append(movie)
    
    return matching_movies


def get_movie_by_natural_id(
    title: str, 
    date: Optional[str] = None, 
    time: Optional[str] = None, 
    room: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Get movie by natural identifiers (title is required, others help narrow down)"""
    search_title = title.lower()
    
    # Parse date if provided
    parsed_date = None
    if date:
        try:
            from datetime import datetime
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return None
    
    # Parse time if provided  
    parsed_time = None
    if time:
        try:
            from datetime import datetime
            # Try different time formats
            for fmt in ["%H:%M", "%I:%M %p", "%I:%M%p"]:
                try:
                    parsed_time = datetime.strptime(time, fmt).time()
                    break
                except ValueError:
                    continue
        except:
            pass
    
    matches = []
    for movie in MOCK_MOVIE_PRESENTATIONS:
        # Title must match (partial, case-insensitive)
        movie_title = movie.get("title", "").lower()
        if search_title not in movie_title:
            continue
            
        # Filter by date if provided
        if parsed_date and movie.get("date") != parsed_date:
            continue
            
        # Filter by time if provided
        if parsed_time and movie.get("time") != parsed_time:
            continue
            
        # Filter by room if provided (case-insensitive)
        if room:
            movie_room = movie.get("room", "").lower()
            search_room = room.lower()
            if movie_room != search_room:
                continue
        
        matches.append(movie)
    
    # Return the first match, or None if no matches
    return matches[0] if matches else None


def search_movie_presentations(
    title: Optional[str] = None,
    genre: Optional[str] = None,
    date: Optional[date] = None,
    room: Optional[str] = None,
    available_seats_min: Optional[int] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """Search movie presentations based on various criteria"""
    filtered_presentations = []
    
    for presentation in MOCK_MOVIE_PRESENTATIONS:
        # Filter by title (partial match, case-insensitive)
        if title:
            presentation_title = presentation.get("title", "").lower()
            search_title = title.lower()
            if search_title not in presentation_title:
                continue
            
        # Filter by genre (case-insensitive)
        if genre:
            presentation_genre = presentation.get("genre", "").lower()
            search_genre = genre.lower()
            if presentation_genre != search_genre:
                continue
            
        # Filter by date
        if date and presentation.get("date") != date:
            continue
            
        # Filter by room (case-insensitive)
        if room:
            presentation_room = presentation.get("room", "").lower()
            search_room = room.lower()
            if presentation_room != search_room:
                continue
            
        # Filter by minimum available seats
        if available_seats_min:
            seats_available = presentation.get("seats_available", 0)
            seats_booked = presentation.get("seats_booked", 0)
            seats_remaining = seats_available - seats_booked
            if seats_remaining < available_seats_min:
                continue
        
        filtered_presentations.append(presentation)
        
        # Apply limit
        if len(filtered_presentations) >= limit:
            break
    
    return filtered_presentations


def parse_movie_data(movie_data: Dict[str, Any]) -> MovieShowing:
    """Parse movie data from mock data into MovieShowing object"""
    return MovieShowing(
        title=movie_data.get("title", ""),
        description=movie_data.get("description", ""),
        date=movie_data.get("date"),
        time=movie_data.get("time"),
        room=movie_data.get("room", ""),
        seats_available=movie_data.get("seats_available", 0),
        seats_booked=movie_data.get("seats_booked", 0),
        duration_minutes=movie_data.get("duration_minutes"),
        genre=movie_data.get("genre"),
        rating=movie_data.get("rating")
    )


def format_movie_details(movie: MovieShowing, movie_data: Dict[str, Any]) -> str:
    """Format movie details as a readable string"""
    room_info = CINEMA_ROOMS.get(movie.room, {})
    genre_name = MOVIE_GENRES.get(movie.genre, movie.genre) if movie.genre else "Unknown"
    
    details = f"🎬 {movie.title}\n"
    details += f"📅 Date: {movie.date.strftime('%A, %B %d, %Y')}\n"
    details += f"🕒 Time: {movie.time.strftime('%I:%M %p')}\n"
    details += f"🏛️ Theater: {room_info.get('name', movie.room)}\n"
    details += f"🎭 Genre: {genre_name}\n"
    
    if movie.rating:
        details += f"🏷️ Rating: {movie.rating}\n"
    
    if movie.duration_minutes:
        hours = movie.duration_minutes // 60
        minutes = movie.duration_minutes % 60
        if hours > 0:
            details += f"⏱️ Duration: {hours}h {minutes}m\n"
        else:
            details += f"⏱️ Duration: {minutes}m\n"
    
    details += f"💺 Seats: {movie.seats_remaining} available / {movie.seats_available} total\n"
    
    if movie.is_sold_out:
        details += f"🚫 Status: SOLD OUT\n"
    else:
        details += f"📊 Occupancy: {movie.occupancy_percentage:.1f}%\n"
    
    if movie_data.get("price_per_seat"):
        details += f"💰 Price: ${movie_data['price_per_seat']:.2f} per seat\n"
    
    if movie_data.get("director"):
        details += f"🎬 Director: {movie_data['director']}\n"
        
    if movie_data.get("cast"):
        cast_list = movie_data["cast"][:3]  # Show first 3 cast members
        details += f"⭐ Cast: {', '.join(cast_list)}\n"
    
    if movie.description:
        details += f"\n📝 Description: {movie.description}\n"
    
    return details


def format_showtime(movie_time: time) -> str:
    """Format time in a user-friendly way"""
    return movie_time.strftime("%I:%M %p").lstrip("0")


def get_room_display_name(room_key: str) -> str:
    """Get display name for cinema room"""
    room_info = CINEMA_ROOMS.get(room_key, {})
    return room_info.get("name", room_key.replace("_", " ").title())


def calculate_total_price(num_seats: int, price_per_seat: float) -> float:
    """Calculate total price for reservation"""
    return num_seats * price_per_seat


def validate_movie_date(movie_date: date) -> bool:
    """Validate that movie date is not in the past"""
    return movie_date >= date.today()


def validate_seat_availability(movie_data: Dict[str, Any], requested_seats: int) -> bool:
    """Check if enough seats are available for booking"""
    seats_available = movie_data.get("seats_available", 0)
    seats_booked = movie_data.get("seats_booked", 0)
    seats_remaining = seats_available - seats_booked
    return seats_remaining >= requested_seats


def get_popular_movies() -> List[Dict[str, Any]]:
    """Get popular movies from mock data"""
    from config import POPULAR_MOVIES
    popular = []
    
    for movie_id in POPULAR_MOVIES:
        movie_data = get_movie_by_id(movie_id)
        if movie_data:
            popular.append(movie_data)
    
    return popular


def format_movie_summary(movie_data: Dict[str, Any]) -> str:
    """Create a short summary of a movie showing"""
    movie_time = movie_data.get("time")
    room_name = get_room_display_name(movie_data.get("room", ""))
    genre_name = MOVIE_GENRES.get(movie_data.get("genre"), movie_data.get("genre", ""))
    
    seats_available = movie_data.get("seats_available", 0)
    seats_booked = movie_data.get("seats_booked", 0)
    seats_remaining = seats_available - seats_booked
    
    time_str = format_showtime(movie_time) if movie_time else "TBA"
    
    summary = f"{movie_data.get('title', 'Untitled')} - {time_str} in {room_name}"
    summary += f" | {genre_name} | {seats_remaining} seats left"
    
    if movie_data.get("rating"):
        summary += f" | Rated {movie_data['rating']}"
    
    return summary