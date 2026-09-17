from __future__ import annotations

from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/api/regions", tags=["regions"])
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
INDIA_AREA_QUERY = '[out:json][timeout:60];area["ISO3166-1"="IN"][boundary=administrative]->.india;relation(area.india)[boundary=administrative][admin_level=4];out tags center;'


def _clean(value: str | None) -> str:
    return (value or "").strip()


async def _overpass(query: str) -> dict:
    async with httpx.AsyncClient(timeout=70, headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"}) as client:
        response = await client.post(OVERPASS_URL, data={"data": query})
        response.raise_for_status()
        return response.json()


async def _state_relations() -> list[dict]:
    data = await _overpass(INDIA_AREA_QUERY)
    states, seen = [], set()
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = _clean(tags.get("name:en") or tags.get("name"))
        if not name or name.casefold() in seen:
            continue
        seen.add(name.casefold())
        center = element.get("center") or {}
        states.append({
            "name": name,
            "code": _clean(tags.get("ISO3166-2")) or None,
            "osm_relation_id": element.get("id"),
            "lat": center.get("lat"), "lng": center.get("lon"),
            "source": "OpenStreetMap",
            "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}",
        })
    return sorted(states, key=lambda x: x["name"].lower())


@router.get("/states")
async def states():
    return await _state_relations()


@router.get("/districts")
async def districts(state: str):
    state = _clean(state)
    if not state:
        raise HTTPException(status_code=400, detail="state is required")
    states_data = await _state_relations()
    selected = next((s for s in states_data if s["name"].casefold() == state.casefold() or s["code"] == state), None)
    if not selected:
        raise HTTPException(status_code=404, detail="State not found in OpenStreetMap administrative data")

    code = selected["code"]
    if not code:
        raise HTTPException(status_code=404, detail="State has no OpenStreetMap ISO code")
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
