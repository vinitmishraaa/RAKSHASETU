"""Live, open geospatial data adapters used by RakshaSetu.

Sources: OpenStreetMap/Overpass, Open-Meteo, USGS and GDACS.
Unknown quantities remain None; no operational value is inferred.
"""
from __future__ import annotations

from datetime import datetime, timezone
from math import cos, radians, sqrt
from xml.etree import ElementTree as ET

import httpx

REGION_CODES = {"West Bengal": "WB", "Bihar": "BR", "Sikkim": "SK", "Odisha": "OR"}
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
GDACS_RSS_URL = "https://www.gdacs.org/contentdata/xml/rss.xml"


def bbox_for(region):
    return REGION_BBOXES.get(region or "India", REGION_BBOXES["India"])


def _area_query(kind: str, region: str | None):
    targets = [region] if region in REGION_CODES else list(REGION_CODES)
    blocks = []
    nodes = []
    for name in targets:
        code = REGION_CODES[name]
        blocks.append(
            f'area["ISO3166-2"="IN-{code}"][boundary=administrative][admin_level=4]->.{code};'
        )
        if kind == "node":
            nodes.append(f'{kind}(area.{code})[place~"^(village|town|city)$"];')
        else:
            nodes.append(f'{kind}(area.{code})[amenity=shelter];')
    query = "[out:json][timeout:45];(" + "".join(blocks) + "(" + "".join(nodes) + "););out center tags;"
    return query, targets


def _risk_from_observations(precip_mm, wind_kmh, earthquake_distance_km):
    rain = min(100.0, max(0.0, (precip_mm or 0.0) * 8.0))
    wind = min(100.0, max(0.0, (wind_kmh or 0.0) * 1.5))
    quake = 0.0 if earthquake_distance_km is None else max(0.0, 100.0 - earthquake_distance_km * 4.0)
    return round(max(rain, wind, quake), 1)


def _level(score):
    return "CRITICAL" if score >= 75 else "HIGH" if score >= 50 else "MODERATE" if score >= 30 else "LOW"


def _distance_km(lat1, lon1, lat2, lon2):
    x = radians(lon2 - lon1) * cos(radians((lat1 + lat2) / 2))
    y = radians(lat2 - lat1)
    return 6371.0 * sqrt(x * x + y * y)


async def _overpass(query):
    async with httpx.AsyncClient(
        timeout=50, headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"}
    ) as client:
        response = await client.post(OVERPASS_URL, data={"data": query})
        response.raise_for_status()
        return response.json()


async def get_live_settlements(region=None):
    query, targets = _area_query("node", region)
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
        state = tags.get("addr:state") or (region if region in REGION_CODES else None)
        if state not in REGION_CODES and len(targets) == 1:
            state = targets[0]
        items.append(
            {
                "id": f"osm-{element['type']}-{element['id']}",
                "name": tags.get("name") or "Unnamed mapped settlement",
                "district": tags.get("addr:district"),
                "state": state,
                "region": state or region or "India",
                "lat": float(lat),
                "lng": float(lon),
                "population": population,
                "population_source": "OpenStreetMap population tag" if population is not None else None,
                "source": "OpenStreetMap",
                "source_url": f"https://www.openstreetmap.org/{element['type']}/{element['id']}",
            }
        )
    return items


async def get_live_shelters(region=None):
    targets = [region] if region in REGION_CODES else list(REGION_CODES)
    blocks = []
    selectors = []
    for name in targets:
        code = REGION_CODES[name]
        blocks.append(
            f'area["ISO3166-2"="IN-{code}"][boundary=administrative][admin_level=4]->.{code};'
        )
        selectors.extend(
            [
                f"node(area.{code})[amenity=shelter];",
                f"way(area.{code})[amenity=shelter];",
                f"relation(area.{code})[amenity=shelter];",
                f"node(area.{code})[emergency=shelter];",
                f"way(area.{code})[emergency=shelter];",
                f"relation(area.{code})[emergency=shelter];",
            ]
        )
    query = "[out:json][timeout:45];(" + "".join(blocks) + "(" + "".join(selectors) + "););out center tags;"
    data = await _overpass(query)
    items = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        center = element.get("center", {})
        lat = element.get("lat", center.get("lat"))
        lon = element.get("lon", center.get("lon"))
        if lat is None or lon is None:
            continue
        state = region if region in REGION_CODES else None
        items.append(
            {
                "id": f"osm-shelter-{element['type']}-{element['id']}",
                "name": tags.get("name") or "Mapped emergency shelter",
                "region": state or "India",
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
            }
        )
    return items


async def _earthquakes():
    async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "RakshaSetu/1.0"}) as client:
        response = await client.get(USGS_URL)
        response.raise_for_status()
        features = response.json().get("features", [])
    out = []
    for feature in features:
        coords = (feature.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        props = feature.get("properties") or {}
        out.append(
            {
                "lat": float(coords[1]),
                "lng": float(coords[0]),
                "magnitude": float(props.get("mag") or 0),
                "time": props.get("time"),
                "place": props.get("place") or "Earthquake",
                "id": feature.get("id"),
            }
        )
    return out


async def _gdacs_events(region=None):
    south, north, west, east = bbox_for(region)
    async with httpx.AsyncClient(timeout=20, headers={"User-Agent": "RakshaSetu/1.0"}) as client:
        response = await client.get(GDACS_RSS_URL)
        response.raise_for_status()
    root = ET.fromstring(response.text)
    items = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "GDACS event").strip()
        description = (item.findtext("description") or "").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link or title).strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        lat = lon = None
        for child in list(item):
            tag = child.tag.lower().split("}")[-1]
            if tag in {"lat", "latitude"}:
                try:
                    lat = float(child.text)
                except (TypeError, ValueError):
                    pass
            if tag in {"long", "lon", "longitude"}:
                try:
                    lon = float(child.text)
                except (TypeError, ValueError):
                    pass
        if lat is None or lon is None:
            continue
        if not (south <= lat <= north and west <= lon <= east):
            continue
        items.append(
            {
                "id": f"gdacs-{guid}",
                "type": "GDACS Alert",
                "title": title,
                "lat": lat,
                "lng": lon,
                "time": pub_date,
                "severity": "ALERT",
                "source": "GDACS",
                "detail": description[:500],
                "url": link or "https://www.gdacs.org/",
            }
        )
    return items


async def enrich_settlements_with_weather(settlements):
    earthquakes = await _earthquakes()
    async with httpx.AsyncClient(timeout=20, headers={"User-Agent": "RakshaSetu/1.0"}) as client:
        for item in settlements:
            weather = {}
            try:
                weather = (
                    await client.get(
                        OPEN_METEO_URL,
                        params={
                            "latitude": item["lat"],
                            "longitude": item["lng"],
                            "current": "temperature_2m,precipitation,wind_speed_10m",
                            "timezone": "UTC",
                        },
                    )
                ).json().get("current", {})
            except Exception:
                pass
            nearest = min(
                (
                    (_distance_km(item["lat"], item["lng"], q["lat"], q["lng"]), q)
                    for q in earthquakes
                ),
                default=(None, None),
                key=lambda x: x[0] if x[0] is not None else 1e12,
            )
            distance, quake = nearest
            score = _risk_from_observations(
                weather.get("precipitation"), weather.get("wind_speed_10m"), distance
            )
            item.update(
                {
                    "weather": {
                        "temperature_c": weather.get("temperature_2m"),
                        "precipitation_mm": weather.get("precipitation"),
                        "wind_speed_kmh": weather.get("wind_speed_10m"),
                    },
                    "nearest_earthquake_km": round(distance, 1) if distance is not None else None,
                    "nearest_earthquake": quake,
                    "risk_score": score,
                    "level": _level(score),
                    "risk_model": "Live indicator from Open-Meteo current precipitation/wind and nearest USGS earthquake; not an official hazard rating.",
                    "observed_at": datetime.now(timezone.utc).isoformat(),
                }
            )
    return settlements
