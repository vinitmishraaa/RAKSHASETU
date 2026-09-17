"""Open/public disaster-data adapters used by RakshaSetu.

The adapters return source data as-is or clearly labelled normalized fields.
No synthetic population, capacity, occupancy, or hazard quantities are generated.
"""
from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote_plus
from xml.etree import ElementTree as ET

import httpx

SACHET_RSS = "https://sachet.ndma.gov.in/cap_public_website/rss/rss_india.xml"
GDACS_URL = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/MAP"
ZENODO_RECORD = "https://zenodo.org/api/records/16994648"
RELIEFWEB_URL = "https://api.reliefweb.int/v2/reports"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=25, headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"})


def _severity(value: str | None) -> str:
    value = (value or "").lower()
    if value in {"red", "critical"}:
        return "CRITICAL"
    if value in {"orange", "high"}:
        return "HIGH"
    if value in {"yellow", "moderate"}:
        return "MODERATE"
    return "LOW"


async def get_sachet_alerts(region: str | None = None) -> dict[str, Any]:
    async with _client() as client:
        response = await client.get(SACHET_RSS)
        response.raise_for_status()
    root = ET.fromstring(response.text)
    items: list[dict[str, Any]] = []
    region_l = (region or "").lower()
    for item in root.findall("./channel/item"):
        def text(name: str) -> str:
            node = item.find(name)
            return (node.text or "").strip() if node is not None else ""
        title, description = text("title"), text("description")
        area = text("areaDesc") or description
        if region_l and region_l not in f"{title} {description} {area}".lower():
            continue
        items.append({"id": text("guid") or text("link") or title,"type": "Official CAP Alert","title": title or "NDMA alert","description": description,"area": area,"published": text("pubDate"),"url": text("link") or "https://sachet.ndma.gov.in/CapFeed","severity": _severity(text("severity") or description),"source": "SACHET · NDMA / Government of India"})
    return {"source": "SACHET · NDMA", "source_url": "https://sachet.ndma.gov.in/CapFeed", "updated_at": datetime.now(timezone.utc).isoformat(), "alerts": items[:100], "count": len(items)}


async def get_gdacs_events(region: str | None = None) -> dict[str, Any]:
    async with _client() as client:
        response = await client.get(GDACS_URL, params={"eventtypes": "EQ,TC,FL,WF,DR,VO"})
        response.raise_for_status()
        payload = response.json()
    features = payload.get("features", []) if isinstance(payload, dict) else []
    region_l = (region or "").lower()
    events = []
    for feature in features:
        props = feature.get("properties") or {}; geometry = feature.get("geometry") or {}; affected = props.get("affectedcountries") or []
        haystack = f"{props.get('country','')} {props.get('name','')} {' '.join(str(x) for x in affected)}".lower()
        if region_l and region_l not in haystack and "india" not in haystack:
            continue
        coords = geometry.get("coordinates") or [None, None]
        lat, lng = (coords[1], coords[0]) if geometry.get("type") == "Point" and len(coords) >= 2 else (None, None)
        events.append({"id": f"gdacs-{props.get('eventid')}-{props.get('episodeid','')}","type": props.get("eventtype") or "Disaster","title": props.get("name") or "GDACS event","lat": lat,"lng": lng,"alertlevel": props.get("alertlevel"),"severity": _severity(props.get("alertlevel")),"alertscore": props.get("alertscore"),"fromdate": props.get("fromdate"),"todate": props.get("todate"),"country": props.get("country"),"source": "GDACS","url": ((props.get("url") or {}).get("report") if isinstance(props.get("url"), dict) else None) or "https://www.gdacs.org/"})
    return {"source": "GDACS", "source_url": "https://www.gdacs.org/", "updated_at": datetime.now(timezone.utc).isoformat(), "events": events[:100], "count": len(events)}


async def get_ifi_flood_history(region: str | None = None, district: str | None = None) -> dict[str, Any]:
    async with _client() as client:
        record_response = await client.get(ZENODO_RECORD)
        record_response.raise_for_status()
        record = record_response.json()
        target = next((f for f in record.get("files", []) if f.get("key") == "India_Flood_Inventory_v3.csv"), None)
        if not target:
            return {"source": "IFI-Impacts", "events": [], "count": 0, "error": "Dataset file not found in Zenodo record"}
        response = await client.get(target["links"]["self"])
        response.raise_for_status()
    # Preserve quoted multiline CSV fields. newline="" is required by Python's csv reader.
    text = response.content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = list(reader)
    region_l, district_l = (region or "").strip().casefold(), (district or "").strip().casefold()
    def match(row: dict[str, Any]) -> bool:
        text = " ".join(str(v or "") for v in row.values()).casefold()
        return (not region_l or region_l in text) and (not district_l or district_l in text)
    events = [r for r in rows if match(r)]
    return {"source": "IFI-Impacts · IIT Delhi / Zenodo", "source_url": "https://zenodo.org/records/16994648", "dataset_period": "1967–2023", "events": events[:5000], "count": len(events), "updated_at": datetime.now(timezone.utc).isoformat()}


async def get_reliefweb_reports(region: str | None = None, appname: str = "rakshasetu") -> dict[str, Any]:
    query = region or "India disaster"
    params = {"appname": appname, "limit": 25, "query[value]": query, "sort[]": "date:desc"}
    async with _client() as client:
        response = await client.get(RELIEFWEB_URL, params=params)
        if response.status_code >= 400:
            return {"source": "ReliefWeb API", "source_url": "https://apidoc.reliefweb.int/", "reports": [], "error": response.text[:300], "count": 0}
        payload = response.json()
    reports = []
    for row in payload.get("data", []):
        fields = row.get("fields") or {}; date = fields.get("date")
        reports.append({"id": row.get("id"), "title": fields.get("title"), "date": date.get("created") if isinstance(date, dict) else date, "url": fields.get("url"), "source": "ReliefWeb"})
    return {"source": "ReliefWeb API", "source_url": "https://apidoc.reliefweb.int/", "reports": reports, "count": len(reports), "updated_at": datetime.now(timezone.utc).isoformat()}


async def route_osrm(start_lat: float, start_lng: float, end_lat: float, end_lng: float) -> dict[str, Any]:
    url = f"{OSRM_URL}/{start_lng},{start_lat};{end_lng},{end_lat}"
    async with _client() as client:
        response = await client.get(url, params={"overview": "full", "geometries": "geojson", "steps": "true"})
        response.raise_for_status()
        payload = response.json()
    route = (payload.get("routes") or [None])[0]
    if not route:
        return {"source": "OSRM", "status": "no-route", "routes": []}
    return {"source": "OSRM", "source_url": "https://project-osrm.org/", "status": payload.get("code"), "distance_m": route.get("distance"), "duration_s": route.get("duration"), "geometry": route.get("geometry"), "steps": route.get("legs", [{}])[0].get("steps", [])}
