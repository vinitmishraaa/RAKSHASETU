"""Lightweight routing helper. In this prototype it returns a straight
line (great-circle) route between village and safe site for map display;
swap for a real routing engine (OSRM / GraphHopper) for road-network
accurate paths in production."""
from .site_scoring import haversine_km


def route_between(village: dict, site: dict) -> dict:
    distance_km = round(haversine_km(village["lat"], village["lng"], site["lat"], site["lng"]), 1)
    return {
        "from": {"lat": village["lat"], "lng": village["lng"], "name": village["name"]},
        "to": {"lat": site["lat"], "lng": site["lng"], "name": site["name"]},
        "distance_km": distance_km,
        "path": [
            [village["lat"], village["lng"]],
            [site["lat"], site["lng"]],
        ],
        "note": "Straight-line prototype route. Replace with a road-network routing engine for production.",
    }
