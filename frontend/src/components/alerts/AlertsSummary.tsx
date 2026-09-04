import type { Alert } from "../../types";

const ICON: Record<string, string> = {
  CRITICAL: "🔴",
  HIGH: "🟠",
  WARNING: "🟡",
};

export default function AlertsSummary({ alerts }: { alerts: Alert[] }) {
  const counts = alerts.reduce<Record<string, number>>((acc, a) => {
    acc[a.level] = (acc[a.level] || 0) + 1;
    return acc;
  }, {});

  const rows = [
    { level: "CRITICAL", label: "Critical Zones" },
    { level: "HIGH", label: "High-Risk Villages" },
    { level: "WARNING", label: "Capacity Warnings" },
  ];

  return (
    <div className="panel" style={{ padding: 20 }}>
      <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 14 }}>ALERTS</h4>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {rows.map((r) => (
          <div key={r.level} style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
            <span>
              {ICON[r.level]} {r.label}
            </span>
            <span className="mono" style={{ fontWeight: 700 }}>
              {counts[r.level] || 0}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
