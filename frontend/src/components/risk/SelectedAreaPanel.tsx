import RiskBadge from "../common/RiskBadge";
import type { VillageDetail } from "../../types";

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
        <span style={{ color: "var(--text-muted)" }}>{label}</span>
        <span className="mono" style={{ color: "var(--text-primary)", fontWeight: 600 }}>
          {value}
        </span>
      </div>
      <div style={{ height: 5, background: "var(--bg-inset)", borderRadius: 3, overflow: "hidden" }}>
        <div
          style={{
            width: `${Math.min(100, value)}%`,
            height: "100%",
            background: "var(--brand)",
          }}
        />
      </div>
    </div>
  );
}

export default function SelectedAreaPanel({
  village,
  onViewRelocation,
}: {
  village: VillageDetail | null;
  onViewRelocation?: () => void;
}) {
  if (!village) {
    return (
      <div className="panel" style={{ padding: 20, height: "100%" }}>
        <p style={{ fontSize: 13 }}>
          Select a village on the map to see its risk profile, drivers, and
          relocation recommendation.
        </p>
      </div>
    );
  }

  return (
    <div
      className="panel"
      style={{
        padding: 20,
        height: "100%",
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        gap: 18,
      }}
    >
      <div>
        <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 4 }}>
          {village.district}, {village.state}
        </div>
        <h3 style={{ fontSize: 18 }}>{village.name}</h3>
      </div>

      <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
        <span className="mono" style={{ fontSize: 40, fontWeight: 700, lineHeight: 1 }}>
          {village.risk_score}
        </span>
        <RiskBadge level={village.level} />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <Metric label="Hazard" value={village.hazard} />
        <Metric label="Exposure" value={village.exposure} />
        <Metric label="Vulnerability" value={village.vulnerability} />
        <Metric label="Accessibility" value={village.accessibility} />
      </div>

      <div>
        <div style={{ fontSize: 11, fontWeight: 700, color: "var(--text-muted)", marginBottom: 8 }}>
          WHY {village.level}?
        </div>
        <ul style={{ margin: 0, paddingLeft: 18, display: "flex", flexDirection: "column", gap: 5 }}>
          {village.reasons.map((r) => (
            <li key={r} style={{ fontSize: 13, color: "var(--text-secondary)" }}>
              {r}
            </li>
          ))}
        </ul>
      </div>

      <div
        style={{
          padding: "10px 12px",
          background: "var(--bg-inset)",
          borderRadius: 8,
          border: "1px solid var(--border-subtle)",
        }}
      >
        <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 3 }}>
          RECOMMENDED ACTION
        </div>
        <div style={{ fontSize: 13.5, fontWeight: 600 }}>{village.recommended_action}</div>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
        <span style={{ color: "var(--text-muted)" }}>Population</span>
        <span className="mono">{village.population.toLocaleString()}</span>
      </div>

      <button className="btn btn-primary" onClick={onViewRelocation}>
        Analyse Relocation Options
      </button>
    </div>
  );
}
