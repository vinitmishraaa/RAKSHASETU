from fastapi import APIRouter, HTTPException
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.risk_engine.vulnerability import accessibility_score
from app.risk_engine.explainability import explain, recommended_action

router = APIRouter(prefix="/api/villages", tags=["villages"])


def _enrich(village: dict) -> dict:
    indicators = compute_risk(village)
    cls = classify(indicators["risk_score"])
    return {
        **village,
        **indicators,
        "accessibility": accessibility_score(village),
        "level": cls["level"],
        "color": cls["color"],
    }


@router.get("")
def list_villages(
    district: str | None = None,
    level: str | None = None,
    min_population: int | None = None,
):
    villages = [_enrich(v) for v in synthetic.get_villages()]
    if district:
        villages = [v for v in villages if v["district"].lower() == district.lower()]
    if level:
        villages = [v for v in villages if v["level"].lower() == level.lower()]
    if min_population:
        villages = [v for v in villages if v["population"] >= min_population]
    return villages


@router.get("/{village_id}")
def get_village(village_id: str):
    village = synthetic.get_village(village_id)
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")

    enriched = _enrich(village)
    history = synthetic.get_history(village_id)
    reasons = explain(village, enriched, history)
    action = recommended_action(enriched["level"])
    rainfall_trend = synthetic.get_rainfall_trend(village_id)

    return {
        **enriched,
        "reasons": reasons,
        "recommended_action": action,
        "history": history,
        "rainfall_trend": rainfall_trend,
    }
