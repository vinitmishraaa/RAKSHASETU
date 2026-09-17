"""Hazard indicator: combines flood, cyclone and landslide hazard signals
along with real-time weather (Open-Meteo/OpenWeather) and seismic observations (USGS)."""
from __future__ import annotations
from math import exp

WEIGHTS = {"flood": 0.40, "cyclone": 0.30, "landslide": 0.15, "live_weather": 0.15}


def hazard_score(village: dict, weather: dict | None = None, earthquake: dict | None = None) -> float:
    base_flood = village.get("flood_hazard", 50)
    base_cyclone = village.get("cyclone_hazard", 40)
    base_landslide = village.get("landslide_hazard", 20)

    # Real-time weather contribution (precipitation and wind speed)
    weather_hazard = 0.0
    if weather:
        precip = float(weather.get("precipitation_mm") or 0.0)
        wind = float(weather.get("wind_speed_kmh") or 0.0)
        # 15mm/h is heavy rain in India IMD classification; 60km/h is storm gale
        rain_factor = min(100.0, precip * 6.0)
        wind_factor = min(100.0, max(0.0, (wind - 20.0) * 2.2))
        weather_hazard = max(rain_factor, wind_factor)

    # Seismic hazard contribution (magnitude attenuated by distance)
    quake_hazard = 0.0
    if earthquake:
        mag = float(earthquake.get("magnitude") or 0.0)
        dist = float(earthquake.get("distance_km") or 999.0)
        if mag >= 3.0 and dist < 350.0:
            quake_hazard = min(100.0, mag * 14.0 * exp(-dist / 200.0))

    dynamic_hazard = max(weather_hazard, quake_hazard)

    score = (
        base_flood * WEIGHTS["flood"]
        + base_cyclone * WEIGHTS["cyclone"]
        + base_landslide * WEIGHTS["landslide"]
        + dynamic_hazard * WEIGHTS["live_weather"]
    )
    # If dynamic hazard is acute (severe storm or close earthquake), boost overall hazard
    if dynamic_hazard >= 70:
        score = max(score, dynamic_hazard)

    return round(min(100.0, max(0.0, score)), 1)
