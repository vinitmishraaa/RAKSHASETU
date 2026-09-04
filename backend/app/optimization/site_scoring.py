"""Ranks candidate safe sites for a given village using the weighted
suitability formula from the technical approach doc:
Safety 30% | Capacity 25% | Accessibility 20% | Distance 10% |
Facilities 10% | Infrastructure 5%."""
from math import radians, sin, cos, sqrt, atan2

WEIGHTS = {
    "safety": 0.30,
    "capacity": 0.25,
    "accessibility": 0.20,
    "distance": 0.10,
    "facilities": 0.10,
    "infrastructure": 0.05,
}


def haversine_km(lat1, lng1, lat2, lng2) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def score_site(village: dict, site: dict) -> dict:
    distance_km = round(haversine_km(village["lat"], village["lng"], site["lat"], site["lng"]), 1)

    safety_component = max(0.0, 100 - site["hazard_risk"])

    available = max(0, site["capacity"] - site["current_occupancy"])
    capacity_component = min(1.0, available / max(village["population"], 1)) * 100

    accessibility_component = max(0.0, 100 - site["distance_road_km"] * 8)

    # Closer sites score higher; normalise against a 50km reasonable band.
    distance_component = max(0.0, 100 - (distance_km / 50) * 100)

    facilities_component = min(1.0, len(site["facilities"]) / 4) * 100

    infrastructure_component = site["infrastructure_score"]

    suitability = (
        safety_component * WEIGHTS["safety"]
        + capacity_component * WEIGHTS["capacity"]
        + accessibility_component * WEIGHTS["accessibility"]
        + distance_component * WEIGHTS["distance"]
        + facilities_component * WEIGHTS["facilities"]
        + infrastructure_component * WEIGHTS["infrastructure"]
    )

    return {
        "site_id": site["id"],
        "site_name": site["name"],
        "suitability": round(min(100.0, max(0.0, suitability)), 1),
        "distance_km": distance_km,
        "available_capacity": available,
        "road_access": "GOOD" if site["distance_road_km"] <= 1.5 else ("MODERATE" if site["distance_road_km"] <= 4 else "POOR"),
        "hazard_risk": site["hazard_risk"],
    }


def rank_sites(village: dict, sites: list[dict]) -> list[dict]:
    scored = [score_site(village, s) for s in sites]
    return sorted(scored, key=lambda s: s["suitability"], reverse=True)
