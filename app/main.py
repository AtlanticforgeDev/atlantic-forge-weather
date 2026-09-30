from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(
    title="Atlantic Forge Weather API",
    version="0.1.0"
)

@app.get("/api/status")
def root():
    return {
        "status": "online",
        "project": "Atlantic Forge Weather"
    }

@app.get("/")
def dashboard():
    return FileResponse("app/index.html")

import requests

@app.get("/api/weather")
def weather():
    headers = {"User-Agent": "AtlanticForgeWeather/0.1"}

    point = requests.get(
        "https://api.weather.gov/points/38.9586,-77.3570",
        headers=headers,
        timeout=10
    ).json()

    forecast_url = point["properties"]["forecast"]

    forecast = requests.get(
        forecast_url,
        headers=headers,
        timeout=10
    ).json()

    period = forecast["properties"]["periods"][0]

    return {
        "period": period["name"],
        "temperature": period["temperature"],
        "unit": period["temperatureUnit"],
        "forecast": period["shortForecast"],
        "details": period["detailedForecast"]
    }

@app.get("/api/buoy/{station_id}")
def buoy(station_id: str):

    url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return {
            "station": station_id,
            "status": "unavailable"
        }

    lines = response.text.strip().splitlines()

    headers = lines[0].replace("#", "").split()
    values = lines[2].split()

    observation = dict(zip(headers, values))

    return {
        "station": station_id,
        "time": {
            "year": observation.get("YY"),
            "month": observation.get("MM"),
            "day": observation.get("DD"),
            "hour": observation.get("hh"),
            "minute": observation.get("mm")
        },
        "wind_direction": observation.get("WDIR"),
        "wind_speed": observation.get("WSPD"),
        "wind_gust": observation.get("GST"),
        "wave_height": observation.get("WVHT"),
        "dominant_wave_period": observation.get("DPD"),
        "pressure": observation.get("PRES"),
        "air_temperature": observation.get("ATMP"),
        "water_temperature": observation.get("WTMP"),
        "dew_point": observation.get("DEWP")
    }
