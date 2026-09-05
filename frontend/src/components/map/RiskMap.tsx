import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup, Polyline, useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./risk-map.css";
import type { Village, SafeSite } from "../../types";

interface RiskMapProps { villages: Village[]; safeSites?: SafeSite[]; selectedId?: string | null; onSelectVillage?: (v: Village) => void; region?: string; district?: string; route?: [number, number][]; center?: [number, number]; zoom?: number; }

type View = { center: [number, number]; zoom: number };
const REGION_VIEWS: Record<string, View> = {
  India:{center:[22.6,79.0],zoom:5}, Nepal:{center:[28.3,84.2],zoom:7}, China:{center:[35.8,103.8],zoom:4},
  "West Bengal":{center:[23.9,87.8],zoom:7}, Bihar:{center:[25.9,85.7],zoom:7}, Odisha:{center:[20.4,84.4],zoom:7}, Jharkhand:{center:[23.6,85.3],zoom:7}, Sikkim:{center:[27.6,88.5],zoom:9},
  Koshi:{center:[27.2,87.0],zoom:8}, Madhesh:{center:[26.7,85.7],zoom:8}, Bagmati:{center:[27.9,85.3],zoom:8}, Gandaki:{center:[28.3,84.3],zoom:8}, Lumbini:{center:[27.9,83.4],zoom:8}, Karnali:{center:[29.2,82.5],zoom:7}, Sudurpashchim:{center:[29.3,80.5],zoom:7},
  Anhui:{center:[31.8,117.2],zoom:7}, Beijing:{center:[40.0,116.4],zoom:9}, Chongqing:{center:[29.5,106.5],zoom:8}, Guangdong:{center:[23.4,113.4],zoom:7}, Gansu:{center:[38.0,99.0],zoom:6}, Sichuan:{center:[30.6,102.0],zoom:7}, Yunnan:{center:[25.0,101.5],zoom:7}, Tibet:{center:[31.0,88.0],zoom:5}, Xinjiang:{center:[41.7,85.0],zoom:5},
};

function Viewport({ villages, region, district, route }: { villages: Village[]; region?: string; district?: string; route?: [number,number][] }) {
  const map=useMap();
  useEffect(()=>{
    map.invalidateSize({animate:false});
    const points=route?.length?route:villages.map(v=>[v.lat,v.lng] as [number,number]);
    if(district && points.length){ const b=L.latLngBounds(points); if(b.isValid()){ map.fitBounds(b,{padding:[55,55],maxZoom:12,animate:true,duration:.65}); return; } }
    const view=REGION_VIEWS[region||""];
    if(view){ map.setView(view.center,view.zoom,{animate:true,duration:.65}); return; }
    if(points.length && region){ const b=L.latLngBounds(points); if(b.isValid()) map.fitBounds(b,{padding:[45,45],maxZoom:9,animate:true,duration:.65}); return; }
    map.setView([25.4,86.0],5,{animate:false});
  },[map,villages,region,district,route]);
  return null;
}

export default function RiskMap({ villages, safeSites=[], selectedId, onSelectVillage, region, district, route, center=[25.4,86.0], zoom=6 }: RiskMapProps){
  const view=REGION_VIEWS[region||""];
  return <MapContainer center={view?.center||center} zoom={view?.zoom||zoom} minZoom={3} maxZoom={18} scrollWheelZoom zoomControl doubleClickZoom dragging touchZoom style={{height:"100%",width:"100%"}} preferCanvas>
    <Viewport villages={villages} region={region} district={district} route={route}/>
    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" maxZoom={19} keepBuffer={2} updateWhenIdle updateWhenZooming={false} />
    {villages.map(v=>{ const selected=v.id===selectedId; const radius=selected?20:Math.max(8,Math.min(18,7+v.risk_score/9)); return <CircleMarker key={v.id} center={[v.lat,v.lng]} radius={radius} className={`risk-pulse risk-pulse-${v.level.toLowerCase()}`} pathOptions={{color:v.color,fillColor:v.color,fillOpacity:selected?.92:.72,weight:selected?3:2}} eventHandlers={{click:()=>onSelectVillage?.(v)}}><Tooltip direction="top" offset={[0,-8]}><strong>{v.name}</strong><br/>{v.district}, {v.state}<br/><b>Risk {v.risk_score} · {v.level}</b><br/>Population {v.population.toLocaleString()}</Tooltip></CircleMarker> })}
    {safeSites.map(s=><CircleMarker key={s.id} center={[s.lat,s.lng]} radius={9} className="safe-pulse" pathOptions={{color:"#075985",fillColor:"#38bdf8",fillOpacity:.9,weight:2}}><Popup><strong>{s.name}</strong><br/>SAFE SITE · Available {s.available_capacity.toLocaleString()}<br/>Facilities: {s.facilities.slice(0,4).join(", ")}</Popup></CircleMarker>)}
    {route?.length?<Polyline positions={route} pathOptions={{color:"#2563eb",weight:5,opacity:.9,dashArray:"10 8"}}/>:null}
  </MapContainer>;
}
