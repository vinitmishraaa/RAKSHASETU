from __future__ import annotations

from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/api/regions", tags=["regions"])

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
INDIA_AREA_QUERY = (
    '[out:json][timeout:60];'
    'area["ISO3166-1"="IN"][boundary=administrative]->.india;'
    'relation(area.india)[boundary=administrative][admin_level=4];'
    'out tags center;'
)


def _clean(value: str | None) -> str:
    return (value or "").strip()


async def _overpass(query: str) -> dict:
    async with httpx.AsyncClient(
        timeout=70,
        headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"},
    ) as client:
        response = await client.post(OVERPASS_URL, data={"data": query})
        response.raise_for_status()
        return response.json()


async def _state_relations() -> list[dict]:
    data = await _overpass(INDIA_AREA_QUERY)
    states = []
    seen = set()
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = _clean(tags.get("name:en") or tags.get("name"))
        if not name or name in seen:
            continue
        seen.add(name)
        code = _clean(tags.get("ISO3166-2"))
        center = element.get("center") or {}
        states.append(
            {
                "name": name,
                "code": code or None,
                "osm_relation_id": element.get("id"),
                "lat": center.get("lat"),
                "lng": center.get("lon"),
                "source": "OpenStreetMap",
                "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}",
            }
        )
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
    selected = next(
        (s for s in states_data if s["name"].casefold() == state.casefold() or s["code"] == state),
        None,
    )
    if not selected:
        raise HTTPException(status_code=404, detail="State not found in OpenStreetMap administrative data")

    relation_id = selected["osm_relation_id"]
    query = (
        f'[out:json][timeout:60];'
        f'relation({relation_id})[boundary=administrative]->.state;'
        f'relation(area.state)[boundary=administrative][admin_level=6];'
        f'out tags center;'
    )
    data = await _overpass(query)
    districts_data = []
    seen = set()
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = _clean(tags.get("name:en") or tags.get("name"))
        if not name or name.casefold() in seen:
            continue
        seen.add(name.casefold())
        center = element.get("center") or {}
        districts_data.append(
            {
                "name": name,
                "state": selected["name"],
                "osm_relation_id": element.get("id"),
                "lat": center.get("lat"),
                "lng": center.get("lon"),
                "source": "OpenStreetMap",
                "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}",
            }
        )

    # A few Indian administrative mappings still use level 5 in OSM. Only
    # use that level when the normal district level has no result.
    if not districts_data:
        query = (
            f'[out:json][timeout:60];'
            f'relation({relation_id})[boundary=administrative]->.state;'
            f'relation(area.state)[boundary=administrative][admin_level=5];'
            f'out tags center;'
        )
        data = await _overpass(query)
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = _clean(tags.get("name:en") or tags.get("name"))
            if not name or name.casefold() in seen:
                continue
            seen.add(name.casefold())
            center = element.get("center") or {}
            districts_data.append(
                {
                    "name": name,
                    "state": selected["name"],
                    "osm_relation_id": element.get("id"),
                    "lat": center.get("lat"),
                    "lng": center.get("lon"),
                    "source": "OpenStreetMap",
                    "source_url": f"https://www.openstreetmap.org/relation/{element.get('id')}",
                }
            )

    return sorted(districts_data, key=lambda x: x["name"].lower())
