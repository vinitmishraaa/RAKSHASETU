from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from app.data.live import get_live_settlements
from app.data.synthetic import get_village as catalog_village

router = APIRouter(prefix="/api/villages", tags=["villages"])


@router.get("")
async def list_villages(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
    level: str | None = Query(default=None),
):
    """Returns settlements for the selected state/district/city enriched with live data."""
    st = state or region
    villages = await get_live_settlements(state=st, district=district, city=city)

    if district:
        villages = [v for v in villages if (v.get("district") or "").casefold() == district.strip().casefold()]
    if city:
        villages = [v for v in villages if (v.get("city") or "").casefold() == city.strip().casefold()]
    if level:
        villages = [v for v in villages if (v.get("level") or "").casefold() == level.strip().casefold()]

    return villages


@router.get("/{village_id}")
async def get_village(
    village_id: str,
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Returns single settlement details enriched with reasons, history, and rainfall trend."""
    st = state or region
    # Look up in scoped live settlements first
    villages = await get_live_settlements(state=st, district=district, city=city)
    village = next((v for v in villages if v["id"] == village_id), None)

    if not village:
        # Fallback to catalog
        cat_v = catalog_village(village_id)
        if not cat_v:
            raise HTTPException(status_code=404, detail=f"Settlement '{village_id}' not found")
        # Enrich the single record
        enriched = await get_live_settlements(state=cat_v.get("state"), district=cat_v.get("district"))
        village = next((v for v in enriched if v["id"] == village_id), None) or cat_v

    return village
