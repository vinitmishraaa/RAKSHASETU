from fastapi import APIRouter
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.optimization.relocation import build_relocation_plan

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("")
def list_alerts():
    alerts = []
    sites = synthetic.get_safe_sites()

    for village in synthetic.get_villages():
        indicators = compute_risk(village)
        cls = classify(indicators["risk_score"])

        if cls["level"] == "CRITICAL":
            alerts.append(
                {
                    "village_id": village["id"],
                    "village_name": village["name"],
                    "level": "CRITICAL",
                    "risk_score": indicators["risk_score"],
                    "message": f"{village['name']} has entered CRITICAL risk category. "
                               f"Immediate relocation assessment recommended.",
                }
            )
        elif cls["level"] == "HIGH":
            alerts.append(
                {
                    "village_id": village["id"],
                    "village_name": village["name"],
                    "level": "HIGH",
                    "risk_score": indicators["risk_score"],
                    "message": f"{village['name']} is at HIGH risk. Priority monitoring advised.",
                }
            )

        plan = build_relocation_plan(village, sites)
        if not plan["fully_covered"] and cls["level"] in ("CRITICAL", "HIGH"):
            alerts.append(
                {
                    "village_id": village["id"],
                    "village_name": village["name"],
                    "level": "WARNING",
                    "risk_score": indicators["risk_score"],
                    "message": f"Capacity warning: available safe sites cannot fully "
                               f"absorb {village['name']}'s population in one location.",
                }
            )

    return alerts


@router.get("/summary")
def alerts_summary():
    alerts = list_alerts()
    summary = {"CRITICAL": 0, "HIGH": 0, "WARNING": 0}
    for a in alerts:
        summary[a["level"]] = summary.get(a["level"], 0) + 1
    return summary
