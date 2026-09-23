from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from app.data.live import get_live_settlements, get_live_shelters
from app.data.synthetic import get_village as catalog_village, get_safe_site as catalog_safe_site
from app.optimization.site_scoring import rank_sites
from app.optimization.relocation import build_relocation_plan
from app.optimization.routing import route_between

router = APIRouter(prefix="/api/relocation", tags=["relocation"])


@router.get("/plan/{village_id}")
async def relocation_plan(
    village_id: str,
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Computes an optimized, capacity-aware relocation plan with a guided official path."""
    st = state or region
    villages = await get_live_settlements(state=st, district=district, city=city)
    village = next((v for v in villages if v["id"] == village_id), None) or catalog_village(village_id)
    if not village:
        raise HTTPException(status_code=404, detail="Village / settlement not found")

    v_state = village.get("state") or st
    v_district = village.get("district") or district
    sites = await get_live_shelters(state=v_state, district=v_district)
    if not sites:
        sites = await get_live_shelters(state=v_state)

    plan = build_relocation_plan(village, sites)
    ranked = rank_sites(village, sites)

    # Guided path instructions for disaster officers
    guided_flow = [
        {"step": 1, "title": "Verify Danger Zone", "action": f"Confirm operational perimeter for {village.get('name')} (Risk Level: {village.get('level', 'CRITICAL')})."},
        {"step": 2, "title": "Review Designated Shelter", "action": f"Verify intake capacity at primary destination ({plan.get('best_site', {}).get('site_name', 'Designated Shelter')})."},
        {"step": 3, "title": "Calculate Road Evacuation Corridor", "action": "Generate turn-by-turn road route and evaluate any flooded low-lying bridges."},
        {"step": 4, "title": "Issue Official Dispatch / Hand-off", "action": "Hand off route guidance to field vehicles; officials may execute or modify based on local ground conditions."},
    ]

    return {
        "village_id": village["id"],
        "village_name": village.get("name"),
        "population": village.get("population", 0),
        "best_site": plan.get("best_site"),
        "ranked_sites": ranked,
        "allocations": plan.get("allocations", []),
        "fully_covered": plan.get("fully_covered", True),
        "reason": plan.get("reason"),
        "carrying_capacity_assessment": plan.get("carrying_capacity_assessment"),
        "relocation_tier": village.get("relocation_tier", "IMMEDIATE"),
        "relocation_horizon": village.get("relocation_horizon", "0–48 Hours"),
        "is_red_zone": village.get("is_red_zone", True),
        "red_zone_declaration": village.get("red_zone_declaration", "DECLARED MULTI-HAZARD RED ZONE — UNSUITABLE FOR PERMANENT HABITATION"),
        "primary_hazard_trigger": village.get("primary_hazard_trigger", "Multi-hazard Vulnerability"),
        "guided_flow": guided_flow,
        "advisory_note": "RakshaSetu provides an algorithmic decision-support recommendation to assist disaster authorities. Officials maintain full discretion to adapt routes based on real-time field situations.",
        "scope": {"state": v_state, "district": v_district, "city": city},
    }


@router.get("/route/{village_id}/{site_id}")
async def relocation_route(
    village_id: str,
    site_id: str,
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Generates a live road-network route between origin village and destination safe site."""
    st = state or region
    villages = await get_live_settlements(state=st, district=district, city=city)
    village = next((v for v in villages if v["id"] == village_id), None) or catalog_village(village_id)

    sites = await get_live_shelters(state=st, district=district, city=city)
    site = next((s for s in sites if s["id"] == site_id), None) or catalog_safe_site(site_id)

    if not village or not site:
        raise HTTPException(status_code=404, detail="Origin village or destination safe site not found")

    return await route_between(village, site)


@router.get("/plans")
async def all_plans(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Returns relocation summaries for all villages in scope."""
    st = state or region
    villages = await get_live_settlements(state=st, district=district, city=city)
    sites = await get_live_shelters(state=st, district=district, city=city)
    plans = []
    for v in villages:
        plan = build_relocation_plan(v, sites)
        plans.append({
            "village_id": v["id"],
            "village_name": v.get("name"),
            "population": v.get("population"),
            "best_site": plan.get("best_site"),
            "allocations": plan.get("allocations"),
            "fully_covered": plan.get("fully_covered"),
            "reason": plan.get("reason"),
        })
    return plans
