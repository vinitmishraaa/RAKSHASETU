from fastapi import APIRouter, HTTPException
from app.data import synthetic
from app.optimization.capacity import available_capacity
from app.optimization.site_scoring import rank_sites

router = APIRouter(prefix="/api/safesites", tags=["safe sites"])


def _enrich(site: dict) -> dict:
    return {**site, "available_capacity": available_capacity(site)}


@router.get("")
def list_sites():
    return [_enrich(s) for s in synthetic.get_safe_sites()]


@router.get("/{site_id}")
def get_site(site_id: str):
    site = synthetic.get_safe_site(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Safe site not found")
    return _enrich(site)


@router.get("/rank-for/{village_id}")
def rank_for_village(village_id: str):
    village = synthetic.get_village(village_id)
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return rank_sites(village, synthetic.get_safe_sites())
