from fastapi import APIRouter
from app.data.open_data import get_ifi_flood_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/region/{region}")
async def region_history(region: str, district: str | None = None):
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


@router.get("/{village_id}")
async def village_history(village_id: str):
    # Village-level historical attribution is not invented when IFI does not
    # provide a reliable village identifier. The UI receives an explicit empty
    # event list instead of fabricated history.
    return {
        "village_id": village_id,
        "events": [],
        "rainfall_trend": [],
        "source": "IFI-Impacts",
        "source_url": "https://zenodo.org/records/16994648",
        "note": "IFI-Impacts is a national flood inventory. Village-level history is not inferred without a verified identifier.",
    }
