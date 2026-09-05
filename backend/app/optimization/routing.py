"""Road-network routing for relocation, with explicit exact-point navigation links."""
from __future__ import annotations
import httpx
from .site_scoring import haversine_km

def _google_maps_url(village:dict,site:dict,mode:str="driving")->str:
    origin=f"{village['name']}, {village.get('district','')}, {village.get('state','')}, India"
    destination=f"{site['name']}, India"
    return ("https://www.google.com/maps/dir/?api=1"
            f"&origin={village['lat']},{village['lng']}"
            f"&destination={site['lat']},{site['lng']}"
            f"&travelmode={mode}")

async def route_between(village:dict,site:dict)->dict:
    straight_km=haversine_km(village["lat"],village["lng"],site["lat"],site["lng"])
    path=[[village["lat"],village["lng"]],[site["lat"],site["lng"]]]; road_distance=straight_km; road_minutes=None; router="unavailable"; route_available=False
    try:
        coords=f"{village['lng']},{village['lat']};{site['lng']},{site['lat']}"
        async with httpx.AsyncClient(timeout=12,headers={"User-Agent":"RakshaSetu-Demo/1.0"}) as client:
            r=await client.get(f"https://router.project-osrm.org/route/v1/driving/{coords}",params={"overview":"full","geometries":"geojson"}); r.raise_for_status()
            routes=r.json().get("routes") or []
            if routes:
                route=routes[0]; geom=route.get("geometry",{}).get("coordinates",[])
                if geom:
                    path=[[float(x[1]),float(x[0])] for x in geom]; route_available=True; router="OSRM road network"
                road_distance=float(route.get("distance",0))/1000 or straight_km; road_minutes=round(float(route.get("duration",0))/60)
    except Exception:
        pass
    return {"from":{"lat":village["lat"],"lng":village["lng"],"name":village["name"]},"to":{"lat":site["lat"],"lng":site["lng"],"name":site["name"]},"distance_km":round(road_distance,1),"road_distance_km":round(road_distance,1),"road_eta_minutes":road_minutes,"air_distance_km":round(straight_km,1),"path":path,"router":router,"route_available":route_available,"google_maps_driving_url":_google_maps_url(village,site,"driving"),"google_maps_transit_url":_google_maps_url(village,site,"transit"),"note":("Road-network route generated successfully." if route_available else "A road-network route could not be confirmed. The map keeps the exact endpoints only; use the Google Maps link for live navigation if road coverage is available.")}
