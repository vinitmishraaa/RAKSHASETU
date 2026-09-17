from __future__ import annotations

import asyncio
import time
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/api/regions", tags=["regions"])

# Stable Indian administrative list. Names/codes are not fetched from Overpass so
# the first dropdown cannot fail because a public OSM endpoint is rate-limited.
INDIA_REGIONS = [
    ("Andaman and Nicobar Islands", "IN-AN"), ("Andhra Pradesh", "IN-AP"),
    ("Arunachal Pradesh", "IN-AR"), ("Assam", "IN-AS"), ("Bihar", "IN-BR"),
    ("Chandigarh", "IN-CH"), ("Chhattisgarh", "IN-CT"),
    ("Dadra and Nagar Haveli and Daman and Diu", "IN-DH"), ("Delhi", "IN-DL"),
    ("Goa", "IN-GA"), ("Gujarat", "IN-GJ"), ("Haryana", "IN-HR"),
    ("Himachal Pradesh", "IN-HP"), ("Jammu and Kashmir", "IN-JK"),
    ("Jharkhand", "IN-JH"), ("Karnataka", "IN-KA"), ("Kerala", "IN-KL"),
    ("Ladakh", "IN-LA"), ("Lakshadweep", "IN-LD"), ("Madhya Pradesh", "IN-MP"),
    ("Maharashtra", "IN-MH"), ("Manipur", "IN-MN"), ("Meghalaya", "IN-ML"),
    ("Mizoram", "IN-MZ"), ("Nagaland", "IN-NL"), ("Odisha", "IN-OR"),
    ("Puducherry", "IN-PY"), ("Punjab", "IN-PB"), ("Rajasthan", "IN-RJ"),
    ("Sikkim", "IN-SK"), ("Tamil Nadu", "IN-TN"), ("Telangana", "IN-TG"),
    ("Tripura", "IN-TR"), ("Uttar Pradesh", "IN-UP"), ("Uttarakhand", "IN-UT"),
    ("West Bengal", "IN-WB"),
]

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
CACHE_TTL = 600
_city_cache: dict[str, tuple[float, list[dict]]] = {}
_district_cache: dict[str, tuple[float, list[dict]]] = {}
_city_locks: dict[str, asyncio.Lock] = {}
_district_locks: dict[str, asyncio.Lock] = {}


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _region(state: str) -> dict | None:
    wanted = state.casefold().strip()
    for name, code in INDIA_REGIONS:
        if name.casefold() == wanted or code.casefold() == wanted:
            return {"name": name, "code": code}
    return None


async def _overpass(query: str) -> dict:
    last_error: Exception | None = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=70, headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"}) as client:
                response = await client.post(endpoint, data={"data": query})
                if response.status_code in (429, 502, 503, 504):
                    last_error = httpx.HTTPStatusError(f"Overpass {response.status_code}", request=response.request, response=response)
                    continue
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            last_error = exc
    raise HTTPException(status_code=503, detail="OpenStreetMap Overpass services are temporarily rate-limited or unavailable. Please retry shortly.") from last_error


@router.get("/states")
async def states():
    return [
        {"name": name, "code": code, "source": "Indian administrative list", "source_url": "https://www.indiacode.nic.in/"}
        for name, code in INDIA_REGIONS
    ]


async def _cities_for_state(state: str) -> list[dict]:
    selected = _region(state)
    if not selected:
        raise HTTPException(status_code=404, detail="State / Union Territory not found")
    code = selected["code"]
    query = f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;nwr(area.state)[place~"^(city|town)$"];out center tags;'
    data = await _overpass(query)
    rows, seen = [], set()
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = _clean(tags.get("name:en") or tags.get("name"))
        if not name or name.casefold() in seen:
            continue
        center = element.get("center") or {}
        lat = element.get("lat", center.get("lat")); lng = element.get("lon", center.get("lon"))
        if lat is None or lng is None:
            continue
        seen.add(name.casefold())
        rows.append({
            "name": name,
            "state": selected["name"],
            "place_type": tags.get("place"),
            "district": _clean(tags.get("addr:district")) or None,
            "lat": lat,
            "lng": lng,
            "source": "OpenStreetMap",
            "source_url": f"https://www.openstreetmap.org/{element.get('type')}/{element.get('id')}",
        })
    return sorted(rows, key=lambda x: x["name"].casefold())


@router.get("/cities")
async def cities(state: str):
    key = state.casefold().strip()
    now = time.monotonic()
    cached = _city_cache.get(key)
    if cached and now - cached[0] < CACHE_TTL:
        return cached[1]
    lock = _city_locks.setdefault(key, asyncio.Lock())
    async with lock:
        now = time.monotonic()
        cached = _city_cache.get(key)
        if cached and now - cached[0] < CACHE_TTL:
            return cached[1]
        result = await _cities_for_state(state)
        _city_cache[key] = (time.monotonic(), result)
        return result


async def _districts_for_state(state: str) -> list[dict]:
    selected = _region(state)
    if not selected:
        raise HTTPException(status_code=404, detail="State / Union Territory not found")
    code = selected["code"]
    query = f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level=6];out tags center;'
    data = await _overpass(query)
    rows, seen = [], set()
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = _clean(tags.get("name:en") or tags.get("name"))
        if not name or name.casefold() in seen:
            continue
        seen.add(name.casefold())
        center = element.get("center") or {}
        rows.append({
            "name": name,
            "state": selected["name"],
            "osm_relation_id": element.get("id"),
            "lat": center.get("lat"),
            "lng": center.get("lon"),
            "source": "OpenStreetMap",
            "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}",
        })
    if not rows:
        query = f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level=5];out tags center;'
        data = await _overpass(query)
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = _clean(tags.get("name:en") or tags.get("name"))
            if not name or name.casefold() in seen:
                continue
            seen.add(name.casefold())
            center = element.get("center") or {}
            rows.append({"name": name, "state": selected["name"], "osm_relation_id": element.get("id"), "lat": center.get("lat"), "lng": center.get("lon"), "source": "OpenStreetMap", "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}"})
    return sorted(rows, key=lambda x: x["name"].casefold())


@router.get("/districts")
async def districts(state: str, city: str | None = None):
    key = state.casefold().strip()
    now = time.monotonic()
    cached = _district_cache.get(key)
    if not cached or now - cached[0] >= CACHE_TTL:
        lock = _district_locks.setdefault(key, asyncio.Lock())
        async with lock:
            cached = _district_cache.get(key)
            if not cached or time.monotonic() - cached[0] >= CACHE_TTL:
                result = await _districts_for_state(state)
                _district_cache[key] = (time.monotonic(), result)
                cached = _district_cache[key]
    rows = cached[1]
    if city:
        city_l = city.casefold().strip()
        city_rows = _city_cache.get(key)
        matched = None
        if city_rows:
            matched = next((c for c in city_rows[1] if c["name"].casefold() == city_l and c.get("district")), None)
        if matched:
            district_l = matched["district"].casefold()
            exact = [r for r in rows if r["name"].casefold() == district_l]
            if exact:
                return exact
    return rows
