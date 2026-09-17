from __future__ import annotations
from fastapi import APIRouter, Query
from app.data.open_data import get_gdacs_events, get_sachet_alerts
from app.data.live import get_live_settlements

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
):
    """Returns combined real-time official alerts (SACHET/GDACS) and high-risk monitored zones."""
    st = state or region
    alerts = []

    # 1. Official NDMA SACHET CAP Alerts
    try:
        sachet = await get_sachet_alerts(district or st)
        for a in sachet.get("alerts", []):
            alerts.append({
                "village_id": a.get("id"),
                "village_name": a.get("title") or "NDMA Official Alert",
                "district": district or a.get("area"),
                "state": st,
                "lat": None,
                "lng": None,
                "population": None,
                "level": "CRITICAL" if a.get("severity") == "CRITICAL" else ("HIGH" if a.get("severity") == "HIGH" else "WARNING"),
                "risk_score": 90 if a.get("severity") == "CRITICAL" else (70 if a.get("severity") == "HIGH" else 45),
                "message": a.get("description") or a.get("title"),
                "action": "Follow NDMA official advisories",
                "source": "SACHET · NDMA",
                "time": a.get("published"),
                "url": a.get("url"),
            })
    except Exception:
        pass

    # 2. GDACS Global Disaster Alert Feed
    try:
        gdacs = await get_gdacs_events(st)
        for g in gdacs.get("events", []):
            alerts.append({
                "village_id": g.get("id"),
                "village_name": g.get("title") or "GDACS Event",
                "district": district,
                "state": st,
                "lat": g.get("lat"),
                "lng": g.get("lng"),
                "population": None,
                "level": "CRITICAL" if g.get("severity") == "CRITICAL" else ("HIGH" if g.get("severity") == "HIGH" else "WARNING"),
                "risk_score": 85 if g.get("severity") == "CRITICAL" else 65,
                "message": f"{g.get('type')} alert level: {g.get('alertlevel')}",
                "action": "Monitor situation updates via GDACS",
                "source": "GDACS",
                "time": g.get("fromdate"),
                "url": g.get("url"),
            })
    except Exception:
        pass

    # 3. High & Critical Monitored Settlements from RakshaSetu Risk Engine
    try:
        villages = await get_live_settlements(state=st, district=district)
        for v in villages:
            if v.get("level") in ("CRITICAL", "HIGH"):
                reasons_str = "; ".join(v.get("reasons", [])[:2])
                alerts.append({
                    "village_id": v["id"],
                    "village_name": v["name"],
                    "district": v.get("district"),
                    "state": v.get("state"),
                    "lat": v["lat"],
                    "lng": v["lng"],
                    "population": v.get("population"),
                    "level": v["level"],
                    "risk_score": v["risk_score"],
                    "message": f"Calculated risk {v['risk_score']}/100. {reasons_str}",
                    "action": v.get("recommended_action") or "Immediate relocation assessment",
                    "source": "RakshaSetu Risk Engine",
                    "time": v.get("observed_at"),
                })
    except Exception:
        pass

    # Sort alerts: CRITICAL first, then HIGH, then WARNING
    severity_order = {"CRITICAL": 0, "HIGH": 1, "WARNING": 2, "MODERATE": 3, "LOW": 4}
    alerts.sort(key=lambda a: severity_order.get(a.get("level", "LOW"), 5))

    return alerts


@router.get("/summary")
async def alerts_summary(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
):
    """Returns count breakdown of active alerts."""
    alerts = await list_alerts(state=state, region=region, district=district)
    summary = {"CRITICAL": 0, "HIGH": 0, "WARNING": 0}
    for a in alerts:
        lvl = a.get("level", "WARNING")
        if lvl in summary:
            summary[lvl] += 1
        else:
            summary["WARNING"] += 1
    return summary
