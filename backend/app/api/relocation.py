from fastapi import APIRouter, HTTPException
from app.data.live import get_live_settlements, get_live_shelters
from app.optimization.routing import route_between

router = APIRouter(prefix="/api/relocation", tags=["relocation"])

@router.get("/plan/{village_id}")
async def relocation_plan(village_id: str, region: str | None = None):
    villages = await get_live_settlements(region); sites = await get_live_shelters(region)
    village = next((v for v in villages if v["id"] == village_id), None)
    if not village: raise HTTPException(status_code=404, detail="Live settlement not found")
    return {"village_id": village["id"], "village_name": village["name"], "population": village.get("population"), "best_site": None, "ranked_sites": [], "allocations": [], "fully_covered": False, "reason": "Capacity-aware allocation is disabled because OpenStreetMap does not provide verified operational shelter capacity or occupancy. Choose a mapped shelter and verify it with the local authority before relocation."}

@router.get("/route/{village_id}/{site_id}")
async def relocation_route(village_id: str, site_id: str, region: str | None = None):
    villages = await get_live_settlements(region); sites = await get_live_shelters(region)
    village = next((v for v in villages if v["id"] == village_id), None); site = next((s for s in sites if s["id"] == site_id), None)
    if not village or not site: raise HTTPException(status_code=404, detail="Live settlement or mapped shelter not found")
    return await route_between(village, site)

@router.get("/plans")
async def all_plans(region: str | None = None):
    villages = await get_live_settlements(region)
    return [{"village_id": v["id"], "village_name": v["name"], "population": v.get("population"), "best_site": None, "allocations": [], "fully_covered": False, "reason": "Capacity data not verified."} for v in villages]
