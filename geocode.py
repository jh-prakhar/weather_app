# geocode.py
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from typing import Optional, List

geolocator = Nominatim(user_agent="prakhar_weather_app", timeout=10)

def geocode(query: str, limit: int = 3):
    """
    Returns a list of candidate dicts: {name, lat, lon, raw}
    """
    try:
        locations = geolocator.geocode(query, exactly_one=False, limit=limit)
    except GeocoderTimedOut:
        return []
    if not locations:
        return []
    results = []
    for loc in locations:
        results.append({
            "name": loc.address,
            "lat": loc.latitude,
            "lon": loc.longitude,
            "raw": loc.raw
        })
    return results
