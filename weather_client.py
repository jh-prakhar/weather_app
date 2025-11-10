# weather_client.py
import os
import httpx
from datetime import datetime, timedelta

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE = "https://api.openweathermap.org/data/2.5"

async def get_current_weather(lat: float, lon: float):
    url = f"{BASE}/weather"
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units":"metric"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

async def get_5day_forecast(lat: float, lon: float):
    # OpenWeatherMap 5 day / 3 hour forecast
    url = f"{BASE}/forecast"
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units":"metric"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

# helper to aggregate forecast to daily summary
def aggregate_daily(forecast_json):
    # forecast_json["list"] contains 3-hour entries
    days = {}
    for item in forecast_json.get("list", []):
        dt = datetime.utcfromtimestamp(item["dt"])
        day_key = dt.date().isoformat()
        if day_key not in days:
            days[day_key] = {
                "temps": [],
                "weather": []
            }
        days[day_key]["temps"].append(item["main"]["temp"])
        days[day_key]["weather"].append(item["weather"][0])
    # produce list
    out = []
    for d, data in days.items():
        out.append({
            "date": d,
            "temp_min": min(data["temps"]),
            "temp_max": max(data["temps"]),
            "weather_sample": data["weather"][len(data["weather"])//2]
        })
    return out
