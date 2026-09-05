"""Ranks candidate safe sites for a given village using a weighted suitability score."""
from math import radians, sin, cos, sqrt, atan2

WEIGHTS = {"safety": 0.30, "capacity": 0.25, "accessibility": 0.20, "distance": 0.10, "facilities": 0.10, "infrastructure": 0.05}


def haversine_km(lat1, lng1, lat2, lng2) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def score_site(village: dict, site: dict) -> dict:
    distance_km = round(haversine_km(village["lat"], village["lng"], site["lat"], site["lng"]), 1)
    safety = max(0.0, 100 - site["hazard_risk"])
    available = max(0, site["capacity"] - site["current_occupancy"])
    capacity = min(1.0, available / max(village["population"], 1)) * 100
    accessibility = max(0.0, 100 - site["distance_road_km"] * 8)
    distance = max(0.0, 100 - (distance_km / 50) * 100)
    facilities = min(1.0, len(site["facilities"]) / 4) * 100
    infrastructure = site["infrastructure_score"]
    suitability = (safety * WEIGHTS["safety"] + capacity * WEIGHTS["capacity"] + accessibility * WEIGHTS["accessibility"] + distance * WEIGHTS["distance"] + facilities * WEIGHTS["facilities"] + infrastructure * WEIGHTS["infrastructure"])
    return {
        "site_id": site["id"], "site_name": site["name"], "region": site.get("region", site.get("state")),
        "suitability": round(min(100.0, max(0.0, suitability)), 1), "distance_km": distance_km,
        "available_capacity": available,
        "road_access": "GOOD" if site["distance_road_km"] <= 1.5 else ("MODERATE" if site["distance_road_km"] <= 4 else "POOR"),
        "hazard_risk": site["hazard_risk"], "facilities": site["facilities"],
    }


def rank_sites(village: dict, sites: list[dict]) -> list[dict]:
    region = village.get("region", village.get("state"))
    regional = [s for s in sites if s.get("region", s.get("state")) == region]
    candidates = regional if regional else sites
    return sorted([score_site(village, s) for s in candidates], key=lambda s: (s["suitability"], -s["distance_km"]), reverse=True)
