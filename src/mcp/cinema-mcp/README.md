# Cinema MCP Server

A Model Context Protocol (MCP) server for managing movie theater showings and reservations.

## Features

- **Current Movies**: View all currently playing movies with showtimes
- **Movie Details**: Get detailed information about specific movie showings
- **Search Movies**: Filter movies by genre, date, theater room, or seat availability
- **Daily Schedule**: View all movies for a specific date

## Quick Start

1. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

2. Run the MCP server:
   ```bash
   uv run mcp dev main.py
   ```

3. The server will start on port 8009

## Available Tools

### `get_current_movies()`
Returns all currently playing movies with complete details including showtimes, seat availability, and pricing.

### `get_movie_details(movie_id: str)`
Get detailed information about a specific movie showing including cast, director, and theater details.

### `search_movies(genre, date, room, available_seats_min, limit)`
Search and filter movies by various criteria:
- **genre**: action, comedy, drama, horror, sci-fi, romance, thriller, animation, documentary, family
- **date**: YYYY-MM-DD format
- **room**: theater_a, theater_b, theater_c, imax
- **available_seats_min**: minimum seats required
- **limit**: maximum results (default: 20)

### `get_movies_by_date(date: str)`
Get all movie showings for a specific date, sorted by showtime.

## Available Resources

- `movie://{movie_id}` - Formatted movie details
- `cinema://current-movies` - Current movies overview

## Mock Data

The server uses `MOCK_MOVIE_PRESENTATIONS` from `config.py` with sample movies including:
- Galactic Adventures (Sci-Fi)
- The Midnight Mystery (Thriller)  
- Laugh Out Loud (Comedy)
- Dragon's Heart (Animation)
- City of Shadows (Drama)
- Ocean's Edge (Documentary/IMAX)
- Love in Paris (Romance)
- Nightmare Manor (Horror)

## Configuration

Edit `config.py` to modify:
- Theater room configurations
- Movie genres and ratings
- Mock movie data
- Pricing and capacity settings

## Usage Examples

```python
# Get all current movies
movies = get_current_movies()

# Search for action movies with at least 50 seats available
action_movies = search_movies(genre="action", available_seats_min=50)

# Get movies playing tomorrow
tomorrow_movies = get_movies_by_date("2025-09-26")

# Get details for a specific movie
movie_details = get_movie_details("movie_001")
```