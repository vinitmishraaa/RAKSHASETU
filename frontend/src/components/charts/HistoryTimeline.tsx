import type { VillageDetail } from "../../types";

const SEVERITY_COLOR: Record<string, string> = {
  Critical: "var(--risk-critical)",
  High: "var(--risk-high)",
  Moderate: "var(--risk-moderate)",
  Low: "var(--risk-low)",
};

export default function HistoryTimeline({ village }: { village: VillageDetail }) {
  return (
    <div className="panel" style={{ padding: 20 }}>
      <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
        HISTORICAL EVENTS
      </h4>
      {village.history.length === 0 ? (
        <p style={{ fontSize: 13 }}>No recorded disaster events for this settlement.</p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
          {village.history.map((event, i) => (
            <div key={i} style={{ display: "flex", gap: 14, position: "relative" }}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <div
                  style={{
                    width: 9,
                    height: 9,
                    borderRadius: "50%",
                    background: SEVERITY_COLOR[event.severity] || "var(--text-muted)",
                    marginTop: 4,
                  }}
                />
                {i < village.history.length - 1 && (
                  <div style={{ width: 1, flex: 1, background: "var(--border-subtle)", minHeight: 28 }} />
                )}
              </div>
              <div style={{ paddingBottom: 20 }}>
                <div className="mono" style={{ fontSize: 12, color: "var(--text-muted)" }}>
                  {event.year}
                </div>
                <div style={{ fontSize: 14, fontWeight: 600 }}>{event.hazard}</div>
                <div style={{ fontSize: 12, color: SEVERITY_COLOR[event.severity] }}>
                  {event.severity} severity
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
