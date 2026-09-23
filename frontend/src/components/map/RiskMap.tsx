import { MapContainer, TileLayer, CircleMarker, Tooltip, Popup, Polyline, useMap, LayersControl } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./risk-map.css";
import type { Village, SafeSite, LiveHazard } from "../../types";

interface RiskMapProps {
  villages: Village[];
  safeSites?: SafeSite[];
  liveHazards?: LiveHazard[];
  selectedId?: string | null;
  onSelectVillage?: (v: Village) => void;
  region?: string;
  district?: string;
  route?: [number, number][];
  center?: [number, number];
  zoom?: number;
}

type View = { center: [number, number]; zoom: number };

const REGION_VIEWS: Record<string, View> = {
  India: { center: [22.6, 82.5], zoom: 5 },
  "West Bengal": { center: [23.5, 87.8], zoom: 7 },
  Bihar: { center: [25.7, 85.5], zoom: 7 },
  Odisha: { center: [20.5, 84.5], zoom: 7 },
  Sikkim: { center: [27.5, 88.5], zoom: 9 },
  Delhi: { center: [28.6, 77.2], zoom: 10 },
  Maharashtra: { center: [19.7, 75.7], zoom: 6 },
  Rajasthan: { center: [27.0, 74.2], zoom: 6 },
  "Uttar Pradesh": { center: [26.8, 80.9], zoom: 6 },
  "Tamil Nadu": { center: [11.1, 78.6], zoom: 7 },
  Karnataka: { center: [15.3, 75.7], zoom: 6 },
  Gujarat: { center: [22.2, 71.1], zoom: 6 },
  Kerala: { center: [10.8, 76.2], zoom: 7 },
};

function Viewport({
  villages,
  region,
  district,
  route,
}: {
  villages: Village[];
  region?: string;
  district?: string;
  route?: [number, number][];
}) {
  const map = useMap();

  useEffect(() => {
    map.invalidateSize({ animate: false });

    if (route?.length) {
      const b = L.latLngBounds(route);
      if (b.isValid()) {
        map.fitBounds(b, { padding: [60, 60], maxZoom: 14, animate: true, duration: 0.65 });
        return;
      }
    }

    const points = villages.map((v) => [v.lat, v.lng] as [number, number]);
    if (district && points.length) {
      const b = L.latLngBounds(points);
      if (b.isValid()) {
        map.fitBounds(b, { padding: [50, 50], maxZoom: 12, animate: true, duration: 0.65 });
        return;
      }
    }

    const view = REGION_VIEWS[region || ""];
    if (view && (!points.length || !district)) {
      map.setView(view.center, view.zoom, { animate: true, duration: 0.65 });
      return;
    }

    if (points.length) {
      const b = L.latLngBounds(points);
      if (b.isValid()) {
        map.fitBounds(b, { padding: [45, 45], maxZoom: 9, animate: true, duration: 0.65 });
        return;
      }
    }

    map.setView([22.5, 82.5], 5, { animate: false });
  }, [map, villages, region, district, route]);

  return null;
}

function hazardColor(h: LiveHazard) {
  if (h.severity === "CRITICAL") return "#e5484d";
  if (h.severity === "HIGH") return "#f2994a";
  if (h.severity === "MODERATE") return "#f5c94a";
  return "#3fb27f";
}

export default function RiskMap({
  villages,
  safeSites = [],
  liveHazards = [],
  selectedId,
  onSelectVillage,
  region = "West Bengal",
  district,
  route,
  center = [23.5, 87.8],
  zoom = 7,
}: RiskMapProps) {
  const view = REGION_VIEWS[region || ""];
  const satelliteDate = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const pointHazards = liveHazards.filter((h): h is LiveHazard & { lat: number; lng: number } => h.lat != null && h.lng != null);

  return (
    <MapContainer
      center={view?.center || center}
      zoom={view?.zoom || zoom}
      minZoom={3}
      maxZoom={18}
      scrollWheelZoom
      zoomControl
      doubleClickZoom
      dragging
      touchZoom
      style={{ height: "100%", width: "100%" }}
      preferCanvas
    >
      <Viewport villages={villages} region={region} district={district} route={route} />

      <LayersControl position="topright">
        <LayersControl.BaseLayer checked name="OpenStreetMap Standard">
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            maxZoom={19}
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          />
        </LayersControl.BaseLayer>
        <LayersControl.Overlay name="NASA GIBS Satellite (NRT)">
          <TileLayer
            url={`https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_SNPP_CorrectedReflectance_TrueColor/default/${satelliteDate}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg`}
            opacity={0.85}
            maxZoom={9}
          />
        </LayersControl.Overlay>
      </LayersControl>

      {/* 1. CRITICAL ZONES: Buffering radar blowout expansion animation */}
      {villages
        .filter((v) => v.level === "CRITICAL")
        .map((v) => {
          const selected = v.id === selectedId;
          const radius = selected ? 22 : 14;
          return (
            <CircleMarker
              key={`blowout-${v.id}`}
              center={[v.lat, v.lng]}
              radius={radius + 10}
              className="risk-zone-blowout-critical"
              pathOptions={{
                color: "#e5484d",
                fillColor: "#e5484d",
                fillOpacity: 0.18,
                weight: 2.5,
              }}
            />
          );
        })}

      {/* 2. ALL RISK ZONES: Core marker with interactive tooltip & click */}
      {villages.map((v) => {
        const isCritical = v.level === "CRITICAL";
        const isHigh = v.level === "HIGH";
        const isModerate = v.level === "MODERATE";
        const selected = v.id === selectedId;

        const baseRadius = selected ? 18 : isCritical ? 13 : isHigh ? 11 : isModerate ? 9 : 8;
        const color = isCritical ? "#e5484d" : isHigh ? "#f2994a" : isModerate ? "#f5c94a" : "#3fb27f";
        const markerClass = isCritical ? "risk-core-critical" : isHigh ? "risk-zone-high" : isModerate ? "risk-zone-moderate" : "risk-zone-low";

        return (
          <CircleMarker
            key={v.id}
            center={[v.lat, v.lng]}
            radius={baseRadius}
            className={markerClass}
            pathOptions={{
              color: color,
              fillColor: color,
              fillOpacity: selected ? 0.95 : 0.85,
              weight: selected ? 3.5 : 2,
            }}
            eventHandlers={{
              click: () => onSelectVillage?.(v),
            }}
          >
            <Tooltip direction="top" offset={[0, -8]}>
              <div style={{ fontSize: "12px", lineHeight: "1.4", minWidth: "180px" }}>
                {v.is_red_zone && (
                  <div style={{ color: "#ff8095", fontWeight: 800, fontSize: "10px", marginBottom: "2px" }}>
                    ⚠️ MULTI-HAZARD RED ZONE
                  </div>
                )}
                <strong>{v.name}</strong>
                <br />
                <span style={{ color: "#64748b" }}>
                  {v.district || district}, {v.state || region}
                </span>
                <br />
                <b style={{ color }}>
                  Risk Index: {v.risk_score}/100 ({v.level})
                </b>
                <br />
                <span style={{ color: "#f5c94a", fontWeight: 700, fontSize: "11px" }}>
                  Priority: {v.relocation_horizon || (v.level === "CRITICAL" ? "0–48 Hours (Immediate)" : "1–3 Months")}
                </span>
                <br />
                <span>Population: {v.population != null ? v.population.toLocaleString() : "—"}</span>
                {v.primary_hazard_trigger && (
                  <>
                    <br />
                    <small style={{ color: "#94a3b8" }}>Trigger: {v.primary_hazard_trigger}</small>
                  </>
                )}
                {v.weather?.precipitation_mm ? (
                  <>
                    <br />
                    <span>Live rain: {v.weather.precipitation_mm} mm/h</span>
                  </>
                ) : null}
              </div>
            </Tooltip>
          </CircleMarker>
        );
      })}

      {/* 3. SAFE SHELTERS: Green glowing pulse with buffer rings */}
      {safeSites.map((s) => (
        <CircleMarker
          key={`safe-buffer-${s.id}`}
          center={[s.lat, s.lng]}
          radius={15}
          className="safe-buffer-green"
          pathOptions={{
            color: "#10b981",
            fillColor: "#10b981",
            fillOpacity: 0.12,
            weight: 1.5,
          }}
        />
      ))}

      {safeSites.map((s) => (
        <CircleMarker
          key={s.id}
          center={[s.lat, s.lng]}
          radius={9}
          className="safe-pulse-green"
          pathOptions={{
            color: "#059669",
            fillColor: "#10b981",
            fillOpacity: 0.95,
            weight: 2.5,
          }}
        >
          <Popup>
            <div style={{ minWidth: "190px", fontSize: "12px", lineHeight: "1.4" }}>
              <div style={{ color: "#10b981", fontWeight: "bold", textTransform: "uppercase", fontSize: "10px" }}>
                DESIGNATED SAFE SHELTER
              </div>
              <strong style={{ fontSize: "13px" }}>{s.name}</strong>
              <br />
              <span style={{ color: "#64748b" }}>
                {s.district || district}, {s.state || region}
              </span>
              <br />
              <b>Capacity: {s.capacity != null ? s.capacity.toLocaleString() : "—"}</b>
              <br />
              <span style={{ color: "#059669" }}>
                Available Intake: {s.available_capacity != null ? s.available_capacity.toLocaleString() : "Full"}
              </span>
              <br />
              <small style={{ color: "#475569" }}>
                Facilities: {s.facilities?.slice(0, 3).join(", ") || "Medical & shelter wings"}
              </small>
            </div>
          </Popup>
        </CircleMarker>
      ))}

      {/* 4. LIVE HAZARD OBSERVATIONS: USGS Earthquakes & NASA FIRMS */}
      {pointHazards.map((h) => {
        const c = hazardColor(h);
        const isFire = h.type.toLowerCase().includes("fire");
        const radius = isFire ? 8 : Math.max(8, Math.min(16, 7 + (h.magnitude || 2)));

        return (
          <CircleMarker
            key={`live-${h.id}`}
            center={[h.lat, h.lng]}
            radius={radius}
            className="live-hazard-pulse"
            pathOptions={{
              color: c,
              fillColor: c,
              fillOpacity: 0.9,
              weight: 2,
            }}
          >
            <Popup>
              <div className="live-popup">
                <div className="live-popup-kicker">LIVE {h.type.toUpperCase()}</div>
                <strong>{h.title || "Hazard observation"}</strong>
                <span>{h.detail || "Public real-time observation"}</span>
                <b style={{ color: c }}>
                  {isFire
                    ? h.frp != null
                      ? `FRP ${h.frp.toFixed(1)} MW · ${h.severity}`
                      : h.severity
                    : `Magnitude ${h.magnitude?.toFixed(1) ?? "—"} · ${h.severity}`}
                </b>
                <small>Source: {h.source}</small>
                {h.url && (
                  <a href={h.url} target="_blank" rel="noreferrer">
                    View official source report →
                  </a>
                )}
              </div>
            </Popup>
          </CircleMarker>
        );
      })}

      {/* 5. EVACUATION ROUTE: OSRM Driving Route Corridor */}
      {route?.length ? (
        <Polyline
          positions={route}
          pathOptions={{
            color: "#0284c7",
            weight: 5,
            opacity: 0.9,
            dashArray: "10 8",
          }}
        />
      ) : null}
    </MapContainer>
  );
}
