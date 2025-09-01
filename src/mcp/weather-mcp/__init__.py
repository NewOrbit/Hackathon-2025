"""
Weather MCP Package - Modular weather information service.
"""


from weather_service import get_current_weather_data, get_weather_forecast_data
from models import CurrentWeather, WeatherForecast, Temperature, Weather, Wind, Precipitation
from utils import get_coordinates, format_location_name, get_weather_description

__version__ = "1.0.0"
__all__ = [
    "get_current_weather_data",
    "get_weather_forecast_data", 
    "CurrentWeather",
    "WeatherForecast",
    "Temperature",
    "Weather", 
    "Wind",
    "Precipitation",
    "get_coordinates",
    "format_location_name",
    "get_weather_description"
]
