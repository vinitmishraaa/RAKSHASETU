from fastapi import APIRouter
from app.data.live import get_live_settlements, enrich_settlements_with_weather

router = APIRouter(prefix="/api/risk", tags=["risk"])

@router.get("/summary")
async def risk_summary(region: str | None = None, district: str | None = None):
    villages = await enrich_settlements_with_weather(await get_live_settlements(region, district))
    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    population_at_risk = None
    known_population = 0
    for village in villages:
        level = village.get("level", "LOW")
        counts[level] = counts.get(level, 0) + 1
        if village.get("population") is not None:
            known_population += village["population"]
            if level in ("CRITICAL", "HIGH"):
                population_at_risk = (population_at_risk or 0) + village["population"]
    return {"total_villages": len(villages), "counts": counts, "population_at_risk": population_at_risk, "known_population_records": known_population, "data_status": "live-open-data", "scope": {"region": region, "district": district}, "note": "Risk is a live operational indicator calculated from current Open-Meteo precipitation/wind and USGS earthquake magnitude/distance. It is not an official government hazard rating. Population totals use only published OpenStreetMap population tags."}
