from fastapi import APIRouter, HTTPException
from app.data import synthetic
from app.optimization.relocation import build_relocation_plan
from app.optimization.site_scoring import rank_sites
from app.optimization.routing import route_between

router = APIRouter(prefix="/api/relocation", tags=["relocation"])


@router.get("/plan/{village_id}")
def relocation_plan(village_id: str):
    village = synthetic.get_village(village_id)
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")

    sites = synthetic.get_safe_sites()
    plan = build_relocation_plan(village, sites)
    ranked = rank_sites(village, sites)

    return {
        "village_id": village["id"],
        "village_name": village["name"],
        "population": plan["population"],
        "best_site": plan["best_site"],
        "ranked_sites": ranked,
        "allocations": plan["allocations"],
        "fully_covered": plan["fully_covered"],
        "reason": plan["reason"],
    }


@router.get("/route/{village_id}/{site_id}")
def relocation_route(village_id: str, site_id: str):
    village = synthetic.get_village(village_id)
    site = synthetic.get_safe_site(site_id)
    if not village or not site:
        raise HTTPException(status_code=404, detail="Village or site not found")
    return route_between(village, site)


@router.get("/plans")
def all_plans():
    sites = synthetic.get_safe_sites()
    plans = []
    for village in synthetic.get_villages():
        plan = build_relocation_plan(village, sites)
        plans.append(
            {
                "village_id": village["id"],
                "village_name": village["name"],
                "population": plan["population"],
                "best_site": plan["best_site"],
                "allocations": plan["allocations"],
                "fully_covered": plan["fully_covered"],
                "reason": plan["reason"],
            }
        )
    return plans
