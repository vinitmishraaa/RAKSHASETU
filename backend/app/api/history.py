from collections import Counter
from fastapi import APIRouter, HTTPException
from app.data import synthetic

router = APIRouter(prefix="/api/history", tags=["history"])
CURATED={
 "West Bengal":[{"year":2024,"hazard":"Cyclone Remal","severity":"High"},{"year":2021,"hazard":"Cyclone Yaas","severity":"High"},{"year":2020,"hazard":"Cyclone Amphan","severity":"High"},{"year":2019,"hazard":"Cyclone Bulbul","severity":"High"}],
 "Bihar":[{"year":2024,"hazard":"Flood","severity":"High"},{"year":2021,"hazard":"Flood","severity":"High"},{"year":2019,"hazard":"Flood","severity":"High"},{"year":2008,"hazard":"Kosi Flood","severity":"High"}],
 "Odisha":[{"year":2021,"hazard":"Cyclone Yaas","severity":"High"},{"year":2019,"hazard":"Cyclone Fani","severity":"High"},{"year":2018,"hazard":"Cyclone Titli","severity":"High"},{"year":2013,"hazard":"Cyclone Phailin","severity":"High"}],
 "Sikkim":[{"year":2023,"hazard":"South Lhonak Glacial Lake Outburst Flood","severity":"Critical"},{"year":2016,"hazard":"Heavy Rainfall / Landslide","severity":"High"},{"year":2011,"hazard":"Sikkim Earthquake","severity":"High"},{"year":1997,"hazard":"Flood / Landslide","severity":"Moderate"}],
}

def _events(village):
    return CURATED.get(village.get("state"), synthetic.get_history(village["id"]))

@router.get("/{village_id}")
def village_history(village_id: str):
    village=synthetic.get_village(village_id)
    if not village: raise HTTPException(status_code=404,detail="Village not found")
    return {"village_id":village_id,"events":_events(village),"rainfall_trend":synthetic.get_rainfall_trend(village_id)}

@router.get("/region/{region}")
def region_history(region: str,district: str|None=None):
    villages=[v for v in synthetic.VILLAGES if v.get("state")==region and (not district or v.get("district")==district)]
    if not villages:return {"region":region,"district":district,"events":[],"hazard_counts":{},"severity_counts":{}}
    base=CURATED.get(region)
    if base:
        timeline=[{**e,"zones_affected":len(villages)} for e in base]
        return {"region":region,"district":district,"events":timeline,"hazard_counts":dict(Counter(e["hazard"] for e in base)),"severity_counts":dict(Counter(e["severity"] for e in base)),"source_note":"Named historical incidents are curated from published disaster records; live publisher context is loaded separately from Google News."}
    events=[]
    for village in villages:
        for event in synthetic.get_history(village["id"]):events.append({**event,"zone":village["name"],"district":village.get("district")})
    grouped={}
    for event in events:
        key=(event.get("year"),event.get("hazard"),event.get("severity"));grouped.setdefault(key,{"year":key[0],"hazard":key[1],"severity":key[2],"zones_affected":0});grouped[key]["zones_affected"]+=1
    timeline=sorted(grouped.values(),key=lambda x:x["year"],reverse=True)
    return {"region":region,"district":district,"events":timeline,"hazard_counts":dict(Counter(e["hazard"] for e in events)),"severity_counts":dict(Counter(e["severity"] for e in events)),"source_note":"Prototype historical layer for non-pilot regions."}
