from fastapi import APIRouter, Query
from app.data.open_data import route_osrm

router = APIRouter(prefix="/api/routing", tags=["routing"])


@router.get("/route")
async def route(
    start_lat: float = Query(...),
    start_lng: float = Query(...),
    end_lat: float = Query(...),
    end_lng: float = Query(...),
):
    return await route_osrm(start_lat, start_lng, end_lat, end_lng)
