from fastapi import APIRouter
from app.data import synthetic
from app.data.districts import TARGET_REGIONS
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/overview")
def overview_report(region: str | None = None):
    """Aggregate analytics feed for dashboard and regional comparison."""
    villages = synthetic.get_villages()
    if region:
        villages = [v for v in villages if v["state"].lower() == region.lower()]

    rows = []
    for v in villages:
        indicators = compute_risk(v)
        cls = classify(indicators["risk_score"])
        rows.append({
            "village_id": v["id"], "name": v["name"], "district": v["district"],
            "state": v["state"], "population": v["population"],
            "risk_score": indicators["risk_score"], "level": cls["level"],
        })

    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    population_at_risk = 0
    for r in rows:
        counts[r["level"]] += 1
        if r["level"] in ("CRITICAL", "HIGH"):
            population_at_risk += r["population"]

    by_region = []
    for name in TARGET_REGIONS:
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
        d = by_district.setdefault(r["district"], {"district": r["district"], "region": r["state"], "population": 0, "villages": 0, "avg_risk": 0})
        d["population"] += r["population"]
        d["villages"] += 1
        d["avg_risk"] += r["risk_score"]
    for d in by_district.values():
        d["avg_risk"] = round(d["avg_risk"] / d["villages"], 1)

    return {
        "scope": region or "All target regions",
        "villages": rows,
        "by_region": by_region,
        "by_district": list(by_district.values()),
        "counts": counts,
        "population_at_risk": population_at_risk,
        "total_villages": len(rows),
    }
