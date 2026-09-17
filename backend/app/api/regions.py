from __future__ import annotations
import asyncio,time
from fastapi import APIRouter,HTTPException
import httpx

router=APIRouter(prefix="/api/regions",tags=["regions"])
INDIA_REGIONS=[("Andaman and Nicobar Islands","IN-AN"),("Andhra Pradesh","IN-AP"),("Arunachal Pradesh","IN-AR"),("Assam","IN-AS"),("Bihar","IN-BR"),("Chandigarh","IN-CH"),("Chhattisgarh","IN-CT"),("Dadra and Nagar Haveli and Daman and Diu","IN-DH"),("Delhi","IN-DL"),("Goa","IN-GA"),("Gujarat","IN-GJ"),("Haryana","IN-HR"),("Himachal Pradesh","IN-HP"),("Jammu and Kashmir","IN-JK"),("Jharkhand","IN-JH"),("Karnataka","IN-KA"),("Kerala","IN-KL"),("Ladakh","IN-LA"),("Lakshadweep","IN-LD"),("Madhya Pradesh","IN-MP"),("Maharashtra","IN-MH"),("Manipur","IN-MN"),("Meghalaya","IN-ML"),("Mizoram","IN-MZ"),("Nagaland","IN-NL"),("Odisha","IN-OR"),("Puducherry","IN-PY"),("Punjab","IN-PB"),("Rajasthan","IN-RJ"),("Sikkim","IN-SK"),("Tamil Nadu","IN-TN"),("Telangana","IN-TG"),("Tripura","IN-TR"),("Uttar Pradesh","IN-UP"),("Uttarakhand","IN-UT"),("West Bengal","IN-WB")]
OVERPASS_ENDPOINTS=["https://overpass-api.de/api/interpreter","https://overpass.private.coffee/api/interpreter","https://overpass.kumi.systems/api/interpreter"]
CACHE_TTL=600
_city_cache={};_district_cache={};_city_locks={};_district_locks={}

def _clean(v):return(v or "").strip()
def _region(state):
    wanted=state.casefold().strip()
    for name,code in INDIA_REGIONS:
        if name.casefold()==wanted or code.casefold()==wanted:return {"name":name,"code":code}
    return None
async def _overpass(query):
    last=None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=70,headers={"User-Agent":"RakshaSetu/1.0 (open-data dashboard)"}) as client:
                r=await client.post(endpoint,data={"data":query})
                if r.status_code in(429,502,503,504):continue
                r.raise_for_status();return r.json()
        except(httpx.HTTPError,ValueError)as exc:last=exc
    raise HTTPException(status_code=503,detail="OpenStreetMap Overpass services are temporarily rate-limited or unavailable. Please retry shortly.") from last

@router.get("/states")
async def states():return [{"name":n,"code":c,"source":"Indian administrative list","source_url":"https://www.indiacode.nic.in/"} for n,c in INDIA_REGIONS]

async def _cities_for_state(state):
    selected=_region(state)
    if not selected:raise HTTPException(status_code=404,detail="State / Union Territory not found")
    code=selected["code"];query=f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;(node(area.state)[place=city];node(area.state)[place=town];);out center tags;';data=await _overpass(query);rows=[];seen=set()
    for e in data.get("elements",[]):
        t=e.get("tags",{});name=_clean(t.get("name:en") or t.get("name"));c=e.get("center") or {};lat=e.get("lat",c.get("lat"));lng=e.get("lon",c.get("lon"))
        if not name or name.casefold() in seen or lat is None or lng is None:continue
        seen.add(name.casefold());rows.append({"name":name,"state":selected["name"],"place_type":t.get("place"),"district":_clean(t.get("addr:district")) or None,"lat":lat,"lng":lng,"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/{e.get('type')}/{e.get('id')}"})
    return sorted(rows,key=lambda x:x["name"].casefold())

@router.get("/cities")
async def cities(state:str):
    key=state.casefold().strip();cached=_city_cache.get(key)
    if cached and time.monotonic()-cached[0]<CACHE_TTL:return cached[1]
    lock=_city_locks.setdefault(key,asyncio.Lock())
    async with lock:
        cached=_city_cache.get(key)
        if cached and time.monotonic()-cached[0]<CACHE_TTL:return cached[1]
        result=await _cities_for_state(state);_city_cache[key]=(time.monotonic(),result);return result

async def _districts_for_state(state):
    selected=_region(state)
    if not selected:raise HTTPException(status_code=404,detail="State / Union Territory not found")
    code=selected["code"];query=f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level=6];out tags center;';data=await _overpass(query);rows=[];seen=set()
    for e in data.get("elements",[]):
        t=e.get("tags",{});name=_clean(t.get("name:en") or t.get("name"));
        if not name or name.casefold() in seen:continue
        seen.add(name.casefold());c=e.get("center") or {};rows.append({"name":name,"state":selected["name"],"osm_relation_id":e.get("id"),"lat":c.get("lat"),"lng":c.get("lon"),"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/relation/{e.get('id')}"})
    if not rows:
        query=f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level=5];out tags center;';data=await _overpass(query)
        for e in data.get("elements",[]):
            t=e.get("tags",{});name=_clean(t.get("name:en") or t.get("name"));
            if not name or name.casefold() in seen:continue
            seen.add(name.casefold());c=e.get("center") or {};rows.append({"name":name,"state":selected["name"],"osm_relation_id":e.get("id"),"lat":c.get("lat"),"lng":c.get("lon"),"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/relation/{e.get('id')}"})
    return sorted(rows,key=lambda x:x["name"].casefold())

@router.get("/districts")
async def districts(state:str,city:str|None=None):
    key=state.casefold().strip();cached=_district_cache.get(key)
    if not cached or time.monotonic()-cached[0]>=CACHE_TTL:
        lock=_district_locks.setdefault(key,asyncio.Lock())
        async with lock:
            cached=_district_cache.get(key)
            if not cached or time.monotonic()-cached[0]>=CACHE_TTL:
                result=await _districts_for_state(state);_district_cache[key]=(time.monotonic(),result);cached=_district_cache[key]
    rows=cached[1]
    if city:
        city_rows=_city_cache.get(key);matched=None
        if city_rows:matched=next((c for c in city_rows[1] if c["name"].casefold()==city.casefold().strip() and c.get("district")),None)
        if matched:
            exact=[r for r in rows if r["name"].casefold()==matched["district"].casefold()]
            if exact:return exact
    return rows
