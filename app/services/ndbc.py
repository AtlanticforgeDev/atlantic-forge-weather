import requests


NDBC_REALTIME_URL = "https://www.ndbc.noaa.gov/data/realtime2/{station}.txt"


def get_buoy_data(station: str):
    """
    Get the latest observation from any NDBC station.
    """

    station = station.upper().strip()

    url = NDBC_REALTIME_URL.format(station=station)

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    lines = response.text.strip().splitlines()

    if len(lines) < 3:
        raise ValueError(f"No current data available for station {station}")

    headers = lines[0].lstrip("#").split()
    values = lines[2].split()

    observation = dict(zip(headers, values))

    return {
        "station": station,
        "time": {
            "year": observation.get("YY"),
            "month": observation.get("MM"),
            "day": observation.get("DD"),
            "hour": observation.get("hh"),
            "minute": observation.get("mm"),
        },
        "wind_direction": observation.get("WDIR"),
        "wind_speed": observation.get("WSPD"),
        "wind_gust": observation.get("GST"),
        "wave_height": observation.get("WVHT"),
        "dominant_wave_period": observation.get("DPD"),
        "average_wave_period": observation.get("APD"),
        "wave_direction": observation.get("MWD"),
        "pressure": observation.get("PRES"),
        "air_temperature": observation.get("ATMP"),
        "water_temperature": observation.get("WTMP"),
        "dew_point": observation.get("DEWP"),
        "visibility": observation.get("VIS"),
        "pressure_tendency": observation.get("PTDY"),
        "tide": observation.get("TIDE"),
    }
