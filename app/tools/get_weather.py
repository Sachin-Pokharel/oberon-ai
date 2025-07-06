import os
import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Location(BaseModel):
    name: str
    country: str
    localtime: str
    lat: float
    lon: float


class Condition(BaseModel):
    text: str = Field(..., alias="text")


class CurrentWeather(BaseModel):
    temp_c: float
    condition: Condition


class WeatherResponse(BaseModel):
    location: Location
    current: CurrentWeather

def get_weather_from_api(query: str) -> dict:
    """
    Fetch weather data from WeatherAPI for the given location query.

    Args:
        query (str): Location query string (e.g., city name).

    Returns:
        dict: Dictionary containing name, country, localtime, lat, lon,
              temperature in Celsius, and weather condition text.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY environment variable is not set")

    url = f"https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": query,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    weather_data = WeatherResponse.model_validate(response.json())

    return {
        "name": weather_data.location.name,
        "country": weather_data.location.country,
        "localtime": weather_data.location.localtime,
        "lat": weather_data.location.lat,
        "lon": weather_data.location.lon,
        "temp_c": weather_data.current.temp_c,
        "weather_condition": weather_data.current.condition.text,
    }