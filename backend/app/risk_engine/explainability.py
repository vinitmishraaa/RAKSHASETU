"""Produces human-readable reasons explaining the computed risk level,
grounded in physical factors and live environmental observations."""
from __future__ import annotations


def explain(village: dict, indicators: dict, history: list, weather: dict | None = None, earthquake: dict | None = None) -> list[str]:
    reasons = []

    if weather:
        precip = float(weather.get("precipitation_mm") or 0)
        wind = float(weather.get("wind_speed_kmh") or 0)
        if precip >= 15.0:
            reasons.append(f"Live severe precipitation: {precip:.1f} mm/h (Open-Meteo realtime)")
        elif precip >= 5.0:
            reasons.append(f"Live active rainfall: {precip:.1f} mm/h")
        if wind >= 45.0:
            reasons.append(f"Live gale-force wind speed: {wind:.1f} km/h")

    if earthquake:
        dist = float(earthquake.get("distance_km") or 999)
        mag = float(earthquake.get("magnitude") or 0)
        if dist < 250 and mag >= 4.0:
            reasons.append(f"Seismic activity: M{mag:.1f} earthquake within {dist:.0f} km (USGS feed)")

    if village.get("flood_hazard", 0) >= 70:
        reasons.append(f"Elevated flood susceptibility ({village['flood_hazard']}%)")
    if village.get("cyclone_hazard", 0) >= 70:
        reasons.append(f"High coastal cyclone vulnerability ({village['cyclone_hazard']}%)")
    if village.get("landslide_hazard", 0) >= 70:
        reasons.append(f"Steep slope landslide hazard ({village['landslide_hazard']}%)")
    if indicators.get("vulnerability", 0) >= 60:
        children = village.get("children", 0)
        elderly = village.get("elderly", 0)
        reasons.append(f"High demographic vulnerability ({children} children, {elderly} elderly)")
    if village.get("distance_road_km", 0) >= 6:
        reasons.append(f"Remote access road ({village['distance_road_km']} km to major road)")
    if village.get("embankment_condition", 1.0) <= 0.4:
        reasons.append("Degraded or compromised flood embankment")
    if len(history) >= 2:
        reasons.append(f"Historical incident record ({len(history)} past disaster events)")

    if not reasons:
        reasons.append("Physical indicators currently within manageable operational limits")

    return reasons


def recommended_action(level: str) -> str:
    return {
        "CRITICAL": "IMMEDIATE EVACUATION: Stage transport, dispatch designated shelter allocation, alert emergency services",
        "HIGH": "PRIORITY ADVISORY: Prepare shelter intake, review vulnerable population transport, pre-position relief",
        "MODERATE": "STANDBY MONITORING: Check road accessibility and maintain communication with village nodal officers",
        "LOW": "ROUTINE MONITORING: Regular situational updates via district emergency operations center",
    }.get(level, "ROUTINE MONITORING")
