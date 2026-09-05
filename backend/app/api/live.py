"""Live public hazard and news adapters for the four-state demo scope."""
from __future__ import annotations
from datetime import datetime, timezone
from urllib.parse import quote_plus
from xml.etree import ElementTree as ET
import httpx
from fastapi import APIRouter, Query
from app.core.config import get_settings

router = APIRouter(prefix="/api/live", tags=["live"])

@router.get("/hazards")
async def live_hazards(region: str | None = Query(default=None)):
    items=[]; sources=[]; settings=get_settings()
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r=await client.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson")
            r.raise_for_status()
            for f in r.json().get("features",[]):
                p=f.get("properties") or {}; g=f.get("geometry") or {}; c=(g.get("coordinates") or [None,None,None])
                if c[0] is None or c[1] is None: continue
                items.append({"id":f.get("id"),"type":"Earthquake","title":p.get("title"),"lat":c[1],"lng":c[0],"magnitude":p.get("mag"),"time":p.get("time"),"severity":"CRITICAL" if (p.get("mag") or 0)>=6 else "HIGH" if (p.get("mag") or 0)>=4.5 else "MODERATE","source":"USGS","url":p.get("url")})
            sources.append({"name":"USGS Earthquake Feed","status":"live"})
            if settings.FIRMS_API_KEY:
                url=f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{settings.FIRMS_API_KEY}/VIIRS_SNPP_NRT/world/1"
                fr=await client.get(url); fr.raise_for_status(); lines=fr.text.splitlines(); headers=lines[0].split(",") if lines else []
                for line in lines[1:201]:
                    row=dict(zip(headers,line.split(",")))
                    try: lat=float(row.get("latitude","")); lng=float(row.get("longitude",""))
                    except ValueError: continue
                    items.append({"id":f"fire-{row.get('acq_date')}-{row.get('acq_time')}-{lat}-{lng}","type":"Fire Hotspot","title":"NASA FIRMS near-real-time hotspot","lat":lat,"lng":lng,"confidence":row.get("confidence"),"time":row.get("acq_date"),"severity":"HIGH","source":"NASA FIRMS"})
                sources.append({"name":"NASA FIRMS","status":"live"})
            else: sources.append({"name":"NASA FIRMS","status":"key_required"})
    except Exception as exc:
        sources.append({"name":"USGS","status":"unavailable","error":str(exc)[:160]})
    return {"updated_at":datetime.now(timezone.utc).isoformat(),"items":items,"sources":sources,"note":"Live public observations; verify official warnings before operational action."}

@router.get("/news")
async def live_news(region: str = Query(..., min_length=2)):
    """Google News RSS gives current publisher articles without a paid search API."""
    q=quote_plus(f'"{region}" (flood OR cyclone OR earthquake OR rainfall OR landslide OR disaster)')
    url=f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    articles=[]
    try:
        async with httpx.AsyncClient(timeout=12,headers={"User-Agent":"RakshaSetu-Demo/1.0"}) as client:
            r=await client.get(url); r.raise_for_status()
        root=ET.fromstring(r.text)
        for item in root.findall("./channel/item")[:12]:
            def text(tag):
                node=item.find(tag); return (node.text or "").strip() if node is not None else ""
            articles.append({"title":text("title"),"url":text("link"),"date":text("pubDate"),"source":text("source"),"domain":"Google News"})
    except Exception as exc:
        return {"region":region,"articles":[],"source":"Google News RSS","error":str(exc)[:160]}
    return {"region":region,"articles":articles,"source":"Google News RSS","note":"Current publisher articles for context; verify the original publisher and official agencies before action."}
