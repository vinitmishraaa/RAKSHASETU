from fastapi import APIRouter
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/summary")
def risk_summary():
    villages = synthetic.get_villages()
    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    total_population_at_risk = 0
    for v in villages:
        indicators = compute_risk(v)
        cls = classify(indicators["risk_score"])
        counts[cls["level"]] += 1
        if cls["level"] in ("CRITICAL", "HIGH"):
            total_population_at_risk += v["population"]

    return {
        "total_villages": len(villages),
        "counts": counts,
        "population_at_risk": total_population_at_risk,
    }
