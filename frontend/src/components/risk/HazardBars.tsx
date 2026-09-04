import type { VillageDetail } from "../../types";

function Bar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12.5, marginBottom: 5 }}>
        <span style={{ color: "var(--text-secondary)" }}>{label}</span>
        <span className="mono" style={{ fontWeight: 600 }}>{value}</span>
      </div>
      <div style={{ height: 8, background: "var(--bg-inset)", borderRadius: 4, overflow: "hidden" }}>
        <div style={{ width: `${value}%`, height: "100%", background: color, borderRadius: 4 }} />
      </div>
    </div>
  );
}

export default function HazardBars({ village }: { village: VillageDetail }) {
  return (
    <div className="panel" style={{ padding: 20 }}>
      <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
        HAZARD ANALYSIS
      </h4>
      <Bar label="Flood risk" value={village.flood_hazard} color="var(--info)" />
      <Bar label="Cyclone risk" value={village.cyclone_hazard} color="var(--brand)" />
      <Bar label="Landslide risk" value={village.landslide_hazard} color="var(--risk-moderate)" />
    </div>
  );
}
