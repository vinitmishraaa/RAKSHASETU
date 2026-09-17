"""Live, open geospatial data adapters used by RakshaSetu.

Sources:
- OpenStreetMap / Overpass for mapped settlements and emergency shelters.
- Open-Meteo for current weather observations at settlement coordinates.
- USGS public GeoJSON feed for recent earthquakes.

No synthetic population, shelter capacity, occupancy or infrastructure values are
created here. Missing values remain None and the UI must show them as unverified.
"""
from __future__ import annotations
from datetime import datetime, timezone
from math import cos, radians, sqrt
import httpx

REGION_BBOXES = {
    "India": (6.0, 37.2, 68.0, 97.5),
    "West Bengal": (21.4, 27.3, 85.8, 89.9),
    "Bihar": (24.0, 27.6, 83.2, 88.4),
    "Sikkim": (27.0, 28.2, 88.0, 88.9),
    "Odisha": (17.7, 22.8, 81.3, 87.6),
}

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def bbox_for(region: str | None) -> tuple[float, float, float, float]:
    return REGION_BBOXES.get(region or "India", REGION_BBOXES["India"])


def _risk_from_observations(precip_mm: float | None, wind_kmh: float | None, earthquake_distance_km: float | None) -> float:
    """Transparent live indicator; it is not an official government risk score."""
    rain_component = min(100.0, max(0.0, (precip_mm or 0.0) * 8.0))
    wind_component = min(100.0, max(0.0, (wind_kmh or 0.0) * 1.5))
    if earthquake_distance_km is None:
        quake_component = 0.0
    else:
        quake_component = max(0.0, 100.0 - earthquake_distance_km * 4.0)
    return round(max(rain_component, wind_component, quake_component), 1)


def _level(score: float) -> str:
    if score >= 75:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 30:
        return "MODERATE"
    return "LOW"


def _distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Equirectangular approximation is sufficient for nearest-observation lookup.
    x = radians(lon2 - lon1) * cos(radians((lat1 + lat2) / 2))
    y = radians(lat2 - lat1)
    return 6371.0 * sqrt(x * x + y * y)


async def _overpass(query: str) -> dict:
    async with httpx.AsyncClient(timeout=35, headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"}) as client:
        response = await client.post(OVERPASS_URL, data={"data": query})
        response.raise_for_status()
        return response.json()


async def get_live_settlements(region: str | None = None) -> list[dict]:
    south, north, west, east = bbox_for(region)
    query = f"""[out:json][timeout:30];\n(\n  node[place~\"^(village|town|city)$\"]({south},{west},{north},{east});\n);\nout tags center;"""
    data = await _overpass(query)
    items = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        lat = element.get("lat")
        lon = element.get("lon")
        if lat is None or lon is None:
            continue
        population = None
        try:
            if tags.get("population"):
                population = int(float(str(tags["population"]).replace(",", "")))
        except (TypeError, ValueError):
            population = None
        items.append({
            "id": f"osm-{element['type']}-{element['id']}",
            "name": tags.get("name") or "Unnamed mapped settlement",
            "district": tags.get("addr:district"),
            "state": tags.get("addr:state") or region,
            "region": region or "India",
            "lat": float(lat),
            "lng": float(lon),
            "population": population,
            "population_source": "OpenStreetMap population tag" if population is not None else None,
            "source": "OpenStreetMap",
            "source_url": f"https://www.openstreetmap.org/{element['type']}/{element['id']}",
        })
    return items


async def get_live_shelters(region: str | None = None) -> list[dict]:
    south, north, west, east = bbox_for(region)
    query = f"""[out:json][timeout:30];\n(\n  node[amenity=shelter]({south},{west},{north},{east});\n  way[amenity=shelter]({south},{west},{north},{east});\n  relation[amenity=shelter]({south},{west},{north},{east});\n  node[emergency=shelter]({south},{west},{north},{east});\n  way[emergency=shelter]({south},{west},{north},{east});\n  relation[emergency=shelter]({south},{west},{north},{east});\n);\nout center tags;"""
    data = await _overpass(query)
    items = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        center = element.get("center", {})
        lat = element.get("lat", center.get("lat"))
        lon = element.get("lon", center.get("lon"))
        if lat is None or lon is None:
            continue
        items.append({
            "id": f"osm-shelter-{element['type']}-{element['id']}",
            "name": tags.get("name") or "Mapped emergency shelter",
            "region": region or "India",
            "lat": float(lat),
            "lng": float(lon),
            "capacity": None,
            "current_occupancy": None,
            "available_capacity": None,
            "hazard_risk": None,
            "infrastructure_score": None,
            "facilities": [v for v in [tags.get("amenity"), tags.get("emergency"), tags.get("access")] if v],
            "verified": False,
            "source": "OpenStreetMap",
            "source_url": f"https://www.openstreetmap.org/{element['type']}/{element['id']}",
            "note": "Mapped location only. Capacity, occupancy and operational status are not inferred.",
        })
    return items


async def _earthquakes() -> list[dict]:
    async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "RakshaSetu/1.0"}) as client:
        response = await client.get(USGS_URL)
        response.raise_for_status()
        features = response.json().get("features", [])
    result = []
    for feature in features:
        coords = (feature.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        props = feature.get("properties") or {}
        result.append({"lat": float(coords[1]), "lng": float(coords[0]), "magnitude": float(props.get("mag") or 0), "time": props.get("time"), "place": props.get("place") or "Earthquake", "id": feature.get("id")})
    return result


async def enrich_settlements_with_weather(settlements: list[dict]) -> list[dict]:
    earthquakes = await _earthquakes()
    async with httpx.AsyncClient(timeout=20, headers={"User-Agent": "RakshaSetu/1.0"}) as client:
        for item in settlements:
            try:
                params = {"latitude": item["lat"], "longitude": item["lng"], "current": "temperature_2m,precipitation,wind_speed_10m", "timezone": "UTC"}
                weather = (await client.get(OPEN_METEO_URL, params=params)).json().get("current", {})
                precipitation = weather.get("precipitation")
                wind = weather.get("wind_speed_10m")
            except Exception:
                precipitation = None
                wind = None
            nearest = min(((_distance_km(item["lat"], item["lng"], q["lat"], q["lng"]), q) for q in earthquakes), default=(None, None), key=lambda x: x[0] if x[0] is not None else 1e12)
            distance, quake = nearest
            score = _risk_from_observations(precipitation, wind, distance)
            item.update({
                "weather": {"temperature_c": weather.get("temperature_2m") if 'weather' in locals() else None, "precipitation_mm": precipitation, "wind_speed_kmh": wind},
                "nearest_earthquake_km": round(distance, 1) if distance is not None else None,
                "nearest_earthquake": quake,
                "risk_score": score,
                "level": _level(score),
                "risk_model": "Live indicator from Open-Meteo current precipitation/wind and nearest USGS earthquake; not an official hazard rating.",
                "observed_at": datetime.now(timezone.utc).isoformat(),
            })
    return settlements
