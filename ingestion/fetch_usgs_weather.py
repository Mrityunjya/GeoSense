import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
OWM_API_KEY = os.getenv("OWM_API_KEY")

def fetch_weather_alerts(lat=28.61, lon=77.21, api_key=OWM_API_KEY):
    """
    Fetch real-time weather alerts from OpenWeatherMap OneCall API.

    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        api_key (str): Your OpenWeatherMap API key (from .env)

    Returns:
        List of alert dictionaries
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&exclude=minutely,hourly,daily"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        alerts = []
        for alert in data.get("alerts", []):
            alerts.append({
                "location": alert.get("sender_name", "Weather Alert"),
                "text": f"{alert['event']} - {alert['description'][:80]}...",
                "coordinates": (lat, lon),
                "timestamp": alert["start"]
            })

        return alerts

    except Exception as e:
        print(f"[⚠️ Weather API Error] {e}")
        return []
