"""Open public data adapters used by RakshaSetu."""
from __future__ import annotations
from datetime import datetime, timezone
import csv
import io
from typing import Any
import httpx

ZENODO_RECORD = "https://zenodo.org/api/records/16994648"
RELIEFWEB_URL = "https://api.reliefweb.int/v1/reports"


def _client():
    return httpx.AsyncClient(timeout=45, headers={"User-Agent": "RakshaSetu/1.0 (open-data dashboard)"})


async def get_ifi_flood_history(region: str | None = None, district: str | None = None) -> dict[str, Any]:
    """Load the public IFI-Impacts national flood inventory from Zenodo."""
    async with _client() as client:
        record_response = await client.get(ZENODO_RECORD)
        record_response.raise_for_status()
        record = record_response.json()
        files = record.get("files", [])
        target = next((f for f in files if f.get("key") == "India_Flood_Inventory_v3.csv"), None)
        if not target:
            return {"source": "IFI-Impacts", "source_url": ZENODO_RECORD, "events": [], "count": 0, "error": "Dataset file not found in Zenodo record"}
        response = await client.get(target["links"]["self"])
        response.raise_for_status()

    # The published CSV contains quoted fields with embedded newlines.  csv.reader
    # must receive a text stream opened with newline="" so Python does not corrupt
    # the CSV record boundaries on Windows/Python 3.14.
    text = response.content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = list(reader)

    region_l = (region or "").strip().casefold()
    district_l = (district or "").strip().casefold()

    def match(row: dict[str, Any]) -> bool:
        text = " ".join(str(v or "") for v in row.values()).casefold()
        if region_l and region_l not in text:
            return False
        if district_l and district_l not in text:
            return False
        return True

    events = [r for r in rows if match(r)]
    return {
        "source": "IFI-Impacts · IIT Delhi / Zenodo",
        "source_url": "https://zenodo.org/records/16994648",
        "dataset_period": "1967–2023",
        "events": events[:5000],
        "count": len(events),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


async def get_reliefweb_reports(region: str | None = None, appname: str = "rakshasetu") -> dict[str, Any]:
    """Fetch current humanitarian reports. ReliefWeb requires an approved appname."""
    query = region or "India disaster"
    params = {"appname": appname, "limit": 25, "query[value]": query, "sort[]": "date:desc"}
    async with _client() as client:
        response = await client.get(RELIEFWEB_URL, params=params)
        if response.status_code >= 400:
            return {"source": "ReliefWeb API", "source_url": "https://apidoc.reliefweb.int/", "reports": [], "error": response.text[:300], "count": 0}
        payload = response.json()
    reports = []
    for row in payload.get("data", []):
        fields = row.get("fields") or {}
        date = fields.get("date")
        reports.append({"id": row.get("id"), "title": fields.get("title"), "date": date.get("created") if isinstance(date, dict) else date, "url": fields.get("url"), "source": "ReliefWeb"})
    return {"source": "ReliefWeb API", "source_url": "https://apidoc.reliefweb.int/", "reports": reports, "count": len(reports), "updated_at": datetime.now(timezone.utc).isoformat()}
