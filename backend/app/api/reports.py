from __future__ import annotations
from fastapi import APIRouter, Query
from app.data.geo_catalog import get_villages_for_scope
from app.data.administrative import INDIA_STATES
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/overview")
def overview_report(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
):
    """Aggregate analytics report for decision intelligence."""
    target_state = state or region
    villages = get_villages_for_scope(state=target_state, district=district)

    rows = []
    for v in villages:
        indicators = compute_risk(v)
        cls = classify(indicators["risk_score"])
        rows.append({
            "village_id": v["id"],
            "name": v["name"],
            "district": v.get("district"),
            "state": v.get("state"),
            "population": v.get("population", 0),
            "risk_score": indicators["risk_score"],
            "level": cls["level"],
        })

    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    population_at_risk = 0
    for r in rows:
        counts[r["level"]] += 1
        if r["level"] in ("CRITICAL", "HIGH"):
            population_at_risk += r["population"]

    by_region = []
    state_names = [s["name"] for s in INDIA_STATES]
    for name in state_names:
        region_rows = [r for r in rows if r["state"] == name]
        if region_rows:
            by_region.append({
                "region": name,
                "villages": len(region_rows),
                "population": sum(r["population"] for r in region_rows),
                "avg_risk": round(sum(r["risk_score"] for r in region_rows) / len(region_rows), 1),
                "critical": sum(r["level"] == "CRITICAL" for r in region_rows),
                "high": sum(r["level"] == "HIGH" for r in region_rows),
            })

    by_district: dict[str, dict] = {}
    for r in rows:
        dist_name = r.get("district") or "Unknown"
        d = by_district.setdefault(dist_name, {
            "district": dist_name,
            "region": r["state"],
            "population": 0,
            "villages": 0,
            "avg_risk": 0.0,
        })
        d["population"] += r["population"]
        d["villages"] += 1
        d["avg_risk"] += r["risk_score"]

    for d in by_district.values():
        d["avg_risk"] = round(d["avg_risk"] / max(d["villages"], 1), 1)

    return {
        "scope": target_state or "India",
        "district": district,
        "villages": rows,
        "by_region": by_region,
        "by_district": list(by_district.values()),
        "counts": counts,
        "population_at_risk": population_at_risk,
    }
