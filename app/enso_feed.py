from datetime import datetime, timezone
from math import isfinite
import requests

SOURCE = "https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt"

def load_enso():
    response = requests.get(SOURCE, timeout=15)
    response.raise_for_status()
    lines = response.text.splitlines()
    if not lines or lines[0].split() != ["SEAS", "YR", "ANOM"]:
        raise ValueError("Unexpected NOAA data format")
    seasons = "DJF JFM FMA MAM AMJ MJJ JJA JAS ASO SON OND NDJ".split()
    history = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) != 3 or parts[0] not in seasons:
            continue
        season, year, value = parts
        year, value = int(year), float(value)
        if isfinite(value) and abs(value) < 10:
            history.append(dict(season=season, year=year, roni_c=value))
    if len(history) < 2:
        raise ValueError("NOAA readings unavailable")
    return {
        "source": "NOAA CPC",
        "source_url": SOURCE,
        "index": "RONI",
        "latest": history[-1],
        "change_c": round(history[-1]["roni_c"] - history[-2]["roni_c"], 2),
        "history": history[-24:],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat()
    }
