import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell, Legend,
} from "recharts";
import { api } from "../../services/api";

const LEVEL_COLORS: Record<string, string> = {
  CRITICAL: "#e5484d",
  HIGH: "#f2994a",
  MODERATE: "#f5c94a",
  LOW: "#3fb27f",
};

export default function Analytics() {
  const [overview, setOverview] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    api.reports.overview().then(setOverview);
    api.risk.summary().then(setSummary);
  }, []);

  if (!overview || !summary) {
    return <div style={{ padding: 24, color: "var(--text-muted)" }}>Loading analytics…</div>;
  }

  const pieData = Object.entries(summary.counts).map(([level, count]) => ({
    name: level,
    value: count as number,
  }));

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <h2 style={{ fontSize: 20, marginBottom: 4 }}>Analytics</h2>
      <p style={{ marginBottom: 20 }}>
        System-wide risk distribution and population exposure across {summary.total_villages} settlements.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 16, marginBottom: 16 }}>
        <div className="panel" style={{ padding: 20 }}>
          <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 6 }}>
            POPULATION AT HIGH/CRITICAL RISK
          </div>
          <div className="mono" style={{ fontSize: 32, fontWeight: 800 }}>
            {summary.population_at_risk.toLocaleString()}
          </div>
        </div>
        <div className="panel" style={{ padding: 20 }}>
          <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 6 }}>
            TOTAL SETTLEMENTS MONITORED
          </div>
          <div className="mono" style={{ fontSize: 32, fontWeight: 800 }}>
            {summary.total_villages}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 16 }}>
        <div className="panel" style={{ padding: 20 }}>
          <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
            RISK SCORE BY VILLAGE
          </h4>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={overview.villages}>
              <CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{
                  background: "var(--bg-panel-raised)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Bar dataKey="risk_score" radius={[4, 4, 0, 0]}>
                {overview.villages.map((v: any, i: number) => (
                  <Cell key={i} fill={LEVEL_COLORS[v.level]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="panel" style={{ padding: 20 }}>
          <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
            RISK DISTRIBUTION
          </h4>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={90} paddingAngle={2}>
                {pieData.map((d, i) => (
                  <Cell key={i} fill={LEVEL_COLORS[d.name]} />
                ))}
              </Pie>
              <Legend />
              <Tooltip
                contentStyle={{
                  background: "var(--bg-panel-raised)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
