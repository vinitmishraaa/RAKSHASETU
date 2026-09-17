from fastapi import APIRouter, HTTPException
from app.data.live import get_live_settlements, enrich_settlements_with_weather

router = APIRouter(prefix="/api/villages", tags=["villages"])


async def _live(region: str | None = None, district: str | None = None):
    settlements = await get_live_settlements(region, district)
    return await enrich_settlements_with_weather(settlements)


@router.get("")
async def list_villages(
    region: str | None = None,
    state: str | None = None,
    district: str | None = None,
    level: str | None = None,
):
    region = state or region
    villages = await _live(region, district)
    if district:
        villages = [v for v in villages if not v.get("district") or v.get("district", "").casefold() == district.casefold()]
    if level:
        villages = [v for v in villages if v.get("level", "").casefold() == level.casefold()]
    return villages


@router.get("/{village_id}")
async def get_village(village_id: str, region: str | None = None, state: str | None = None, district: str | None = None):
    villages = await _live(state or region, district)
    village = next((v for v in villages if v["id"] == village_id), None)
    if not village:
        raise HTTPException(status_code=404, detail="Live settlement not found")
    return {
        **village,
        "reasons": [
            "Risk indicator is calculated from the live weather and USGS earthquake observations returned with this record.",
            "Population is shown only when an OpenStreetMap population tag is available.",
        ],
        "recommended_action": "Use official government alerts and local authorities for operational decisions.",
        "history": [],
        "rainfall_trend": [],
        "data_status": "live-open-data",
    }
