"""
Weather MCP Server - Get weather information for any location.

To run this server:
    uv run mcp dev main.py

Uses Open-Meteo free weather API - no API key required!
https://open-meteo.com/
"""

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from weather_service import (
    get_current_weather_data, 
    get_weather_forecast_data,
    format_weather_resource,
    get_weather_summary_prompt
)


mcp = FastMCP("Weather")

# tools
@mcp.tool()
def get_current_weather(location: str) -> Dict[str, Any]:
    """Get current weather information for a specific location
    
    Args:
        location: City name or place name (e.g., "London", "New York", "Tokyo")
        
    Returns:
        CurrentWeather object as dictionary or error dict
    """
    return get_current_weather_data(location)

@mcp.tool()
def get_weather_forecast(location: str, days: int = 7) -> Dict[str, Any]:
    """Get weather forecast for a specific location
    
    Args:
        location: City name or place name (e.g., "London", "New York", "Tokyo")
        days: Number of days for forecast (1-16, default is 7)
        
    Returns:
        WeatherForecast object as dictionary or error dict
    """
    return get_weather_forecast_data(location, days)

# Weather resource and prompts
@mcp.resource("weather://{location}")
def get_weather_resource(location: str) -> str:
    """Get weather information as a formatted resource"""
    return format_weather_resource(location)

@mcp.prompt()
def weather_summary_prompt(location: str, include_forecast: bool = False) -> str:
    """Generate a prompt for weather summary"""
    return get_weather_summary_prompt(location, include_forecast)

if __name__ == "__main__":
    mcp.run()