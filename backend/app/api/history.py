from __future__ import annotations
from fastapi import APIRouter
from app.data.synthetic import get_history, get_rainfall_trend, get_village
from app.data.open_data import get_ifi_flood_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/region/{region}")
async def region_history(region: str, district: str | None = None):
    try:
        data = await get_ifi_flood_history(region=region, district=district)
        return {
            "region": region,
            "district": district,
            "events": data.get("events", []),
            "count": data.get("count", 0),
            "source": data.get("source"),
            "source_url": data.get("source_url"),
            "dataset_period": data.get("dataset_period"),
            "updated_at": data.get("updated_at"),
            "error": data.get("error"),
        }
    except Exception as exc:
        return {
            "region": region,
            "district": district,
            "events": [],
            "count": 0,
            "source": "Historical Flood Inventory",
            "error": str(exc)[:100],
        }


@router.get("/{village_id}")
async def village_history(village_id: str):
    events = get_history(village_id)
    v = get_village(village_id)
    base_rain = v.get("rainfall_mm_month", 250) if v else 250
    trend = get_rainfall_trend(village_id, base_rainfall=base_rain)

    return {
        "village_id": village_id,
        "events": events,
        "rainfall_trend": trend,
        "source": "State Disaster Incident Database & Climatological Observation",
    }
