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
    from app.buoy_readings import recent_waves
    wave_observations = recent_waves(headers, lines, observation) 

    # Convert NDBC metric data to US units
    def num(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    water_c = num(observation.get("WTMP"))
    air_c = num(observation.get("ATMP"))
    dew_c = num(observation.get("DEWP"))

    wave_m = num(observation.get("WVHT"))

    wind_ms = num(observation.get("WSPD"))
    gust_ms = num(observation.get("GST"))

    water_f = round((water_c * 9 / 5) + 32, 1) if water_c is not None else None
    air_f = round((air_c * 9 / 5) + 32, 1) if air_c is not None else None
    dew_f = round((dew_c * 9 / 5) + 32, 1) if dew_c is not None else None

    wave_ft = round(wave_m * 3.28084, 1) if wave_m is not None else None

    wind_mph = round(wind_ms * 2.23694, 1) if wind_ms is not None else None
    gust_mph = round(gust_ms * 2.23694, 1) if gust_ms is not None else None

    
    return {
        "station": station_id,
        "wave_observations": wave_observations,
        "time": {
            "year": observation.get("YY"),
            "month": observation.get("MM"),
            "day": observation.get("DD"),
            "hour": observation.get("hh"),
            "minute": observation.get("mm")
       
              
    },

    "wind_direction_deg": observation.get("WDIR"),

    "wind_speed_mps": observation.get("WSPD"),
    "wind_speed_mph": wind_mph,

    "wind_gust_mps": observation.get("GST"),
    "wind_gust_mph": gust_mph,

    "wave_height_m": observation.get("WVHT"),
    "wave_height_ft": wave_ft,

    "dominant_wave_period_sec": observation.get("DPD"),

    "pressure_hpa": observation.get("PRES"),

    "air_temperature_c": observation.get("ATMP"),
    "air_temperature_f": air_f,

    "water_temperature_c": observation.get("WTMP"),
    "water_temperature_f": water_f,

    "dew_point_c": observation.get("DEWP"),
    "dew_point_f": dew_f
}
   
# --------------------------------------------------
# GOES-19 SATELLITE
# --------------------------------------------------

@app.get("/api/goes19")
def goes19():
    return {
        "satellite": "GOES-19",
        "status": "online",
        "sector": "CONUS",
        "product": "GeoColor",
        "image_url": "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/latest.jpg"
    }

@app.get("/api/enso")
def enso():
    from app.enso_feed import load_enso
    from fastapi import HTTPException
    try:
        return load_enso()
    except (requests.RequestException, ValueError):
        raise HTTPException(status_code=503, detail="NOAA ENSO data temporarily unavailable")

