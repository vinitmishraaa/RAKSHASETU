import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import type { VillageDetail } from "../../types";

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export default function RainfallTrendChart({ village }: { village: VillageDetail }) {
  const data = village.rainfall_trend.map((mm, i) => ({ month: MONTHS[i], mm }));

  return (
    <div className="panel" style={{ padding: 20 }}>
      <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
        RAINFALL TREND (mm / month)
      </h4>
      <ResponsiveContainer width="100%" height={180}>
        <LineChart data={data}>
          <CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="month" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} width={32} />
          <Tooltip
            contentStyle={{
              background: "var(--bg-panel-raised)",
              border: "1px solid var(--border-subtle)",
              borderRadius: 8,
              fontSize: 12,
            }}
          />
          <Line type="monotone" dataKey="mm" stroke="var(--info)" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
