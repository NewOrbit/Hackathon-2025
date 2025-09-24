# Tourist Attractions MCP Server

A Model Context Protocol (MCP) server for discovering and booking tourist attractions worldwide using the World Tourist Attractions API.

## Features

🏛️ **Attraction Discovery**
- Search attractions by location and category
- Get detailed attraction information
- Discover random famous attractions
- Explore world wonders

🎫 **Booking System**
- Book attraction visits
- Generate confirmation codes
- Calculate estimated costs
- Validate visit dates and requirements

🗂️ **Categories Supported**
- Historical Sites
- Natural Wonders
- Cultural Sites
- Religious Sites
- Museums
- Parks & Gardens
- Beaches & Mountains
- Architecture
- Entertainment & Adventure Sports

## Installation

```bash
## cd to attractions mcp project
cd src/mcp/attractions-mcp
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

#### 1. Get Attraction Details
```python
get_attraction_details(attraction_id: int)
```
Get comprehensive information about a specific attraction including facilities, best visiting times, and reviews.

#### 2. Search Attractions
```python
search_attractions(location: str = None, category: str = None, limit: int = 20)
```
Search for attractions with optional location and category filters.

#### 3. Random Attraction Discovery
```python
get_random_attraction(region: str = "famous")
```
Get a random attraction for inspiration. Use `region="india"` for Indian attractions.

#### 4. World Wonders
```python
get_world_wonders()
```
Get the list of world wonder attractions.

#### 5. Book Attraction
```python
book_attraction(
    attraction_id: int,
    visitor_name: str,
    email: str,
    visit_date: str,  # YYYY-MM-DD format
    num_visitors: int = 1,
    phone: str = None,
    special_requirements: str = None
)
```
Book a visit to an attraction with confirmation.

#### 6. Get Categories
```python
get_attraction_categories()
```
Get all available attraction categories for filtering.

#### 7. Search and Format
```python
search_and_format_attractions(location: str = None, category: str = None, limit: int = 10)
```
Search attractions and return nicely formatted results.

### Resources

Access attraction data as resources:
- `attraction://{attraction_id}` - Specific attraction details
- `attractions://search/{location}` - Attractions by location
- `attractions://category/{category}` - Attractions by category

### Prompts

- `attraction_booking_prompt(location, category)` - Booking assistance
- `travel_planning_prompt(location, days)` - Multi-day itinerary planning
- `attraction_comparison_prompt(attraction_ids)` - Compare multiple attractions

## Example Usage

```python
# Search for historical attractions in Rome
search_attractions(location="Rome", category="historical", limit=10)

# Get details about the Colosseum (example ID: 123)
get_attraction_details(123)

# Book a visit
book_attraction(
    attraction_id=123,
    visitor_name="John Doe",
    email="john@example.com", 
    visit_date="2024-06-15",
    num_visitors=2
)

# Get formatted search results
search_and_format_attractions(location="Paris", category="cultural", limit=5)
```

## Project Structure

```
src/mcp/attractions-mcp/
├── __init__.py           # Package exports
├── main.py              # MCP server setup and tools
├── models.py            # Data classes (Attraction, Booking, etc.)
├── config.py            # API URLs and constants
├── utils.py             # Helper functions and validation
├── attractions_service.py # Core business logic
├── pyproject.toml       # Dependencies
└── README.md           # This file
```

## Development

The codebase follows a modular structure similar to the weather-mcp:
- **Models**: Data structures for attractions and bookings
- **Config**: Mock Data for attractions
- **Utils**: Helper functions for API calls and validation
- **Service**: Business logic and data processing
- **Main**: MCP server orchestration
