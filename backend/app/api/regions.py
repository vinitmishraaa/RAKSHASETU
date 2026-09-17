from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from app.data.administrative import (
    get_states,
    get_districts_for_state,
    get_cities_for_district,
)

router = APIRouter(prefix="/api/regions", tags=["regions"])


@router.get("/states")
async def states():
    """Returns all 36 States and Union Territories of India."""
    return get_states()


@router.get("/districts")
async def districts(state: str = Query(..., min_length=2)):
    """Returns official districts belonging to the selected State or UT."""
    results = get_districts_for_state(state)
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"State / Union Territory '{state}' not found. Please select a valid state from India."
        )
    return results


@router.get("/cities")
async def cities(state: str = Query(..., min_length=2), district: str = Query(..., min_length=1)):
    """Returns cities / towns belonging to the selected district."""
    results = get_cities_for_district(state, district)
    return results
