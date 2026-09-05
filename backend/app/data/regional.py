"""Deterministic demo coverage used until verified GIS/live feeds are connected.
The generated records are explicitly marked prototype and must not be presented as
real incident observations.
"""
from __future__ import annotations
import hashlib, random
from app.data import districts, synthetic

CHINA_PROVINCES = ["Anhui","Beijing","Chongqing","Fujian","Gansu","Guangdong","Guangxi","Guizhou","Hainan","Hebei","Heilongjiang","Henan","Hubei","Hunan","Inner Mongolia","Jiangsu","Jiangxi","Jilin","Liaoning","Ningxia","Qinghai","Shaanxi","Shandong","Shanghai","Shanxi","Sichuan","Tianjin","Tibet","Xinjiang","Yunnan","Zhejiang"]
CHINA_POINTS={"Anhui":(31.8,117.2),"Beijing":(40.0,116.4),"Chongqing":(29.5,106.5),"Fujian":(26.1,118.0),"Gansu":(38.0,99.0),"Guangdong":(23.4,113.4),"Guangxi":(24.0,108.0),"Guizhou":(26.8,106.8),"Hainan":(19.2,109.7),"Hebei":(39.3,115.4),"Heilongjiang":(47.8,127.8),"Henan":(34.3,113.6),"Hubei":(30.9,112.2),"Hunan":(27.6,111.7),"Inner Mongolia":(44.0,111.7),"Jiangsu":(32.9,119.5),"Jiangxi":(27.6,115.7),"Jilin":(43.7,126.2),"Liaoning":(41.3,122.6),"Ningxia":(37.3,106.2),"Qinghai":(36.0,96.0),"Shaanxi":(35.2,109.0),"Shandong":(36.4,118.0),"Shanghai":(31.2,121.5),"Shanxi":(37.8,112.5),"Sichuan":(30.6,102.0),"Tianjin":(39.1,117.2),"Tibet":(31.0,88.0),"Xinjiang":(41.7,85.0),"Yunnan":(25.0,101.5),"Zhejiang":(29.2,120.2)}
NEPAL_PROVINCES=["Koshi","Madhesh","Bagmati","Gandaki","Lumbini","Karnali","Sudurpashchim"]
NEPAL_POINTS={"Koshi":(27.2,87.0),"Madhesh":(26.7,85.7),"Bagmati":(27.9,85.3),"Gandaki":(28.3,84.3),"Lumbini":(27.9,83.4),"Karnali":(29.2,82.5),"Sudurpashchim":(29.3,80.5)}

def _rng(key:str)->random.Random: return random.Random(int(hashlib.sha256(key.encode()).hexdigest()[:8],16))
def _point(region:str,district:str):
    if region in CHINA_POINTS: lat,lng=CHINA_POINTS[region]; r=_rng(f"point:{region}:{district}"); return round(lat+r.uniform(-.35,.35),5),round(lng+r.uniform(-.45,.45),5)
    if region in NEPAL_POINTS: lat,lng=NEPAL_POINTS[region]; r=_rng(f"point:{region}:{district}"); return round(lat+r.uniform(-.18,.18),5),round(lng+r.uniform(-.25,.25),5)
    south,north,west,east=districts.REGION_BOUNDS[region]; r=_rng(f"point:{region}:{district}"); return round(r.uniform(south,north),5),round(r.uniform(west,east),5)
def _village(region:str,district:str,index:int,province:str|None=None):
    r=_rng(f"village:{region}:{district}"); lat,lng=_point(region,district); flood=r.randint(25,90); landslide=r.randint(10,88); cyclone=r.randint(10,90)
    if region in {"Bihar","Nepal"} or province in {"Madhesh","Koshi"}: flood=min(96,flood+10)
    if region in {"West Bengal","Odisha"}: cyclone=min(96,cyclone+10)
    if region in {"Sikkim","Nepal"} or province in {"Bagmati","Gandaki","Karnali"}: landslide=min(96,landslide+12)
    population=r.randint(1200,7200)
    return {"id":f"RG{index:03d}","name":f"{district} Response Zone","district":district,"state":region,"region":region,"province":province,"country":"China" if region in CHINA_POINTS else ("Nepal" if region in NEPAL_POINTS else "India"),"lat":lat,"lng":lng,"population":population,"households":max(1,round(population/r.uniform(3.7,5.2)),),"children":round(population*r.uniform(.16,.24)),"elderly":round(population*r.uniform(.07,.13)),"other_vulnerable":round(population*r.uniform(.04,.09)),"elevation_m":round(r.uniform(2,180),1),"distance_river_km":round(r.uniform(.2,8),2),"distance_road_km":round(r.uniform(.4,15),2),"embankment_condition":round(r.uniform(.3,.9),2),"rainfall_mm_month":r.randint(120,480),"flood_hazard":flood,"landslide_hazard":landslide,"cyclone_hazard":cyclone}
def _safe_site(region,index,latlng=None):
    r=_rng(f"site:{region}:{index}"); lat,lng=latlng or _point(region,f"safe-site-{index}"); capacity=r.randint(1200,6500); occupancy=r.randint(100,min(1000,capacity//2)); facilities=["Water supply","Emergency power"]
    if r.random()>.35: facilities.append("Medical post")
    if r.random()>.45: facilities.append("Shelter-ready hall")
    return {"id":f"RS{index:03d}","name":f"{region} Emergency Shelter {index}","region":region,"lat":lat,"lng":lng,"capacity":capacity,"current_occupancy":occupancy,"elevation_m":round(r.uniform(5,25),1),"distance_road_km":round(r.uniform(.1,2.5),2),"hazard_risk":r.randint(5,30),"infrastructure_score":r.randint(68,96),"facilities":facilities}

def build_regional_data():
    existing={v["district"] for v in synthetic.VILLAGES}; generated=[]; index=100
    for region in districts.TARGET_REGIONS:
        for district in districts.get_districts(region):
            if district in existing: continue
            generated.append(_village(region,district,index)); index+=1
    for province,(lat,lng) in NEPAL_POINTS.items(): generated.append(_village(province,f"{province} Province",index,province)); index+=1
    for province,(lat,lng) in CHINA_POINTS.items(): generated.append(_village(province,f"{province} Province",index)); index+=1
    sites=[]; site_index=10
    for region in districts.TARGET_REGIONS:
        for _ in range(3): sites.append(_safe_site(region,site_index)); site_index+=1
    for province,(lat,lng) in {**NEPAL_POINTS,**CHINA_POINTS}.items(): sites.append(_safe_site(province,site_index,(lat,lng))); site_index+=1
    for village in generated:
        r=_rng(f"history:{village['id']}"); events=[]
        for year in (2019,2021,2023,2025): events.append({"year":year,"hazard":r.choice(["Flood","Heavy Rainfall","Cyclone","Landslide","Earthquake"]),"severity":r.choice(["Low","Moderate","High"])})
        synthetic.HISTORICAL_EVENTS[village["id"]]=events; base=village["rainfall_mm_month"]; synthetic.RAINFALL_TREND[village["id"]]=[max(80,round(base*r.uniform(.55,1.15))) for _ in range(12)]
    return generated,sites
