get_movie_details_data# Movie Reviews MCP Server

A Model Context Protocol (MCP) server for discovering movie list and reviews using the Movie Reviews API.

## Features

🏛️ **Movie Discovery**
- Search movies by title and genre
- Get detailed movie information
- Discover a random famous movie
- Get a list of reviews from a movie

## Installation

```bash
## cd to movie reviews mcp project
cd src/mcp/movie-reviews-mcp
```

```bash
# Install dependencies
uv sync
```

### Running the Server

```bash
uv run mcp dev main.py
```

```bash
# use this when wanting to consume within an agent
uv run main.py
```

### Available Tools

#### 1. Get Movie Details
```python
get_movie_details_data(movie_id: int)
```
Get comprehensive information about a specific movie and its reviews.

#### 2. Search Movies
```python
search_movies_data(title: str = None, genre: str = None, limit: int = 20)
```
Search for movies by title and genre.

#### 3. Random Famous Movie
```python
get_random_famous_movie_data(region: str = "famous")
```
Get a random famous movie.

### Resources

Access attraction data as resources:
- `movie://{movie_id}` - Specific movie details
- `movies://search/{location}` - movies by location
- `movies://genre/{genre}` - movies by category

### Prompts

- `movie_booking_prompt(title, genre)` - Booking assistance
- `travel_planning_prompt(title, days)` - Multi-day itinerary planning
- `movie_comparison_prompt(movie_ids)` - Compare multiple movies

## Example Usage

```python
# Search for historical movies in Rome
search_movies(title="Inception", genre="sci-fi", limit=10)

# Get details about the movie Inception (example ID: 1)
get_movie_details(1)

# Get formatted search results
search_and_format_movies(location="Paris", category="cultural", limit=5)
```

## Project Structure

```
src/mcp/attractions-mcp/
├── __init__.py          # Package exports
├── main.py              # MCP server setup and tools
├── models.py            # Data classes (Movie, Booking, etc.)
├── config.py            # API URLs and constants
├── utils.py             # Helper functions and validation
├── movie_service.py     # Core business logic
├── pyproject.toml       # Dependencies
└── README.md            # This file
```

## Development

The codebase follows a modular structure similar to the weather-mcp:
- **Models**: Data structures for movies and reviews
- **Config**: Mock Data for movies
- **Utils**: Helper functions for API calls and validation
- **Service**: Business logic and data processing
- **Main**: MCP server orchestration
