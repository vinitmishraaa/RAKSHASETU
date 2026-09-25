"""Multi-Hazard Risk Engine:
Combines 4 primary recurring natural hazards:
1. Floods
2. Landslides
3. Coastal Erosion
4. Cloudbursts
along with real-time meteorological observations (Open-Meteo precipitation/wind) and seismic telemetry (USGS)."""
from __future__ import annotations
from math import exp

# Multi-Hazard Component Weights
WEIGHTS = {
    "flood": 0.25,
    "landslide": 0.25,
    "coastal_erosion": 0.15,
    "cloudburst": 0.15,
    "live_signals": 0.20,
}


def hazard_score(village: dict, weather: dict | None = None, earthquake: dict | None = None) -> float:
    base_flood = float(village.get("flood_hazard") or 40.0)
    base_landslide = float(village.get("landslide_hazard") or 25.0)
    base_erosion = float(village.get("coastal_erosion_hazard") or 15.0)
    base_cloudburst = float(village.get("cloudburst_hazard") or 20.0)

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
        + base_landslide * WEIGHTS["landslide"]
        + base_erosion * WEIGHTS["coastal_erosion"]
        + base_cloudburst * WEIGHTS["cloudburst"]
        + dynamic_hazard * WEIGHTS["live_signals"]
    )
    # If dynamic hazard is acute (severe storm or close earthquake), boost overall hazard
    if dynamic_hazard >= 70:
        score = max(score, dynamic_hazard)

    return round(min(100.0, max(0.0, score)), 1)
