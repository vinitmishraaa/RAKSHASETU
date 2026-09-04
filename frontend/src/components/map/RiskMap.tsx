import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup, useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./risk-map.css";
import type { Village, SafeSite } from "../../types";

interface RiskMapProps { villages: Village[]; safeSites?: SafeSite[]; selectedId?: string | null; onSelectVillage?: (village: Village) => void; region?: string; district?: string; center?: [number, number]; zoom?: number; }

function Viewport({ villages, region, district }: { villages: Village[]; region?: string; district?: string }) {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize();
    if (!villages.length) return;
    if (district || region) {
      const bounds = L.latLngBounds(villages.map((v) => [v.lat, v.lng] as [number, number]));
      map.fitBounds(bounds.pad(0.35), { padding: [24, 24], maxZoom: district ? 10 : 7, animate: true, duration: 0.7 });
    } else {
      map.fitBounds([[20.0, 80.0], [30.8, 90.0]], { padding: [20, 20], maxZoom: 7, animate: false });
    }
  }, [map, villages, region, district]);
  return null;
}

export default function RiskMap({ villages, safeSites = [], selectedId, onSelectVillage, region, district, center = [25.4, 86.0], zoom = 6 }: RiskMapProps) {
  return (
    <MapContainer center={center} zoom={zoom} minZoom={4} maxZoom={14} scrollWheelZoom zoomControl doubleClickZoom dragging touchZoom style={{ height: "100%", width: "100%" }} preferCanvas>
      <Viewport villages={villages} region={region} district={district} />
      <TileLayer attribution='&copy; OpenStreetMap contributors &copy; CARTO' url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" maxZoom={20} keepBuffer={2} updateWhenIdle />
      {villages.map((v) => {
        const isSelected = v.id === selectedId;
        return <CircleMarker key={v.id} center={[v.lat, v.lng]} radius={isSelected ? 15 : 10} className={`risk-pulse risk-pulse-${v.level.toLowerCase()}`} pathOptions={{ color: v.color, fillColor: v.color, fillOpacity: isSelected ? 0.85 : 0.62, weight: isSelected ? 3 : 2 }} eventHandlers={{ click: () => onSelectVillage?.(v) }}>
          <Tooltip direction="top" offset={[0, -8]}><strong>{v.name}</strong><br />{v.district}, {v.state}<br /><b>Risk {v.risk_score} · {v.level}</b><br />Population {v.population.toLocaleString()}</Tooltip>
        </CircleMarker>;
      })}
      {safeSites.map((s) => <CircleMarker key={s.id} center={[s.lat, s.lng]} radius={8} pathOptions={{ color: "#1976d2", fillColor: "#43a5f5", fillOpacity: 0.88, weight: 2 }}><Popup><strong>{s.name}</strong><br />SAFE SITE · Available {s.available_capacity.toLocaleString()}<br />Facilities: {s.facilities.slice(0, 4).join(", ")}</Popup></CircleMarker>)}
    </MapContainer>
  );
}
