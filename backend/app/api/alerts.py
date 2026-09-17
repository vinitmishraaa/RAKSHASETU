from fastapi import APIRouter, Query
from app.data.open_data import get_gdacs_events, get_sachet_alerts

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(region: str | None = Query(default=None)):
    """Return official/open live alert records only; no synthetic alert generation."""
    alerts = []
    sources = []
    try:
        sachet = await get_sachet_alerts(region)
        alerts.extend(sachet.get("alerts", []))
        sources.append({"name": "SACHET · NDMA", "status": "live", "count": sachet.get("count", 0)})
    except Exception as exc:
        sources.append({"name": "SACHET · NDMA", "status": f"unavailable: {str(exc)[:120]}"})
    try:
        gdacs = await get_gdacs_events(region)
        alerts.extend(gdacs.get("events", []))
        sources.append({"name": "GDACS", "status": "live", "count": gdacs.get("count", 0)})
    except Exception as exc:
        sources.append({"name": "GDACS", "status": f"unavailable: {str(exc)[:120]}"})
    return {
        "region": region or "India",
        "updated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "alerts": alerts,
        "count": len(alerts),
        "sources": sources,
        "note": "Official/open live feeds. Alert severity and wording are sourced from providers; RakshaSetu does not invent evacuation orders.",
    }


@router.get("/summary")
async def alerts_summary(region: str | None = Query(default=None)):
    data = await list_alerts(region)
    summary = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    for alert in data.get("alerts", []):
        level = alert.get("severity", "LOW")
        summary[level] = summary.get(level, 0) + 1
    return {"region": data.get("region"), "summary": summary, "count": data.get("count", 0), "sources": data.get("sources", [])}
