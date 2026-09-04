from fastapi import APIRouter, HTTPException
from app.data import synthetic

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/{village_id}")
def village_history(village_id: str):
    village = synthetic.get_village(village_id)
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return {
        "village_id": village_id,
        "events": synthetic.get_history(village_id),
        "rainfall_trend": synthetic.get_rainfall_trend(village_id),
    }
