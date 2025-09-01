"""
Weather data models - Data classes for weather objects.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Coordinates:
    lat: float
    lon: float


@dataclass
class Location:
    name: str
    country: str = ""
    admin1: str = ""
    timezone: str = ""
    coordinates: Coordinates = None


@dataclass
class Temperature:
    current: float
    feels_like: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    unit: str = "°C"


@dataclass
class Weather:
    description: str
    code: int


@dataclass
class Wind:
    speed: float
    direction: float
    unit: str = "km/h"
    max_gusts: Optional[float] = None


@dataclass
class Precipitation:
    total: float = 0
    rain: float = 0
    showers: float = 0
    snow: float = 0
    hours: float = 0
    unit: str = "mm"


@dataclass
class CurrentWeather:
    location: str
    coordinates: Coordinates
    temperature: Temperature
    weather: Weather
    wind: Wind
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    precipitation: float = 0
    timezone: str = ""
    timestamp: str = ""


@dataclass
class ForecastDay:
    date: str
    temperature: Temperature
    apparent_temperature: Temperature
    weather: Weather
    precipitation: Precipitation
    wind: Wind


@dataclass
class WeatherForecast:
    location: str
    coordinates: Coordinates
    timezone: str
    forecast_days: int
    forecasts: List[ForecastDay]
