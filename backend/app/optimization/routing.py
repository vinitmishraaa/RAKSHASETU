"""Road-network routing for relocation demos, with Google Maps handoff links."""
from __future__ import annotations
import math
import httpx
from .site_scoring import haversine_km


def _google_maps_url(village: dict, site: dict, mode: str = "driving") -> str:
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={village['lat']},{village['lng']}"
        f"&destination={site['lat']},{site['lng']}"
        f"&travelmode={mode}"
    )


async def route_between(village: dict, site: dict) -> dict:
    """Fetch an actual road geometry from OSRM and provide Google Maps live links.
    If the public router is unavailable, fall back to endpoints only."""
    straight_km = haversine_km(village["lat"], village["lng"], site["lat"], site["lng"])
    path = [[village["lat"], village["lng"]], [site["lat"], site["lng"]]]
    road_distance = straight_km
    road_minutes = None
    router = "endpoint fallback"
    try:
        coords = f"{village['lng']},{village['lat']};{site['lng']},{site['lat']}"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://router.project-osrm.org/route/v1/driving/{coords}", params={"overview":"full","geometries":"geojson"})
            r.raise_for_status()
            route = (r.json().get("routes") or [])[0]
            geom = route.get("geometry", {}).get("coordinates", [])
            if geom:
                path = [[float(latlng[1]), float(latlng[0])] for latlng in geom]
            road_distance = float(route.get("distance", 0)) / 1000 or straight_km
            road_minutes = round(float(route.get("duration", 0)) / 60)
            router = "OSRM road network"
    except Exception:
        pass

    transit_url = _google_maps_url(village, site, "transit")
    driving_url = _google_maps_url(village, site, "driving")
    return {
        "from": {"lat": village["lat"], "lng": village["lng"], "name": village["name"]},
        "to": {"lat": site["lat"], "lng": site["lng"], "name": site["name"]},
        "distance_km": round(road_distance, 1),
        "road_distance_km": round(road_distance, 1),
        "road_eta_minutes": road_minutes,
        "air_distance_km": round(straight_km, 1),
        "path": path,
        "router": router,
        "google_maps_driving_url": driving_url,
        "google_maps_transit_url": transit_url,
        "note": "Road path is network-routed when the public router responds. Google Maps links open live navigation and current traffic/transit information."
    }
