"""
Weather service with MCP tools and API logic.
"""

from typing import Dict, Any, List
from dataclasses import asdict

from config import WEATHER_BASE_URL
from models import (
    Temperature, Weather, Wind, Precipitation, CurrentWeather, 
    ForecastDay, WeatherForecast
)
from utils import (
    make_api_request, get_coordinates, format_location_name, 
    get_weather_description
)


def get_current_weather_data(location: str) -> Dict[str, Any]:
    """Get current weather information for a specific location
    
    Args:
        location: City name or place name (e.g., "London", "New York", "Tokyo")
        
    Returns:
        CurrentWeather object as dictionary or error dict
    """
    try:
        location_obj = get_coordinates(location)
        if not location_obj:
            return {"error": f"Location '{location}' not found"}
        
        url = f"{WEATHER_BASE_URL}/forecast"
        params = {
            "latitude": location_obj.coordinates.lat, 
            "longitude": location_obj.coordinates.lon, 
            "current_weather": "true",
            "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,surface_pressure,wind_speed_10m,wind_direction_10m",
            "timezone": location_obj.timezone or "auto", 
            "forecast_days": 1
        }
        
        data = make_api_request(url, params)
        current = data["current_weather"]
        hourly = data["hourly"]
        
        temperature = Temperature(
            current=current["temperature"],
            feels_like=hourly["apparent_temperature"][0] if hourly["apparent_temperature"] else None
        )
        
        weather = Weather(
            description=get_weather_description(current["weathercode"]),
            code=current["weathercode"]
        )
        
        wind = Wind(
            speed=current["windspeed"],
            direction=current["winddirection"]
        )
        
        current_weather = CurrentWeather(
            location=format_location_name(location_obj),
            coordinates=location_obj.coordinates,
            temperature=temperature,
            weather=weather,
            wind=wind,
            humidity=hourly["relative_humidity_2m"][0] if hourly["relative_humidity_2m"] else None,
            pressure=hourly["surface_pressure"][0] if hourly["surface_pressure"] else None,
            precipitation=hourly["precipitation"][0] if hourly["precipitation"] else 0,
            timezone=location_obj.timezone,
            timestamp=current["time"]
        )
        
        # Return as dictionary for MCP compatibility
        return asdict(current_weather)
        
    except Exception as e:
        return {"error": f"Failed to get weather for {location}: {str(e)}"}


def get_weather_forecast_data(location: str, days: int = 7) -> Dict[str, Any]:
    """Get weather forecast for a specific location
    
    Args:
        location: City name or place name (e.g., "London", "New York", "Tokyo")
        days: Number of days for forecast (1-16, default is 7)
        
    Returns:
        WeatherForecast object as dictionary or error dict
    """    
    if not 1 <= days <= 16:
        return {"error": "Days must be between 1 and 16"}
    
    try:
        location_obj = get_coordinates(location)
        if not location_obj:
            return {"error": f"Location '{location}' not found"}
        
        # Get forecast data
        url = f"{WEATHER_BASE_URL}/forecast"
        params = {
            "latitude": location_obj.coordinates.lat, 
            "longitude": location_obj.coordinates.lon,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant",
            "timezone": location_obj.timezone or "auto", 
            "forecast_days": days
        }
        
        data = make_api_request(url, params)
        daily = data["daily"]
        
        forecast_days = []
        for i in range(len(daily["time"])):
            temperature = Temperature(
                current=0,  
                min=daily["temperature_2m_min"][i],
                max=daily["temperature_2m_max"][i]
            )
            
            apparent_temperature = Temperature(
                current=0,
                min=daily["apparent_temperature_min"][i],
                max=daily["apparent_temperature_max"][i]
            )
            
            weather = Weather(
                description=get_weather_description(daily["weather_code"][i]),
                code=daily["weather_code"][i]
            )
            
            precipitation = Precipitation(
                total=daily["precipitation_sum"][i],
                rain=daily["rain_sum"][i],
                showers=daily["showers_sum"][i],
                snow=daily["snowfall_sum"][i],
                hours=daily["precipitation_hours"][i]
            )
            
            wind = Wind(
                speed=daily["wind_speed_10m_max"][i],
                direction=daily["wind_direction_10m_dominant"][i],
                max_gusts=daily["wind_gusts_10m_max"][i]
            )
            
            forecast_day = ForecastDay(
                date=daily["time"][i],
                temperature=temperature,
                apparent_temperature=apparent_temperature,
                weather=weather,
                precipitation=precipitation,
                wind=wind
            )
            forecast_days.append(forecast_day)
        
        forecast = WeatherForecast(
            location=format_location_name(location_obj),
            coordinates=location_obj.coordinates,
            timezone=location_obj.timezone,
            forecast_days=len(forecast_days),
            forecasts=forecast_days
        )
        
        # Return as dictionary for MCP compatibility
        return asdict(forecast)
        
    except Exception as e:
        return {"error": f"Failed to get forecast for {location}: {str(e)}"}


def format_weather_resource(location: str) -> str:
    """Get weather information as a formatted resource"""
    data = get_current_weather_data(location)
    if "error" in data:
        return f"Error: {data['error']}"
    
    temp = data['temperature']
    weather = data['weather']
    wind = data['wind']
    
    feels_like = f" (feels like {temp['feels_like']}°C)" if temp.get('feels_like') else ""
    humidity = f"\nHumidity: {data['humidity']}%" if data.get('humidity') else ""
    pressure = f"\nPressure: {data['pressure']} hPa" if data.get('pressure') else ""
    
    return f"""Weather for {data['location']}:
Temperature: {temp['current']}°C{feels_like}
Condition: {weather['description']}{humidity}
Wind: {wind['speed']} {wind['unit']} at {wind['direction']}°{pressure}
Timezone: {data['timezone']}"""


def get_weather_summary_prompt(location: str, include_forecast: bool = False) -> str:
    """Generate a prompt for weather summary"""
    base = f"Please provide a weather summary for {location}, including current conditions and practical advice."
    if include_forecast:
        return f"{base} Include a 3-day forecast and activity recommendations."
    return f"{base} Keep it concise and user-friendly."
