from fastapi import APIRouter
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.optimization.relocation import build_relocation_plan

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


def make_alert(village, level, score, message, action, source="RakshaSetu risk engine"):
    return {
        "village_id": village["id"],
        "village_name": village["name"],
        "district": village.get("district"),
        "state": village.get("state"),
        "lat": village.get("lat"),
        "lng": village.get("lng"),
        "population": village.get("population"),
        "level": level,
        "risk_score": score,
        "message": message,
        "action": action,
        "source": source,
    }


@router.get("")
def list_alerts():
    alerts = []
    sites = synthetic.get_safe_sites()
    for village in synthetic.get_villages():
        indicators = compute_risk(village)
        cls = classify(indicators["risk_score"])
        score = indicators["risk_score"]
        location = f"{village['name']}, {village.get('district', '')}, {village.get('state', '')}"

        if cls["level"] == "CRITICAL":
            alerts.append(make_alert(village, "CRITICAL", score, f"{location} has entered CRITICAL risk category. Immediate relocation assessment recommended.", "Assess relocation now"))
        elif cls["level"] == "HIGH":
            alerts.append(make_alert(village, "HIGH", score, f"{location} is at HIGH risk. Priority monitoring and readiness advised.", "Increase field monitoring"))

        plan = build_relocation_plan(village, sites)
        if not plan["fully_covered"] and cls["level"] in ("CRITICAL", "HIGH"):
            alerts.append(make_alert(village, "WARNING", score, f"{location}: available safe-site capacity cannot fully absorb the population in one location.", "Split allocation across safe sites", "Relocation capacity engine"))

    alerts.sort(key=lambda a: (a["level"] != "CRITICAL", a["level"] != "HIGH", -a["risk_score"]))
    return alerts


@router.get("/summary")
def alerts_summary():
    alerts = list_alerts()
    summary = {"CRITICAL": 0, "HIGH": 0, "WARNING": 0}
    for a in alerts:
        summary[a["level"]] = summary.get(a["level"], 0) + 1
    return summary
