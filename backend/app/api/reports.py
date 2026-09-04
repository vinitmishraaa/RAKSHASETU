from fastapi import APIRouter
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/overview")
def overview_report():
    """Aggregate analytics feed for the Analytics page charts."""
    villages = synthetic.get_villages()
    rows = []
    for v in villages:
        indicators = compute_risk(v)
        cls = classify(indicators["risk_score"])
        rows.append(
            {
                "village_id": v["id"],
                "name": v["name"],
                "district": v["district"],
                "population": v["population"],
                "risk_score": indicators["risk_score"],
                "level": cls["level"],
            }
        )

    by_district: dict[str, dict] = {}
    for r in rows:
        d = by_district.setdefault(r["district"], {"district": r["district"], "population": 0, "villages": 0})
        d["population"] += r["population"]
        d["villages"] += 1

    return {
        "villages": rows,
        "by_district": list(by_district.values()),
    }
