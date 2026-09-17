"""Road-network routing with a live OSRM path and human-readable route steps."""
from __future__ import annotations
import httpx
from .site_scoring import haversine_km

def _google_maps_url(village:dict,site:dict,mode:str="driving")->str:
    return ("https://www.google.com/maps/dir/?api=1"
            f"&origin={village['lat']},{village['lng']}"
            f"&destination={site['lat']},{site['lng']}"
            f"&travelmode={mode}")

def _step_text(step:dict)->str:
    maneuver=step.get("maneuver") or {}; instruction=maneuver.get("instruction") or ""
    name=step.get("name") or ""
    if instruction: return instruction + (f" via {name}" if name and name not in instruction else "")
    return name or maneuver.get("type") or "Continue on the mapped route"

async def route_between(village:dict,site:dict)->dict:
    straight_km=haversine_km(village["lat"],village["lng"],site["lat"],site["lng"])
    path=[[village["lat"],village["lng"]],[site["lat"],site["lng"]]]; road_distance=straight_km; road_minutes=None; router="unavailable"; route_available=False; steps=[]
    try:
        coords=f"{village['lng']},{village['lat']};{site['lng']},{site['lat']}"
        async with httpx.AsyncClient(timeout=15,headers={"User-Agent":"RakshaSetu/1.0"}) as client:
            r=await client.get(f"https://router.project-osrm.org/route/v1/driving/{coords}",params={"overview":"full","geometries":"geojson","steps":"true"}); r.raise_for_status()
            routes=r.json().get("routes") or []
            if routes:
                route=routes[0]; geom=route.get("geometry",{}).get("coordinates",[])
                if geom: path=[[float(x[1]),float(x[0])] for x in geom]; route_available=True; router="OSRM road network"
                road_distance=float(route.get("distance",0))/1000 or straight_km; road_minutes=round(float(route.get("duration",0))/60)
                raw_steps=(route.get("legs") or [{}])[0].get("steps") or []
                steps=[{"instruction":_step_text(s),"distance_km":round(float(s.get("distance",0))/1000,2),"duration_minutes":round(float(s.get("duration",0))/60,1)} for s in raw_steps]
    except Exception:
        pass
    return {"from":{"lat":village["lat"],"lng":village["lng"],"name":village["name"]},"to":{"lat":site["lat"],"lng":site["lng"],"name":site["name"]},"distance_km":round(road_distance,1),"road_distance_km":round(road_distance,1),"road_eta_minutes":road_minutes,"air_distance_km":round(straight_km,1),"path":path,"router":router,"route_available":route_available,"steps":steps[:25],"google_maps_driving_url":_google_maps_url(village,site,"driving"),"google_maps_transit_url":_google_maps_url(village,site,"transit"),"note":("Road-network route generated from OSRM. Re-check current road closures and official instructions before travel." if route_available else "A road-network route could not be confirmed. Use the live Google Maps link for navigation if available.")}
