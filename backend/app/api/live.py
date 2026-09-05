"""Live public hazard and news adapters for the four-state India demo."""
from __future__ import annotations
from datetime import datetime, timezone
from urllib.parse import quote_plus
from xml.etree import ElementTree as ET
import csv
import io
import httpx
from fastapi import APIRouter, Query
from app.core.config import get_settings

router = APIRouter(prefix="/api/live", tags=["live"])
REGION_BBOXES={"India":(6.0,37.2,68.0,97.5),"West Bengal":(21.4,27.3,85.8,89.9),"Bihar":(24.0,27.6,83.2,88.4),"Sikkim":(27.0,28.2,88.0,88.9),"Odisha":(17.7,22.8,81.3,87.6)}

def in_bbox(lat:float,lng:float,bbox:tuple[float,float,float,float])->bool:
    south,north,west,east=bbox; return south<=lat<=north and west<=lng<=east

def fire_severity(frp:float)->str:
    if frp>=80:return "CRITICAL"
    if frp>=30:return "HIGH"
    if frp>=8:return "MODERATE"
    return "LOW"

async def fetch_firms(client:httpx.AsyncClient,key:str,source:str,bbox:tuple[float,float,float,float]):
    south,north,west,east=bbox; area=f"{west},{south},{east},{north}"
    url=f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{source}/{area}/1"
    response=await client.get(url); response.raise_for_status(); records=[]
    for row in csv.DictReader(io.StringIO(response.text)):
        try:
            lat=float(row.get("latitude","")); lng=float(row.get("longitude","")); frp=float(row.get("frp") or 0)
        except (TypeError,ValueError): continue
        exact=f"{lat:.5f}°, {lng:.5f}°"
        records.append({"id":f"fire-{source}-{row.get('acq_date')}-{row.get('acq_time')}-{lat}-{lng}","type":"Fire Hotspot","title":f"Active fire hotspot · {exact}","lat":lat,"lng":lng,"frp":frp,"confidence":row.get("confidence"),"time":f"{row.get('acq_date','')} {row.get('acq_time','')}","severity":fire_severity(frp),"source":f"NASA FIRMS · {source}","detail":f"Exact location {exact} · FRP {frp:.1f} MW · confidence {row.get('confidence') or 'n/a'} · satellite {row.get('satellite') or source}","url":"https://firms.modaps.eosdis.nasa.gov/"})
    return records

@router.get("/hazards")
async def live_hazards(region:str|None=Query(default=None)):
    settings=get_settings(); bbox=REGION_BBOXES.get(region or "India",REGION_BBOXES["India"]); items=[]; sources=[]
    async with httpx.AsyncClient(timeout=15,headers={"User-Agent":"RakshaSetu-Demo/1.0"}) as client:
        try:
            r=await client.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"); r.raise_for_status()
            for feature in r.json().get("features",[]):
                props=feature.get("properties") or {}; coords=(feature.get("geometry") or {}).get("coordinates") or [None,None,None]
                if coords[0] is None or coords[1] is None or not in_bbox(float(coords[1]),float(coords[0]),bbox): continue
                mag=float(props.get("mag") or 0); severity="CRITICAL" if mag>=6 else "HIGH" if mag>=4.5 else "MODERATE" if mag>=3 else "LOW"
                items.append({"id":feature.get("id"),"type":"Earthquake","title":props.get("title"),"lat":float(coords[1]),"lng":float(coords[0]),"magnitude":mag,"time":props.get("time"),"severity":severity,"source":"USGS","detail":f"Exact location {float(coords[1]):.5f}°, {float(coords[0]):.5f}° · magnitude {mag:.1f} · depth {float(coords[2] or 0):.1f} km","url":props.get("url")})
            sources.append({"name":"USGS Earthquake Feed","status":"live","count":len([x for x in items if x["type"]=="Earthquake"])})
        except Exception as exc: sources.append({"name":"USGS Earthquake Feed","status":f"unavailable: {str(exc)[:100]}"})
        if settings.FIRMS_API_KEY:
            fire_count=0
            for sensor in ("VIIRS_NOAA20_NRT","VIIRS_NOAA21_NRT"):
                try:
                    records=await fetch_firms(client,settings.FIRMS_API_KEY,sensor,bbox); items.extend(records[:800]); fire_count+=len(records)
                except Exception as exc: sources.append({"name":f"NASA FIRMS · {sensor}","status":f"unavailable: {str(exc)[:100]}"})
            sources.append({"name":"NASA FIRMS","status":"live","count":fire_count})
        else: sources.append({"name":"NASA FIRMS","status":"key_required"})
    items.sort(key=lambda x:(x["severity"]!="CRITICAL",x["severity"]!="HIGH",-(float(x.get("magnitude") or 0)+float(x.get("frp") or 0)/100)))
    return {"updated_at":datetime.now(timezone.utc).isoformat(),"items":items,"sources":sources,"region":region or "India","note":"Live public observations. Satellite fire detections and earthquake feeds are signals, not official evacuation orders; verify official warnings before action."}

@router.get("/news")
async def live_news(region:str=Query(...,min_length=2)):
    q=quote_plus(f'"{region}" (flood OR cyclone OR earthquake OR rainfall OR landslide OR disaster)'); url=f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"; articles=[]
    try:
        async with httpx.AsyncClient(timeout=12,headers={"User-Agent":"RakshaSetu-Demo/1.0"}) as client:
            r=await client.get(url); r.raise_for_status()
        root=ET.fromstring(r.text)
        for item in root.findall("./channel/item")[:12]:
            def text(tag):
                node=item.find(tag); return (node.text or "").strip() if node is not None else ""
            articles.append({"title":text("title"),"url":text("link"),"date":text("pubDate"),"source":text("source"),"domain":"Google News"})
    except Exception as exc: return {"region":region,"articles":[],"source":"Google News RSS","error":str(exc)[:160]}
    return {"region":region,"articles":articles,"source":"Google News RSS","note":"Current publisher articles for context; verify the original publisher and official agencies before action."}
