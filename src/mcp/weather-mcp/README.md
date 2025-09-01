# Weather MCP Server

A Model Context Protocol (MCP) server for getting comprehensive weather information for any location worldwide using the Open-Meteo API.

## Features

🌤️ **Current Weather**
- Real-time weather conditions
- Temperature with "feels like" values
- Wind speed and direction
- Humidity and pressure data
- Precipitation information

🌦️ **Weather Forecasts**
- 1-16 day forecasts
- Daily temperature ranges (min/max)
- Apparent temperature forecasts
- Precipitation totals and breakdown
- Wind conditions and gusts
- Weather condition descriptions

🌍 **Global Coverage**
- Worldwide location support
- Automatic coordinate resolution
- Timezone-aware data
- No API key required

## Installation

```bash
# Install dependencies
uv sync

# Or install manually
uv add "mcp[cli]>=1.13.1" requests
```

## Usage

### Running the Server

```bash
uv run mcp dev main.py
```

### Available Tools

#### 1. Get Current Weather
```python
get_current_weather(location: str)
```
Get comprehensive current weather information including temperature, conditions, wind, humidity, and pressure.

**Example:**
```python
get_current_weather("London")
get_current_weather("New York")
get_current_weather("Tokyo")
```

#### 2. Get Weather Forecast
```python
get_weather_forecast(location: str, days: int = 7)
```
Get detailed weather forecast for 1-16 days with daily breakdowns.

**Example:**
```python
get_weather_forecast("Paris", days=5)
get_weather_forecast("Sydney", days=14)
```

### Resources

Access weather data as resources:
- `weather://{location}` - Current weather formatted as text resource

**Example:**
```
weather://London
weather://San Francisco
```

### Prompts

#### 1. Weather Summary Prompt
```python
weather_summary_prompt(location: str, include_forecast: bool = False)
```
Generate prompts for weather summaries with practical advice.

**Examples:**
- `weather_summary_prompt("London")` - Current conditions with advice
- `weather_summary_prompt("Tokyo", include_forecast=True)` - 3-day forecast with activities

## Data Structure

### Current Weather Response
```json
{
    "location": "London, England, United Kingdom",
    "coordinates": {"lat": 51.5074, "lon": -0.1278},
    "temperature": {
        "current": 18.5,
        "feels_like": 17.2,
        "unit": "°C"
    },
    "weather": {
        "description": "Partly cloudy",
        "code": 2
    },
    "wind": {
        "speed": 12.0,
        "direction": 240.0,
        "unit": "km/h"
    },
    "humidity": 65,
    "pressure": 1013.2,
    "precipitation": 0,
    "timezone": "Europe/London",
    "timestamp": "2024-01-15T14:30"
}
```

### Forecast Response
```json
{
    "location": "Paris, Île-de-France, France",
    "coordinates": {"lat": 48.8566, "lon": 2.3522},
    "timezone": "Europe/Paris",
    "forecast_days": 7,
    "forecasts": [
        {
            "date": "2024-01-15",
            "temperature": {"min": 8.2, "max": 15.7, "unit": "°C"},
            "apparent_temperature": {"min": 6.1, "max": 14.2, "unit": "°C"},
            "weather": {"description": "Light rain", "code": 61},
            "precipitation": {
                "total": 2.4,
                "rain": 2.4,
                "showers": 0,
                "snow": 0,
                "hours": 3,
                "unit": "mm"
            },
            "wind": {
                "speed": 18.5,
                "direction": 225.0,
                "max_gusts": 32.1,
                "unit": "km/h"
            }
        }
    ]
}
```

## Weather Codes

The API uses WMO Weather interpretation codes:

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1-3 | Mainly clear to overcast |
| 45-48 | Fog |
| 51-57 | Drizzle (light to freezing) |
| 61-67 | Rain (slight to freezing) |
| 71-77 | Snow (slight to heavy) |
| 80-86 | Rain/snow showers |
| 95-99 | Thunderstorms |

## Example Usage

```python
# Get current weather for multiple cities
current_london = get_current_weather("London")
current_tokyo = get_current_weather("Tokyo")

# Get extended forecast
forecast_paris = get_weather_forecast("Paris", days=10)

# Quick weather check with resource
# Use: weather://Berlin
```

## Project Structure

```
src/mcp/weather-mcp/
├── __init__.py           # Package exports
├── main.py              # MCP server setup and tools
├── models.py            # Data classes (Weather, Temperature, etc.)
├── config.py            # API URLs and weather code constants
├── utils.py             # Helper functions for API calls and geocoding
├── weather_service.py   # Core weather logic and data processing
├── pyproject.toml       # Dependencies
├── uv.lock             # Locked dependencies
└── README.md           # This file
```

## API Integration

This MCP integrates with the **Open-Meteo API**, providing:
- **Free access** - No API key required
- **Global coverage** - Weather data worldwide
- **Reliable data** - Professional weather service
- **Multiple endpoints** - Current weather, forecasts, and geocoding

**API Documentation**: https://open-meteo.com/

## Features by Module

### Models (`models.py`)
- `Coordinates` - Latitude/longitude pairs
- `Location` - Geographic location with timezone
- `Temperature` - Current, min, max, feels-like values
- `Weather` - Condition descriptions and codes
- `Wind` - Speed, direction, gusts
- `Precipitation` - Rain, snow, showers breakdown
- `CurrentWeather` - Complete current weather snapshot
- `ForecastDay` - Single day forecast data
- `WeatherForecast` - Multi-day forecast collection

### Configuration (`config.py`)
- API base URLs for weather and geocoding
- Complete WMO weather code mappings
- Standard units and formats

### Utilities (`utils.py`)
- `make_api_request()` - HTTP request handling with timeouts
- `get_coordinates()` - Location name to coordinates conversion
- `format_location_name()` - Pretty location formatting
- `get_weather_description()` - Weather code to description mapping

### Weather Service (`weather_service.py`)
- `get_current_weather_data()` - Current conditions processing
- `get_weather_forecast_data()` - Forecast data processing
- `format_weather_resource()` - Resource text formatting
- `get_weather_summary_prompt()` - Smart prompt generation

## Development

The codebase follows a modular structure with clear separation of concerns:
- **Models**: Data structures and type definitions
- **Config**: Constants and API configuration
- **Utils**: Reusable helper functions
- **Service**: Core business logic
- **Main**: MCP server orchestration