import { useEffect, useState } from "react";
import { api } from "../../services/api";
import type { SafeSite } from "../../types";

export default function SafeSites() {
  const [sites, setSites] = useState<SafeSite[]>([]);

  useEffect(() => {
    api.safeSites.list().then(setSites);
  }, []);

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <h2 style={{ fontSize: 20, marginBottom: 4 }}>Safe Sites</h2>
      <p style={{ marginBottom: 20 }}>
        Candidate relocation destinations with current capacity and infrastructure.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16 }}>
        {sites.map((s) => {
          const occupancyPct = Math.round((s.current_occupancy / s.capacity) * 100);
          return (
            <div key={s.id} className="panel" style={{ padding: 20 }}>
              <h3 style={{ fontSize: 15, marginBottom: 2 }}>{s.name}</h3>
              <div className="mono" style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 16 }}>
                {s.id}
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 16 }}>
                <Field label="Capacity" value={s.capacity.toLocaleString()} />
                <Field label="Available" value={s.available_capacity.toLocaleString()} />
                <Field label="Hazard risk" value={`${s.hazard_risk}/100`} />
                <Field label="Infrastructure" value={`${s.infrastructure_score}/100`} />
              </div>

              <div style={{ marginBottom: 16 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 4 }}>
                  <span style={{ color: "var(--text-muted)" }}>Occupancy</span>
                  <span className="mono">{occupancyPct}%</span>
                </div>
                <div style={{ height: 6, background: "var(--bg-inset)", borderRadius: 3, overflow: "hidden" }}>
                  <div
                    style={{
                      width: `${occupancyPct}%`,
                      height: "100%",
                      background: occupancyPct > 80 ? "var(--risk-high)" : "var(--info)",
                    }}
                  />
                </div>
              </div>

              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {s.facilities.map((f) => (
                  <span
                    key={f}
                    style={{
                      fontSize: 11,
                      padding: "4px 8px",
                      borderRadius: 6,
                      background: "var(--bg-inset)",
                      color: "var(--text-secondary)",
                      border: "1px solid var(--border-subtle)",
                    }}
                  >
                    {f}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div style={{ fontSize: 10.5, color: "var(--text-muted)" }}>{label}</div>
      <div className="mono" style={{ fontSize: 14, fontWeight: 700 }}>{value}</div>
    </div>
  );
}
