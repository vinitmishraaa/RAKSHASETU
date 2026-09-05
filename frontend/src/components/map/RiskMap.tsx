import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup, Polyline, useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./risk-map.css";
import type { Village, SafeSite } from "../../types";

interface RiskMapProps {
  villages: Village[];
  safeSites?: SafeSite[];
  selectedId?: string | null;
  onSelectVillage?: (village: Village) => void;
  region?: string;
  district?: string;
  route?: [number, number][];
  center?: [number, number];
  zoom?: number;
}

const REGION_VIEWS: Record<string, { center: [number, number]; zoom: number }> = {
  India: [22.6, 79.0, 5] as any,
  Nepal: [28.3, 84.2, 7] as any,
  China: [35.8, 103.8, 4] as any,
  "West Bengal": [23.9, 87.8, 7] as any,
  Bihar: [25.9, 85.7, 7] as any,
  Odisha: [20.4, 84.4, 7] as any,
  Jharkhand: [23.6, 85.3, 7] as any,
  Sikkim: [27.6, 88.5, 9] as any,
};

function Viewport({ villages, region, district, route }: { villages: Village[]; region?: string; district?: string; route?: [number, number][] }) {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize({ animate: false });
    const points = route?.length ? route : villages.map((v) => [v.lat, v.lng] as [number, number]);
    if (points.length && (district || region || route?.length)) {
      const bounds = L.latLngBounds(points);
      if (bounds.isValid()) map.fitBounds(bounds, { padding: [42, 42], maxZoom: route?.length ? 13 : district ? 11 : 8, animate: true, duration: 0.55 });
      return;
    }
    const view = REGION_VIEWS[region || ""];
    if (view) map.setView([view[0] as number, view[1] as number], view[2] as number, { animate: true });
    else map.fitBounds([[5, 65], [38, 100]], { padding: [20, 20], maxZoom: 5, animate: false });
  }, [map, villages, region, district, route]);
  return null;
}

export default function RiskMap({ villages, safeSites = [], selectedId, onSelectVillage, region, district, route, center = [25.4, 86.0], zoom = 6 }: RiskMapProps) {
  const view = REGION_VIEWS[region || ""];
  return <MapContainer center={view ? [view[0] as number, view[1] as number] : center} zoom={view ? view[2] as number : zoom} minZoom={3} maxZoom={17} scrollWheelZoom zoomControl doubleClickZoom dragging touchZoom style={{ height: "100%", width: "100%" }} preferCanvas>
    <Viewport villages={villages} region={region} district={district} route={route} />
    <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" maxZoom={19} keepBuffer={4} updateWhenIdle={false} updateWhenZooming />
    {villages.map((v) => {
      const isSelected = v.id === selectedId;
      const radius = isSelected ? 18 : Math.max(9, Math.min(17, 8 + v.risk_score / 10));
      return <CircleMarker key={v.id} center={[v.lat, v.lng]} radius={radius} className={`risk-pulse risk-pulse-${v.level.toLowerCase()}`} pathOptions={{ color: v.color, fillColor: v.color, fillOpacity: isSelected ? 0.9 : 0.68, weight: isSelected ? 3 : 2 }} eventHandlers={{ click: () => onSelectVillage?.(v) }}>
        <Tooltip direction="top" offset={[0, -8]}><strong>{v.name}</strong><br />{v.district}, {v.state}<br /><b>Risk {v.risk_score} · {v.level}</b><br />Population {v.population.toLocaleString()}</Tooltip>
      </CircleMarker>;
    })}
    {safeSites.map((s) => <CircleMarker key={s.id} center={[s.lat, s.lng]} radius={9} pathOptions={{ color: "#1565c0", fillColor: "#42a5f5", fillOpacity: 0.9, weight: 2 }}><Popup><strong>{s.name}</strong><br />SAFE SITE · Available {s.available_capacity.toLocaleString()}<br />Facilities: {s.facilities.slice(0, 4).join(", ")}</Popup></CircleMarker>)}
    {route?.length ? <Polyline positions={route} pathOptions={{ color: "#1565c0", weight: 5, opacity: 0.9, dashArray: "10 8" }} /> : null}
  </MapContainer>;
}
