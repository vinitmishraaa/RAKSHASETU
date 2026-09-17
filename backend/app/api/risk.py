from __future__ import annotations
from fastapi import APIRouter, Query
from app.data.live import get_live_settlements

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/summary")
async def risk_summary(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
    city: str | None = Query(default=None),
):
    """Returns aggregated risk snapshot and population metrics for the selected scope."""
    st = state or region
    villages = await get_live_settlements(state=st, district=district, city=city)

    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    total_pop = 0
    pop_at_risk = 0
    total_score = 0.0

    for v in villages:
        lvl = v.get("level", "LOW")
        counts[lvl] = counts.get(lvl, 0) + 1
        pop = v.get("population") or 0
        total_pop += pop
        if lvl in ("CRITICAL", "HIGH"):
            pop_at_risk += pop
        total_score += float(v.get("risk_score") or 0.0)

    avg_score = round(total_score / max(len(villages), 1), 1)

    return {
        "total_villages": len(villages),
        "counts": counts,
        "population_at_risk": pop_at_risk,
        "known_population_records": total_pop,
        "average_risk_score": avg_score,
        "data_status": "realtime-open-data",
        "scope": {"state": st, "district": district, "city": city},
        "note": "Operational risk calculated transparently from physical exposure, population vulnerability, and live Open-Meteo weather and USGS earthquake signals.",
    }
