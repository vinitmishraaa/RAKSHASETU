from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from app.data.live import get_live_shelters, get_live_settlements
from app.data.synthetic import get_safe_site as catalog_safe_site, get_village as catalog_village
from app.optimization.site_scoring import rank_sites

router = APIRouter(prefix="/api/safesites", tags=["safe sites"])


@router.get("")
async def list_sites(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Returns safe emergency shelters for the selected state/district/city."""
    st = state or region
    sites = await get_live_shelters(state=st, district=district, city=city)
    if district:
        sites = [s for s in sites if (s.get("district") or "").casefold() == district.strip().casefold()]
    if city:
        sites = [s for s in sites if (s.get("city") or "").casefold() == city.strip().casefold()]
    return sites


@router.get("/rank-for/{village_id}")
async def rank_for_village(
    village_id: str,
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Ranks safe shelters for a specific village using multi-criteria optimization."""
    st = state or region
    villages = await get_live_settlements(state=st, district=district, city=city)
    village = next((v for v in villages if v["id"] == village_id), None) or catalog_village(village_id)
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")

    v_state = village.get("state") or st
    v_district = village.get("district") or district
    sites = await get_live_shelters(state=v_state, district=v_district)
    if not sites:
        sites = await get_live_shelters(state=v_state)

    ranked = rank_sites(village, sites)
    return {
        "available": True,
        "village_id": village_id,
        "village_name": village.get("name"),
        "ranked_sites": ranked,
    }


@router.get("/{site_id}")
async def get_site(
    site_id: str,
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Returns single safe shelter details."""
    st = state or region
    sites = await get_live_shelters(state=st, district=district, city=city)
    site = next((s for s in sites if s["id"] == site_id), None) or catalog_safe_site(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Safe shelter not found")
    return site
