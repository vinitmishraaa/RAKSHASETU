"""Live public hazard and news feeds for RakshaSetu."""
from __future__ import annotations
import csv
from datetime import datetime, timezone
import io
from urllib.parse import quote_plus
from xml.etree import ElementTree as ET
from fastapi import APIRouter, Query
import httpx
from app.core.config import get_settings
from app.data.geo_catalog import get_district_center, STATE_CENTERS
from app.data.open_data import get_gdacs_events, get_sachet_alerts

router = APIRouter(prefix="/api/live", tags=["live"])


def in_bbox(lat: float, lng: float, bbox: tuple[float, float, float, float]) -> bool:
    south, north, west, east = bbox
    return south <= lat <= north and west <= lng <= east


def fire_severity(frp: float) -> str:
    if frp >= 80:
        return "CRITICAL"
    if frp >= 30:
        return "HIGH"
    if frp >= 8:
        return "MODERATE"
    return "LOW"


def _scope_bbox(region: str | None, district: str | None) -> tuple[float, float, float, float]:
    """Computes bounding box from district or state centroid."""
    if district and region:
        lat, lng = get_district_center(region, district)
        return (lat - 0.5, lat + 0.5, lng - 0.5, lng + 0.5)
    if region:
        c = STATE_CENTERS.get(region)
        if c:
            return (c[0] - 2.5, c[0] + 2.5, c[1] - 2.5, c[1] + 2.5)
    # Default India bounding box
    return (6.5, 37.5, 68.0, 97.5)


async def fetch_firms(client: httpx.AsyncClient, key: str, source: str, bbox: tuple[float, float, float, float]):
    south, north, west, east = bbox
    area = f"{west:.2f},{south:.2f},{east:.2f},{north:.2f}"
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{source}/{area}/1"
    response = await client.get(url)
    response.raise_for_status()
    records = []
    for row in csv.DictReader(io.StringIO(response.text)):
        try:
            lat = float(row.get("latitude", ""))
            lng = float(row.get("longitude", ""))
            frp = float(row.get("frp") or 0)
        except (TypeError, ValueError):
            continue
        records.append({
            "id": f"fire-{source}-{row.get('acq_date')}-{row.get('acq_time')}-{lat}-{lng}",
            "type": "Fire Hotspot",
            "title": "NASA Satellite Thermal Anomaly",
            "lat": lat,
            "lng": lng,
            "frp": frp,
            "confidence": row.get("confidence"),
            "time": f"{row.get('acq_date', '')} {row.get('acq_time', '')}",
            "severity": fire_severity(frp),
            "source": f"NASA FIRMS · {source}",
            "detail": f"Fire Radiative Power {frp:.1f} MW · Satellite {row.get('satellite') or source}",
            "url": "https://firms.modaps.eosdis.nasa.gov/",
        })
    return records


@router.get("/hazards")
async def live_hazards(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
):
    """Returns real-time public hazard observations (USGS earthquakes, NASA FIRMS, NDMA SACHET, GDACS)."""
    st = state or region
    settings = get_settings()
    bbox = _scope_bbox(st, district)
    items = []
    sources = []

    async with httpx.AsyncClient(timeout=8.0, headers={"User-Agent": "RakshaSetu/2.0"}) as client:
        # 1. USGS Real-time Earthquakes
        try:
            r = await client.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson")
            r.raise_for_status()
            quake_count = 0
            for feature in r.json().get("features", []):
                coords = (feature.get("geometry") or {}).get("coordinates") or [None, None, None]
                if coords[0] is None or coords[1] is None or not in_bbox(float(coords[1]), float(coords[0]), bbox):
                    continue
                props = feature.get("properties") or {}
                mag = float(props.get("mag") or 0)
                severity = "CRITICAL" if mag >= 6.0 else ("HIGH" if mag >= 4.5 else ("MODERATE" if mag >= 3.0 else "LOW"))
                items.append({
                    "id": feature.get("id"),
                    "type": "Earthquake",
                    "title": props.get("place") or "Earthquake Event",
                    "lat": float(coords[1]),
                    "lng": float(coords[0]),
                    "magnitude": mag,
                    "time": props.get("time"),
                    "severity": severity,
                    "source": "USGS Realtime",
                    "detail": f"{props.get('place') or 'Seismic event'} · Magnitude {mag:.1f} · Depth {float(coords[2] or 0):.1f} km",
                    "url": props.get("url"),
                })
                quake_count += 1
            sources.append({"name": "USGS Earthquake Feed", "status": "live", "count": quake_count})
        except Exception as exc:
            sources.append({"name": "USGS Earthquake Feed", "status": f"unavailable: {str(exc)[:60]}"})

        # 2. GDACS Global Disasters
        try:
            gdacs = await get_gdacs_events(st)
            events = []
            for event in gdacs.get("events", []):
                if event.get("lat") is None or event.get("lng") is None or in_bbox(float(event["lat"]), float(event["lng"]), bbox):
                    events.append(event)
            items.extend(events)
            sources.append({"name": "GDACS Disaster Feed", "status": "live", "count": len(events)})
        except Exception as exc:
            sources.append({"name": "GDACS Disaster Feed", "status": f"unavailable: {str(exc)[:60]}"})

        # 3. NDMA SACHET CAP Alerts
        try:
            sachet = await get_sachet_alerts(district or st)
            sachet_count = sachet.get("count", 0)
            sources.append({"name": "NDMA SACHET Feed", "status": "live", "count": sachet_count})
            for alert in sachet.get("alerts", []):
                items.append({
                    "id": alert["id"],
                    "type": "Official CAP Alert",
                    "title": alert["title"],
                    "lat": None,
                    "lng": None,
                    "severity": alert["severity"],
                    "time": alert["published"],
                    "source": alert["source"],
                    "detail": f"{alert.get('area', '')} · {alert.get('description', '')}",
                    "url": alert["url"],
                })
        except Exception as exc:
            sources.append({"name": "NDMA SACHET Feed", "status": f"unavailable: {str(exc)[:60]}"})

        # 4. NASA FIRMS Fire Detection (if key provided in .env)
        firms_key = settings.FIRMS_API_KEY
        if firms_key:
            fire_count = 0
            for sensor in ("VIIRS_NOAA20_NRT", "VIIRS_SNPP_NRT"):
                try:
                    records = await fetch_firms(client, firms_key, sensor, bbox)
                    items.extend(records[:400])
                    fire_count += len(records)
                except Exception as exc:
                    sources.append({"name": f"NASA FIRMS ({sensor})", "status": f"unavailable: {str(exc)[:60]}"})
            sources.append({"name": "NASA FIRMS Thermal", "status": "live", "count": fire_count})
        else:
            sources.append({"name": "NASA FIRMS Thermal", "status": "key_optional (add FIRMS_API_KEY in .env)"})

    # Sort items: CRITICAL first, then HIGH
    order = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}
    items.sort(key=lambda x: order.get(x.get("severity", "LOW"), 4))

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
        "sources": sources,
        "region": st or "India",
        "district": district,
        "note": "Live public observations from USGS, NDMA SACHET, and GDACS. Official evacuation orders take precedence.",
    }


@router.get("/news")
async def live_news(
    state: str | None = Query(default=None),
    region: str | None = Query(default=None),
    district: str | None = Query(default=None),
):
    """Fetches real-time publisher news for the selected region/district."""
    target_state = state or region or "India"
    scope = f'"{district}, {target_state}"' if district else f'"{target_state}"'
    q = quote_plus(f'{scope} (disaster OR flood OR cyclone OR earthquake OR rainfall OR landslide)')
    url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    articles = []

    try:
        async with httpx.AsyncClient(timeout=8.0, headers={"User-Agent": "RakshaSetu/2.0"}) as client:
            r = await client.get(url)
            r.raise_for_status()
            root = ET.fromstring(r.text)
            for item in root.findall("./channel/item")[:12]:
                def text(tag: str) -> str:
                    node = item.find(tag)
                    return (node.text or "").strip() if node is not None else ""
                articles.append({
                    "title": text("title"),
                    "url": text("link"),
                    "date": text("pubDate"),
                    "source": text("source") or "News Media",
                    "domain": "Google News RSS",
                })
    except Exception as exc:
        return {
            "region": target_state,
            "district": district,
            "articles": [],
            "source": "Google News RSS",
            "error": str(exc)[:120],
        }

    return {
        "region": target_state,
        "district": district,
        "articles": articles,
        "source": "Google News RSS",
        "note": "Live news headlines from regional news publishers for situational awareness.",
    }
