from datetime import datetime, timezone
from fastapi import APIRouter, Query
from app.data.open_data import get_gdacs_events, get_sachet_alerts

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(region: str | None = Query(default=None)):
    """Return official/open live alert records only; no synthetic alert generation."""
    alerts = []
    try:
        sachet = await get_sachet_alerts(region)
        alerts.extend(sachet.get("alerts", []))
    except Exception:
        pass
    try:
        gdacs = await get_gdacs_events(region)
        alerts.extend(gdacs.get("events", []))
    except Exception:
        pass
    return alerts


@router.get("/summary")
async def alerts_summary(region: str | None = Query(default=None)):
    alerts = await list_alerts(region)
    summary = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    for alert in alerts:
        level = alert.get("severity", "LOW")
        summary[level] = summary.get(level, 0) + 1
    return summary
