from __future__ import annotations

import asyncio
import time
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/api/regions", tags=["regions"])
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
CACHE_TTL = 600
INDIA_AREA_QUERY = '[out:json][timeout:60];area["ISO3166-1"="IN"][boundary=administrative]->.india;relation(area.india)[boundary=administrative][admin_level=4];out tags center;'
_state_cache: tuple[float, list[dict]] | None = None
_district_cache: dict[str, tuple[float, list[dict]]] = {}
_state_lock = asyncio.Lock()
_district_locks: dict[str, asyncio.Lock] = {}


def _clean(value: str | None) -> str:
    return (value or "").strip()


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


async def _state_relations() -> list[dict]:
    global _state_cache
    now = time.monotonic()
    if _state_cache and now - _state_cache[0] < CACHE_TTL:
        return _state_cache[1]
    async with _state_lock:
        now = time.monotonic()
        if _state_cache and now - _state_cache[0] < CACHE_TTL:
            return _state_cache[1]
        data = await _overpass(INDIA_AREA_QUERY)
        states, seen = [], set()
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = _clean(tags.get("name:en") or tags.get("name"))
            if not name or name.casefold() in seen:
                continue
            seen.add(name.casefold())
            center = element.get("center") or {}
            states.append({"name": name, "code": _clean(tags.get("ISO3166-2")) or None, "osm_relation_id": element.get("id"), "lat": center.get("lat"), "lng": center.get("lon"), "source": "OpenStreetMap", "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}"})
        result = sorted(states, key=lambda x: x["name"].lower())
        _state_cache = (time.monotonic(), result)
        return result


@router.get("/states")
async def states():
    return await _state_relations()


async def _districts_for_state(state: str) -> list[dict]:
    code = next((s["code"] for s in await _state_relations() if s["name"].casefold() == state.casefold() or s["code"] == state), None)
    selected = next((s for s in await _state_relations() if s["name"].casefold() == state.casefold() or s["code"] == state), None)
    if not selected or not code:
        raise HTTPException(status_code=404, detail="State not found in OpenStreetMap administrative data")
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
        rows.append({"name": name, "state": selected["name"], "osm_relation_id": element.get("id"), "lat": center.get("lat"), "lng": center.get("lon"), "source": "OpenStreetMap", "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}"})
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
    return sorted(rows, key=lambda x: x["name"].lower())


@router.get("/districts")
async def districts(state: str):
    key = state.casefold().strip()
    now = time.monotonic()
    cached = _district_cache.get(key)
    if cached and now - cached[0] < CACHE_TTL:
        return cached[1]
    lock = _district_locks.setdefault(key, asyncio.Lock())
    async with lock:
        now = time.monotonic()
        cached = _district_cache.get(key)
        if cached and now - cached[0] < CACHE_TTL:
            return cached[1]
        result = await _districts_for_state(state)
        _district_cache[key] = (time.monotonic(), result)
        return result
