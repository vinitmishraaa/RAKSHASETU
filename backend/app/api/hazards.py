from fastapi import APIRouter
from app.data import synthetic

router = APIRouter(prefix="/api/hazards", tags=["hazards"])


@router.get("")
def list_hazards():
    """Raw hazard layer values per village (flood/cyclone/landslide) -
    stands in for the GIS hazard raster layers described in the doc."""
    return [
        {
            "village_id": v["id"],
            "name": v["name"],
            "flood_hazard": v["flood_hazard"],
            "cyclone_hazard": v["cyclone_hazard"],
            "landslide_hazard": v["landslide_hazard"],
            "rainfall_mm_month": v["rainfall_mm_month"],
        }
        for v in synthetic.get_villages()
    ]
