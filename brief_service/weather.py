from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import requests

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


WEATHER_CODE_SUMMARY = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


@dataclass
class WeatherBrief:
    temperature_c: float
    windspeed_kmh: float
    weather_description: str
    high_c: float
    low_c: float
    precip_chance: Optional[int]


def fetch_weather(lat: float, lon: float, timezone: str = "Asia/Shanghai") -> WeatherBrief:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": timezone,
    }
    logger.info("Fetching weather for lat=%s lon=%s", lat, lon)
    resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    current = data.get("current_weather", {})
    daily = data.get("daily", {})

    description = WEATHER_CODE_SUMMARY.get(current.get("weathercode"), "Weather update")
    high = (daily.get("temperature_2m_max") or [None])[0]
    low = (daily.get("temperature_2m_min") or [None])[0]
    precip = (daily.get("precipitation_probability_max") or [None])[0]

    return WeatherBrief(
        temperature_c=current.get("temperature"),
        windspeed_kmh=current.get("windspeed"),
        weather_description=description,
        high_c=high,
        low_c=low,
        precip_chance=precip,
    )
