from datetime import datetime, timezone
from math import isfinite

def recent_waves(headers, lines, observation):
    now = datetime.now(timezone.utc)
    metadata = {}
    for field in ("WVHT", "DPD"):
        observation[field] = "MM"
    rows = sorted((s.split() for s in lines[2:]),
                  key=lambda p: p[:5], reverse=True)
    for parts in rows:
        if len(parts) != len(headers):
            continue
        row = dict(zip(headers, parts))
        try:
            stamp = datetime(*(int(row[k]) for k in
                ("YY", "MM", "DD", "hh", "mm")), tzinfo=timezone.utc)
        except (KeyError, ValueError):
            continue
        age = (now - stamp).total_seconds()
        if not 0 <= age <= 10800:
            continue
        for field in ("WVHT", "DPD"):
            if field in metadata:
                continue
            try:
                value = float(row[field])
            except (KeyError, ValueError):
                continue
            if not isfinite(value) or value < 0:
                continue
            observation[field] = row[field]
            metadata[field] = {
                "observed_at_utc": stamp.isoformat(),
                "age_minutes": int(age // 60)}
    return metadata
