"""
Weather MCP configuration constants.
"""

# Weather API configuration - Open-Meteo (free, no API key required)
WEATHER_BASE_URL = "https://api.open-meteo.com/v1"
GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1"

# Weather code descriptions (WMO Weather interpretation codes)
WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Slight thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}
