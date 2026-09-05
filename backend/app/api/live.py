"""Live public hazard/news adapters. These feeds are observational and separate from prototype GIS data."""
from __future__ import annotations
from datetime import datetime, timezone
import httpx
from fastapi import APIRouter, Query
from app.core.config import get_settings

router = APIRouter(prefix="/api/live", tags=["live"])

@router.get("/hazards")
async def live_hazards(region: str | None = Query(default=None)):
    items=[]; sources=[]
    settings=get_settings()
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
                fr=await client.get(url); fr.raise_for_status()
                lines=fr.text.splitlines(); headers=lines[0].split(",") if lines else []
                for line in lines[1:201]:
                    vals=line.split(",")
                    row=dict(zip(headers,vals))
                    try: lat=float(row.get("latitude","")); lng=float(row.get("longitude",""))
                    except ValueError: continue
                    items.append({"id":f"fire-{row.get('acq_date')}-{row.get('acq_time')}-{lat}-{lng}","type":"Fire Hotspot","title":"NASA FIRMS near-real-time hotspot","lat":lat,"lng":lng,"confidence":row.get("confidence"),"time":row.get("acq_date"),"severity":"HIGH","source":"NASA FIRMS"})
                sources.append({"name":"NASA FIRMS","status":"live"})
            else: sources.append({"name":"NASA FIRMS","status":"key_required"})
    except Exception as exc:
        sources.append({"name":"USGS","status":"unavailable","error":str(exc)[:160]})
    return {"updated_at":datetime.now(timezone.utc).isoformat(),"items":items,"sources":sources,"note":"Live public feeds; not a substitute for official emergency orders."}

@router.get("/news")
async def live_news(region: str = Query(..., min_length=2)):
    query=f'"{region}" (flood OR cyclone OR earthquake OR rainfall OR landslide OR disaster)'
    url="https://api.gdeltproject.org/api/v2/doc/doc"
    params={"query":query,"mode":"artlist","maxrecords":12,"format":"json","sort":"datedesc"}
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r=await client.get(url,params=params); r.raise_for_status(); data=r.json()
        articles=[{"title":x.get("title"),"url":x.get("url"),"domain":x.get("domain"),"date":x.get("seendate")} for x in data.get("articles",[])]
        return {"region":region,"articles":articles,"source":"GDELT","note":"News discovery feed; verify articles against the publisher and official agencies before operational use."}
    except Exception as exc:
        return {"region":region,"articles":[],"source":"GDELT","error":str(exc)[:160]}
