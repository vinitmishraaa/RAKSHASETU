import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { Village, SafeSite } from "../../types";

interface RiskMapProps {
  villages: Village[];
  safeSites?: SafeSite[];
  selectedId?: string | null;
  onSelectVillage?: (village: Village) => void;
  center?: [number, number];
  zoom?: number;
}

export default function RiskMap({
  villages,
  safeSites = [],
  selectedId,
  onSelectVillage,
  center = [22.2, 88.65],
  zoom = 10,
}: RiskMapProps) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: "100%", width: "100%", background: "var(--bg-inset)" }}
      zoomControl={true}
    >
      {/* Free OpenStreetMap tiles - no API key required. See README for
          swapping in a Mapbox token for production-scale vector tiles. */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {villages.map((v) => {
        const isSelected = v.id === selectedId;
        return (
          <CircleMarker
            key={v.id}
            center={[v.lat, v.lng]}
            radius={isSelected ? 16 : 11}
            pathOptions={{
              color: v.color,
              fillColor: v.color,
              fillOpacity: isSelected ? 0.75 : 0.55,
              weight: isSelected ? 3 : 1.5,
            }}
            eventHandlers={{
              click: () => onSelectVillage?.(v),
            }}
          >
            <Tooltip direction="top" offset={[0, -8]}>
              <strong>{v.name}</strong>
              <br />
              Risk {v.risk_score} · {v.level}
            </Tooltip>
          </CircleMarker>
        );
      })}

      {safeSites.map((s) => (
        <CircleMarker
          key={s.id}
          center={[s.lat, s.lng]}
          radius={8}
          pathOptions={{
            color: "#4f9cd9",
            fillColor: "#4f9cd9",
            fillOpacity: 0.5,
            weight: 1.5,
            dashArray: "3 2",
          }}
        >
          <Popup>
            <strong>{s.name}</strong>
            <br />
            Available capacity: {s.available_capacity.toLocaleString()}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
