import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup, useMap } from "react-leaflet";
import { useEffect } from "react";
import "leaflet/dist/leaflet.css";
import type { Village, SafeSite } from "../../types";

interface RiskMapProps { villages: Village[]; safeSites?: SafeSite[]; selectedId?: string | null; onSelectVillage?: (village: Village) => void; center?: [number, number]; zoom?: number; }

function RegionalViewport({ region }: { region?: string }) {
  const map = useMap();
  useEffect(() => {
    if (!region) {
      map.fitBounds([[20.0, 80.0], [30.8, 90.0]], { padding: [18, 18] });
    }
  }, [map, region]);
  return null;
}

export default function RiskMap({ villages, safeSites = [], selectedId, onSelectVillage, center = [25.4, 86.0], zoom = 6 }: RiskMapProps) {
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: "100%", width: "100%", background: "var(--bg-inset)" }} zoomControl>
      <RegionalViewport />
      <TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {villages.map((v) => {
        const isSelected = v.id === selectedId;
        return (
          <CircleMarker key={v.id} center={[v.lat, v.lng]} radius={isSelected ? 16 : 10} pathOptions={{ color: v.color, fillColor: v.color, fillOpacity: isSelected ? 0.82 : 0.58, weight: isSelected ? 3 : 1.5 }} eventHandlers={{ click: () => onSelectVillage?.(v) }}>
            <Tooltip direction="top" offset={[0, -8]}><strong>{v.name}</strong><br />{v.district}, {v.state}<br />Risk {v.risk_score} · {v.level}</Tooltip>
          </CircleMarker>
        );
      })}

      {safeSites.map((s) => (
        <CircleMarker key={s.id} center={[s.lat, s.lng]} radius={8} pathOptions={{ color: "#4db6e8", fillColor: "#4db6e8", fillOpacity: 0.7, weight: 2 }}>
          <Popup><strong>{s.name}</strong><br />Available capacity: {s.available_capacity.toLocaleString()}<br />Facilities: {s.facilities.slice(0, 3).join(", ")}</Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
