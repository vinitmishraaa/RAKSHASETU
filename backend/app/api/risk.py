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
    relocation_tiers = {"IMMEDIATE": 0, "SHORT_TERM": 0, "MEDIUM_TERM": 0}
    population_by_tier = {"IMMEDIATE": 0, "SHORT_TERM": 0, "MEDIUM_TERM": 0}
    red_zones_count = 0
    total_pop = 0
    pop_at_risk = 0
    total_score = 0.0

    flood_total = 0.0
    landslide_total = 0.0
    coastal_erosion_total = 0.0
    cloudburst_total = 0.0

    for v in villages:
        lvl = v.get("level", "LOW")
        counts[lvl] = counts.get(lvl, 0) + 1
        tier = v.get("relocation_tier", "MEDIUM_TERM")
        relocation_tiers[tier] = relocation_tiers.get(tier, 0) + 1

        pop = v.get("population") or 0
        total_pop += pop
        population_by_tier[tier] = population_by_tier.get(tier, 0) + pop

        if lvl in ("CRITICAL", "HIGH"):
            pop_at_risk += pop
        total_score += float(v.get("risk_score") or 0.0)

        if v.get("is_red_zone"):
            red_zones_count += 1

        flood_total += float(v.get("flood_hazard") or 0.0)
        landslide_total += float(v.get("landslide_hazard") or 0.0)
        coastal_erosion_total += float(v.get("coastal_erosion_hazard") or 0.0)
        cloudburst_total += float(v.get("cloudburst_hazard") or 0.0)

    n_v = max(len(villages), 1)
    avg_score = round(total_score / n_v, 1)

    return {
        "total_villages": len(villages),
        "counts": counts,
        "red_zones_count": red_zones_count,
        "relocation_tiers": relocation_tiers,
        "population_by_tier": population_by_tier,
        "population_at_risk": pop_at_risk,
        "known_population_records": total_pop,
        "average_risk_score": avg_score,
        "hazard_breakdown_avg": {
            "flood": round(flood_total / n_v, 1),
            "landslide": round(landslide_total / n_v, 1),
            "coastal_erosion": round(coastal_erosion_total / n_v, 1),
            "cloudburst": round(cloudburst_total / n_v, 1),
        },
        "data_status": "realtime-open-data",
        "scope": {"state": st, "district": district, "city": city},
        "note": "Operational risk calculated transparently from physical exposure, population vulnerability, and live Open-Meteo weather and USGS earthquake signals.",
    }
