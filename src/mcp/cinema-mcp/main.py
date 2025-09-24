"""
Cinema MCP Server - Discover and book movie showings.

To run this server:
    uv run mcp dev main.py

Provides information about current movie showings, seat availability, 
and reservation capabilities.
"""

from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from cinema_service import (
    get_current_movies_data,
    get_movie_details_data,
    search_movies_data
)

mcp = FastMCP("Cinema", port=8009)

# Tools
@mcp.tool()
def get_current_movies() -> Dict[str, Any]:
    """Get all currently playing movies with their showtimes and availability
    
    Returns:
        List of all movies currently being shown with details including:
        - Movie title, description, and basic info
        - Showtimes and theater room assignments  
        - Seat availability and pricing
        - Genre, rating, and duration
        - Cast and director information
    """
    return get_current_movies_data()

@mcp.tool()
def get_movie_details(
    title: str,
    date: str,
    time: str,
    room: str
) -> Dict[str, Any]:
    """Get detailed information about a specific movie showing
    
    Args:
        title: Exact movie title
        date: Date in YYYY-MM-DD format (e.g., "2025-09-25")
        time: Time in HH:MM format (e.g., "19:30")
        room: Room identifier (e.g., "theater_a", "theater_b", "theater_c", "imax")
        
    Returns:
        Detailed movie information including plot, cast, theater details, and availability
        Use search_movies first to find the exact title, date, time, and room values needed
    """
    return get_movie_details_data(title, date, time, room)

@mcp.tool()
def search_movies(
    title: Optional[str] = None,
    genre: Optional[str] = None,
    date: Optional[str] = None,
    room: Optional[str] = None, 
    available_seats_min: Optional[int] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """Search for movie presentations with optional filters
    
    Args:
        title: Filter by movie title (partial match, case-insensitive)
        genre: Filter by movie genre (action, comedy, drama, horror, sci-fi, romance, thriller, animation, documentary, family)
        date: Filter by date in YYYY-MM-DD format (e.g., "2025-09-25")
        room: Filter by cinema room (theater_a, theater_b, theater_c, imax)
        available_seats_min: Minimum number of available seats required
        limit: Maximum number of results to return (default: 20, max: 100)
        
    Returns:
        Filtered list of movie presentations matching the search criteria
    """
    return search_movies_data(title, genre, date, room, available_seats_min, limit)

# Resources
@mcp.resource("movie://{title}/{date}/{time}/{room}")
def get_movie_resource(title: str, date: str, time: str, room: str) -> str:
    """Get movie details as a formatted resource"""
    result = get_movie_details_data(title, date, time, room)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    movie = result["movie"]
    showing = result["showing_details"]
    
    return f"""
🎬 {movie['title']} ({movie['rating']})

📅 Showing: {movie['date']} at {movie['time']}
🏛️ Theater: {showing['room']} ({showing['room_type']})
🎭 Genre: {movie['genre']} | ⏱️ Duration: {movie['duration_minutes']} minutes
🎬 Director: {movie['director']}
⭐ Cast: {', '.join(movie['cast'])}

💺 Seating:
- Total Seats: {showing['seats_total']}
- Available: {showing['seats_remaining']}
- Booked: {showing['seats_booked']}
- Occupancy: {showing['occupancy_percentage']}%
- Price: ${showing['price_per_seat']:.2f} per seat

📝 Description:
{movie['description']}

{"🚫 SOLD OUT" if showing['is_sold_out'] else "✅ Tickets Available"}
"""

@mcp.resource("cinema://current-movies")
def get_current_movies_resource() -> str:
    """Get current movies as a formatted resource"""
    result = get_current_movies_data()
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    output = f"🎬 {result['cinema_name']} - Current Movies\n"
    output += f"📊 Total Movies Playing: {result['total_movies']}\n\n"
    
    for i, movie in enumerate(result['movies'], 1):
        output += f"{i}. {movie['title']} ({movie['rating']})\n"
        output += f"   📅 {movie['date']} at {movie['time']} | 🏛️ {movie['room']}\n"
        output += f"   🎭 {movie['genre']} | ⏱️ {movie['duration_minutes']}min | 💰 ${movie['price_per_seat']:.2f}\n"
        output += f"   💺 {movie['seats_remaining']}/{movie['seats_total']} seats available"
        
        if movie['is_sold_out']:
            output += " 🚫 SOLD OUT"
        else:
            output += f" ({movie['occupancy_percentage']}% full)"
        
        output += "\n\n"
    
    return output

if __name__ == "__main__":
    mcp.run()