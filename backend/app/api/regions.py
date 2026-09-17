from __future__ import annotations
import asyncio,time
from fastapi import APIRouter,HTTPException
import httpx

router=APIRouter(prefix="/api/regions",tags=["regions"])
INDIA_REGIONS=[("Andaman and Nicobar Islands","IN-AN"),("Andhra Pradesh","IN-AP"),("Arunachal Pradesh","IN-AR"),("Assam","IN-AS"),("Bihar","IN-BR"),("Chandigarh","IN-CH"),("Chhattisgarh","IN-CT"),("Dadra and Nagar Haveli and Daman and Diu","IN-DH"),("Delhi","IN-DL"),("Goa","IN-GA"),("Gujarat","IN-GJ"),("Haryana","IN-HR"),("Himachal Pradesh","IN-HP"),("Jammu and Kashmir","IN-JK"),("Jharkhand","IN-JH"),("Karnataka","IN-KA"),("Kerala","IN-KL"),("Ladakh","IN-LA"),("Lakshadweep","IN-LD"),("Madhya Pradesh","IN-MP"),("Maharashtra","IN-MH"),("Manipur","IN-MN"),("Meghalaya","IN-ML"),("Mizoram","IN-MZ"),("Nagaland","IN-NL"),("Odisha","IN-OR"),("Puducherry","IN-PY"),("Punjab","IN-PB"),("Rajasthan","IN-RJ"),("Sikkim","IN-SK"),("Tamil Nadu","IN-TN"),("Telangana","IN-TG"),("Tripura","IN-TR"),("Uttar Pradesh","IN-UP"),("Uttarakhand","IN-UT"),("West Bengal","IN-WB")]
OFFICIAL_DISTRICTS={"West Bengal":["Alipurduar","Bankura","Birbhum","Cooch Behar","Dakshin Dinajpur","Darjeeling","Hooghly","Howrah","Jalpaiguri","Jhargram","Kalimpong","Kolkata","Malda","Murshidabad","Nadia","North 24 Parganas","Paschim Bardhaman","Paschim Medinipur","Purba Bardhaman","Purba Medinipur","Purulia","South 24 Parganas","Uttar Dinajpur"]}
OVERPASS_ENDPOINTS=["https://overpass-api.de/api/interpreter","https://overpass.private.coffee/api/interpreter","https://overpass.kumi.systems/api/interpreter"]
CACHE_TTL=600
_district_cache={};_city_cache={};_locks={}

def _clean(v):return(v or "").strip()
def _region(state):
    w=state.casefold().strip()
    for name,code in INDIA_REGIONS:
        if w in (name.casefold(),code.casefold()):return {"name":name,"code":code}
    return None

async def _overpass(query):
    last=None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=70,headers={"User-Agent":"RakshaSetu/1.0 (open-data dashboard)"}) as client:
                r=await client.post(endpoint,data={"data":query})
                if r.status_code in (429,502,503,504):continue
                r.raise_for_status();return r.json()
        except (httpx.HTTPError,ValueError) as exc:last=exc
    raise HTTPException(status_code=503,detail="OpenStreetMap service is temporarily rate-limited. Please retry in a few seconds.") from last

@router.get("/states")
async def states():return [{"name":n,"code":c,"source":"Government administrative directory"} for n,c in INDIA_REGIONS]

async def _districts_for_state(state):
    selected=_region(state)
    if not selected:raise HTTPException(status_code=404,detail="State / Union Territory not found")
    if selected["name"] in OFFICIAL_DISTRICTS:
        return [{"name":name,"state":selected["name"],"source":"Integrated Government Online Directory","source_url":"https://igod.gov.in/sg/WB/E042/organizations"} for name in OFFICIAL_DISTRICTS[selected["name"]]]
    code=selected["code"]
    query=f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level=6];out tags center;'
    data=await _overpass(query);rows=[];seen=set()
    for e in data.get("elements",[]):
        t=e.get("tags",{});name=_clean(t.get("name:en") or t.get("name") or t.get("official_name:en"))
        if not name or name.casefold() in seen:continue
        seen.add(name.casefold());c=e.get("center") or {};rows.append({"name":name,"state":selected["name"],"osm_relation_id":e.get("id"),"lat":c.get("lat"),"lng":c.get("lon"),"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/relation/{e.get('id')}"})
    return sorted(rows,key=lambda x:x["name"].casefold())

@router.get("/districts")
async def districts(state:str):
    selected=_region(state)
    if not selected:raise HTTPException(status_code=404,detail="State / Union Territory not found")
    key=selected["name"].casefold();cached=_district_cache.get(key)
    if cached and time.monotonic()-cached[0]<CACHE_TTL:return cached[1]
    lock=_locks.setdefault(("district",key),asyncio.Lock())
    async with lock:
        cached=_district_cache.get(key)
        if cached and time.monotonic()-cached[0]<CACHE_TTL:return cached[1]
        result=await _districts_for_state(selected["name"]);_district_cache[key]=(time.monotonic(),result);return result

async def _cities_for_district(state,district):
    selected=_region(state)
    if not selected:raise HTTPException(status_code=404,detail="State / Union Territory not found")
    district_name=_clean(district)
    if not district_name:raise HTTPException(status_code=400,detail="District is required")
    code=selected["code"]
    # Fetch only administrative district relations inside the selected state,
    # then match name/name:en/official_name in Python. This handles aliases such
    # as the OSM name "Haora" for the official district "Howrah".
    query=f'[out:json][timeout:60];area["ISO3166-2"="{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level~"^(5|6)$"];out tags;'
    data=await _overpass(query);wanted=district_name.casefold();district_id=None
    for e in data.get("elements",[]):
        t=e.get("tags",{});names={_clean(t.get("name")),_clean(t.get("name:en")),_clean(t.get("official_name")),_clean(t.get("official_name:en"))}
        if wanted in {n.casefold() for n in names if n}:district_id=e.get("id");break
    if not district_id:return []
    area_id=int(district_id)+3600000000
    city_data=await _overpass(f'[out:json][timeout:60];(node(area:{area_id})[place=city];node(area:{area_id})[place=town];);out tags;')
    rows=[];seen=set()
    for e in city_data.get("elements",[]):
        t=e.get("tags",{});name=_clean(t.get("name:en") or t.get("name"))
        if not name or name.casefold() in seen:continue
        seen.add(name.casefold());rows.append({"name":name,"state":selected["name"],"district":district_name,"place_type":t.get("place"),"lat":e.get("lat"),"lng":e.get("lon"),"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/node/{e.get('id')}"})
    return sorted(rows,key=lambda x:x["name"].casefold())

@router.get("/cities")
async def cities(state:str,district:str):
    selected=_region(state)
    if not selected:raise HTTPException(status_code=404,detail="State / Union Territory not found")
    key=(selected["name"].casefold(),district.casefold().strip());cached=_city_cache.get(key)
    if cached and time.monotonic()-cached[0]<CACHE_TTL:return cached[1]
    lock=_locks.setdefault(("city",key),asyncio.Lock())
    async with lock:
        cached=_city_cache.get(key)
        if not cached or time.monotonic()-cached[0]>=CACHE_TTL:
            result=await _cities_for_district(selected["name"],district);_city_cache[key]=(time.monotonic(),result);return result
        return cached[1]
