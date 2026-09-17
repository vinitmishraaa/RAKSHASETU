"""Live, open geospatial data adapters used by RakshaSetu."""
from __future__ import annotations
from datetime import datetime, timezone
from math import cos, exp, radians, sqrt
import httpx

REGION_CODES = {"Andaman and Nicobar Islands":"AN","Andhra Pradesh":"AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chandigarh":"CH","Chhattisgarh":"CT","Dadra and Nagar Haveli and Daman and Diu":"DH","Delhi":"DL","Goa":"GA","Gujarat":"GJ","Haryana":"HR","Himachal Pradesh":"HP","Jammu and Kashmir":"JK","Jharkhand":"JH","Karnataka":"KA","Kerala":"KL","Ladakh":"LA","Lakshadweep":"LD","Madhya Pradesh":"MP","Maharashtra":"MH","Manipur":"MN","Meghalaya":"ML","Mizoram":"MZ","Nagaland":"NL","Odisha":"OR","Puducherry":"PY","Punjab":"PB","Rajasthan":"RJ","Sikkim":"SK","Tamil Nadu":"TN","Telangana":"TG","Tripura":"TR","Uttar Pradesh":"UP","Uttarakhand":"UT","West Bengal":"WB"}
REGION_BBOXES = {"India":(6.0,37.2,68.0,97.5),"West Bengal":(21.4,27.3,85.8,89.9),"Bihar":(24.0,27.6,83.2,88.4),"Sikkim":(27.0,28.2,88.0,88.9),"Odisha":(17.7,22.8,81.3,87.6)}
OVERPASS_ENDPOINTS = ["https://overpass-api.de/api/interpreter","https://overpass.private.coffee/api/interpreter","https://overpass.kumi.systems/api/interpreter"]
USGS_URL="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
OPEN_METEO_URL="https://api.open-meteo.com/v1/forecast"

def bbox_for(region): return REGION_BBOXES.get(region or "India",REGION_BBOXES["India"])
def _clean(value): return (value or "").strip()

async def _overpass(query):
    last_error = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            async with httpx.AsyncClient(timeout=70,headers={"User-Agent":"RakshaSetu/1.0 (open-data dashboard)"}) as client:
                response=await client.post(endpoint,data={"data":query})
                if response.status_code in (429,502,503,504): continue
                response.raise_for_status(); return response.json()
        except httpx.HTTPError as exc: last_error = exc
    raise RuntimeError("OpenStreetMap Overpass services are temporarily rate-limited or unavailable") from last_error

async def _district_relation(state: str,district: str):
    code=REGION_CODES.get(state)
    if not code: return None
    query=f'[out:json][timeout:60];area["ISO3166-2"="IN-{code}"][boundary=administrative]->.state;relation(area.state)[boundary=administrative][admin_level~"^(5|6)$"];out tags center bb;'
    data=await _overpass(query); wanted=district.casefold().strip()
    for element in data.get("elements",[]):
        tags=element.get("tags",{}); names=[_clean(tags.get("name:en")),_clean(tags.get("name")),_clean(tags.get("official_name:en"))]
        if wanted in {x.casefold() for x in names if x}: return element
    return None

def _district_bbox(relation):
    b=relation.get("bounds") or {}
    if all(k in b for k in ("minlat","maxlat","minlon","maxlon")): return (float(b["minlat"]),float(b["maxlat"]),float(b["minlon"]),float(b["maxlon"]))
    c=relation.get("center") or {}
    if c.get("lat") is not None and c.get("lon") is not None:
        return (float(c["lat"])-0.25,float(c["lat"])+0.25,float(c["lon"])-0.25,float(c["lon"])+0.25)
    return None

def _area_query(kind,region):
    targets=[region] if region in REGION_CODES else list(REGION_CODES); blocks=[]; selectors=[]
    for name in targets:
        code=REGION_CODES[name]; blocks.append(f'area["ISO3166-2"="IN-{code}"][boundary=administrative][admin_level=4]->.{code};')
        if kind=="node": selectors.append(f'nwr(area.{code})[place~"^(village|town|city)$"];')
        else: selectors += [f'node(area.{code})[amenity=shelter];',f'way(area.{code})[amenity=shelter];',f'relation(area.{code})[amenity=shelter];',f'node(area.{code})[emergency=shelter];',f'way(area.{code})[emergency=shelter];',f'relation(area.{code})[emergency=shelter];']
    return "[out:json][timeout:60];("+"".join(blocks)+"".join(selectors)+");out center tags;"

async def get_live_settlements(region=None,district=None):
    if district and region in REGION_CODES:
        relation=await _district_relation(region,district)
        if not relation: return []
        area_id=int(relation["id"])+3600000000; data=await _overpass(f'[out:json][timeout:60];nwr(area:{area_id})[place~"^(village|town|city)$"];out center tags;')
    else: data=await _overpass(_area_query("node",region))
    items=[]
    for element in data.get("elements",[]):
        tags=element.get("tags",{}); center=element.get("center") or {}; lat=element.get("lat",center.get("lat")); lon=element.get("lon",center.get("lon"))
        if lat is None or lon is None: continue
        try: population=int(float(str(tags["population"]).replace(",",""))) if tags.get("population") else None
        except (TypeError,ValueError): population=None
        items.append({"id":f"osm-{element['type']}-{element['id']}","name":tags.get("name:en") or tags.get("name") or "Unnamed mapped settlement","district":district or tags.get("addr:district"),"state":region if region in REGION_CODES else tags.get("addr:state"),"region":region or "India","lat":float(lat),"lng":float(lon),"population":population,"population_source":"OpenStreetMap population tag" if population is not None else None,"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/{element['type']}/{element['id']}"})
    return items

async def get_live_shelters(region=None,district=None):
    if district and region in REGION_CODES:
        relation=await _district_relation(region,district)
        if not relation: return []
        area_id=int(relation["id"])+3600000000; data=await _overpass(f'[out:json][timeout:60];(node(area:{area_id})[amenity=shelter];way(area:{area_id})[amenity=shelter];relation(area:{area_id})[amenity=shelter];node(area:{area_id})[emergency=shelter];way(area:{area_id})[emergency=shelter];relation(area:{area_id})[emergency=shelter];);out center tags;')
    else: data=await _overpass(_area_query("shelter",region))
    items=[]
    for element in data.get("elements",[]):
        tags=element.get("tags",{}); center=element.get("center") or {}; lat=element.get("lat",center.get("lat")); lon=element.get("lon",center.get("lon"))
        if lat is None or lon is None: continue
        items.append({"id":f"osm-shelter-{element['type']}-{element['id']}","name":tags.get("name:en") or tags.get("name") or "Mapped emergency shelter","region":region or "India","district":district,"lat":float(lat),"lng":float(lon),"capacity":None,"current_occupancy":None,"available_capacity":None,"hazard_risk":None,"infrastructure_score":None,"facilities":[v for v in [tags.get("amenity"),tags.get("emergency"),tags.get("access")] if v],"verified":False,"source":"OpenStreetMap","source_url":f"https://www.openstreetmap.org/{element['type']}/{element['id']}","note":"Mapped location only. Capacity, occupancy and operational status are not inferred."})
    return items

async def _earthquakes():
    async with httpx.AsyncClient(timeout=20,headers={"User-Agent":"RakshaSetu/1.0"}) as client:
        response=await client.get(USGS_URL); response.raise_for_status(); features=response.json().get("features",[])
    return [{"lat":float((f.get("geometry") or {}).get("coordinates")[1]),"lng":float((f.get("geometry") or {}).get("coordinates")[0]),"magnitude":float((f.get("properties") or {}).get("mag") or 0),"time":(f.get("properties") or {}).get("time"),"place":(f.get("properties") or {}).get("place") or "Earthquake","id":f.get("id")} for f in features if len((f.get("geometry") or {}).get("coordinates") or [])>=2]

def _distance_km(lat1,lon1,lat2,lon2):
    x=radians(lon2-lon1)*cos(radians((lat1+lat2)/2)); y=radians(lat2-lat1); return 6371.0*sqrt(x*x+y*y)
def _risk_from_observations(precip_mm,wind_kmh,earthquake_distance_km,earthquake_magnitude=None):
    rain=min(100.0,max(0.0,(precip_mm or 0.0)*8.0))
    wind=min(100.0,max(0.0,((wind_kmh or 0.0)-25.0)*2.0))
    if earthquake_distance_km is None or earthquake_magnitude is None: quake=0.0
    else: quake=min(100.0,max(0.0,earthquake_magnitude*12.0*exp(-earthquake_distance_km/300.0)))
    return round(max(rain,wind,quake),1),{"precipitation":round(rain,1),"wind":round(wind,1),"earthquake":round(quake,1)}
def _level(score): return "CRITICAL" if score>=75 else "HIGH" if score>=50 else "MODERATE" if score>=30 else "LOW"

async def enrich_settlements_with_weather(settlements):
    if not settlements:return settlements
    earthquakes=await _earthquakes()
    async with httpx.AsyncClient(timeout=30,headers={"User-Agent":"RakshaSetu/1.0"}) as client:
        for start in range(0,len(settlements),80):
            batch=settlements[start:start+80]
            try:
                response=await client.get(OPEN_METEO_URL,params={"latitude":",".join(str(x["lat"]) for x in batch),"longitude":",".join(str(x["lng"]) for x in batch),"current":"temperature_2m,precipitation,wind_speed_10m","timezone":"UTC"}); response.raise_for_status(); rows=response.json().get("current",[]); rows=[rows] if isinstance(rows,dict) else rows
            except Exception: rows=[]
            for i,item in enumerate(batch):
                weather=rows[i] if i<len(rows) else {}; nearest=min(((_distance_km(item["lat"],item["lng"],q["lat"],q["lng"]),q) for q in earthquakes),default=(None,None),key=lambda x:x[0] if x[0] is not None else 1e12); distance,quake=nearest; score,components=_risk_from_observations(weather.get("precipitation"),weather.get("wind_speed_10m"),distance,quake.get("magnitude") if quake else None)
                item.update({"weather":{"temperature_c":weather.get("temperature_2m"),"precipitation_mm":weather.get("precipitation"),"wind_speed_kmh":weather.get("wind_speed_10m")},"nearest_earthquake_km":round(distance,1) if distance is not None else None,"nearest_earthquake":quake,"risk_score":score,"risk_components":components,"level":_level(score),"risk_model":"Live indicator from Open-Meteo current precipitation/wind plus USGS earthquake magnitude and distance; not an official hazard rating.","observed_at":datetime.now(timezone.utc).isoformat()})
    return settlements
