from fastapi import APIRouter, HTTPException
from app.data.live import get_live_shelters

router = APIRouter(prefix="/api/safesites", tags=["safe sites"])


@router.get("")
async def list_sites(region: str | None = None):
    return await get_live_shelters(region)


@router.get("/{site_id}")
async def get_site(site_id: str, region: str | None = None):
    sites = await get_live_shelters(region)
    site = next((s for s in sites if s["id"] == site_id), None)
    if not site:
        raise HTTPException(status_code=404, detail="Mapped shelter not found")
    return site


@router.get("/rank-for/{village_id}")
async def rank_for_village(village_id: str, region: str | None = None):
    # Capacity-aware ranking requires verified operational capacity/occupancy data.
    # Do not invent those quantities from map tags.
    return {"available": False, "reason": "Capacity and occupancy are not available from the open shelter mapping; ranking is disabled until verified operational data is supplied.", "village_id": village_id, "sites": await get_live_shelters(region)}
