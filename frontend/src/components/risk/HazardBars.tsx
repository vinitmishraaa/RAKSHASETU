import type { VillageDetail } from "../../types";

function Bar({ label, value, color }: { label: string; value?: number | null; color: string }) {
  const v = typeof value === "number" && Number.isFinite(value) ? Math.min(Math.max(Math.round(value), 0), 100) : 0;
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 4 }}>
        <span style={{ color: "var(--text-secondary)" }}>{label}</span>
        <span className="mono" style={{ fontWeight: 600 }}>{v}/100</span>
      </div>
      <div style={{ height: 7, background: "var(--bg-inset)", borderRadius: 4, overflow: "hidden" }}>
        <div style={{ width: `${v}%`, height: "100%", background: color, borderRadius: 4 }} />
      </div>
    </div>
  );
}

export default function HazardBars({ village }: { village: VillageDetail }) {
  return (
    <div className="panel" style={{ padding: 18 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
        <h4 style={{ fontSize: 12, color: "var(--text-muted)", margin: 0 }}>
          MULTI-HAZARD PROFILE (SIH PS 26191)
        </h4>
        {village.is_red_zone && (
          <span style={{ fontSize: 9, fontWeight: 800, color: "#ff8095", background: "rgba(255, 23, 68, 0.15)", padding: "2px 6px", borderRadius: 4, border: "1px solid rgba(255, 23, 68, 0.3)" }}>
            RED ZONE
          </span>
        )}
      </div>

      <Bar label="Floods & Inundation" value={village.flood_hazard} color="#29b6f6" />
      <Bar label="Landslides & Slope Failure" value={village.landslide_hazard} color="#ff9800" />
      <Bar label="Coastal Erosion & Storm Surge" value={village.coastal_erosion_hazard ?? village.cyclone_hazard} color="#26a69a" />
      <Bar label="Cloudburst & Flash Rainfall" value={village.cloudburst_hazard ?? (village.rainfall_mm_month ? Math.min(Math.round(village.rainfall_mm_month / 4), 95) : 35)} color="#ab47bc" />

      {village.primary_hazard_trigger && (
        <div style={{ marginTop: 10, padding: "8px 10px", background: "var(--bg-inset)", borderRadius: 6, border: "1px solid var(--border-subtle)", fontSize: 10 }}>
          <strong style={{ color: "var(--text-muted)" }}>Primary Trigger: </strong>
          <span style={{ color: "var(--brand-soft)" }}>{village.primary_hazard_trigger}</span>
        </div>
      )}
    </div>
  );
}
