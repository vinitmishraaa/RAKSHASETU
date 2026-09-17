from fastapi import APIRouter, HTTPException
from app.data.live import get_live_settlements, get_live_shelters
from app.optimization.site_scoring import haversine_km
from app.optimization.routing import route_between

router = APIRouter(prefix="/api/relocation", tags=["relocation"])

def _rank_by_distance(village, sites):
    ranked=[]
    for site in sites:
        distance=round(haversine_km(village["lat"],village["lng"],site["lat"],site["lng"]),1)
        ranked.append({"site_id":site["id"],"site_name":site["name"],"distance_km":distance,"capacity":site.get("capacity"),"current_occupancy":site.get("current_occupancy"),"available_capacity":site.get("available_capacity"),"facilities":site.get("facilities",[]),"source":site.get("source"),"verified":site.get("verified",False),"selection_basis":"Distance only; shelter capacity, occupancy and operational status are not published/verified."})
    return sorted(ranked,key=lambda x:x["distance_km"])[:8]

@router.get("/plan/{village_id}")
async def relocation_plan(village_id: str, region: str | None = None, district: str | None = None, city: str | None = None):
    villages = await get_live_settlements(region, district, city); sites = await get_live_shelters(region, district, city)
    village = next((v for v in villages if v["id"] == village_id), None)
    if not village: raise HTTPException(status_code=404, detail="Live settlement not found in the selected location")
    ranked = _rank_by_distance(village, sites)
    return {"village_id": village["id"],"village_name": village["name"],"population": village.get("population"),"best_site": ranked[0] if ranked else None,"ranked_sites": ranked,"allocations":[],"fully_covered":False,"reason":"Safe sites are ranked by live geographic distance only. No capacity-based allocation is claimed because OpenStreetMap does not publish verified operational capacity/occupancy for these mapped shelters.","guided_flow":["Confirm the danger location on the map.","Choose a mapped shelter after checking its current operational status with the local authority.","Open the road-network route from the selected settlement to the chosen shelter.","Follow the live navigation link and official emergency instructions."],"scope":{"region":region,"district":district,"city":city}}

@router.get("/route/{village_id}/{site_id}")
async def relocation_route(village_id: str, site_id: str, region: str | None = None, district: str | None = None, city: str | None = None):
    villages = await get_live_settlements(region, district, city); sites = await get_live_shelters(region, district, city)
    village = next((v for v in villages if v["id"] == village_id), None); site = next((s for s in sites if s["id"] == site_id), None)
    if not village or not site: raise HTTPException(status_code=404, detail="Live settlement or mapped shelter not found in the selected location")
    return await route_between(village, site)

@router.get("/plans")
async def all_plans(region: str | None = None, district: str | None = None, city: str | None = None):
    villages = await get_live_settlements(region, district, city); sites = await get_live_shelters(region, district, city)
    return [{"village_id": v["id"],"village_name": v["name"],"population": v.get("population"),"best_site": (_rank_by_distance(v,sites) or [None])[0],"ranked_sites":_rank_by_distance(v,sites),"allocations":[],"fully_covered":False,"reason":"Distance-ranked mapped shelters only; operational capacity is not verified."} for v in villages]
