import { useEffect, useMemo, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, PieChart, Pie, Cell, Legend } from "recharts";
import { api } from "../../services/api";

const LEVEL_COLORS: Record<string, string> = { CRITICAL: "#e5484d", HIGH: "#f2994a", MODERATE: "#f5c94a", LOW: "#3fb27f" };
const REGIONS = ["All target regions", "West Bengal", "Bihar", "Odisha", "Jharkhand", "Sikkim", "Nepal"];

export default function Analytics() {
  const [region, setRegion] = useState("All target regions");
  const [overview, setOverview] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    setOverview(null); setSummary(null); setError("");
    Promise.all([
      api.reports.overview(region === "All target regions" ? undefined : region),
      api.risk.summary(),
    ]).then(([o, s]) => { setOverview(o); setSummary(s); }).catch((e) => setError(e.message));
  }, [region]);

  const pieData = useMemo(() => overview ? Object.entries(overview.counts || {}).map(([name, value]) => ({ name, value })) : [], [overview]);
  const regionalRows = overview?.by_region || [];
  const topDistricts = [...(overview?.by_district || [])].sort((a, b) => b.avg_risk - a.avg_risk).slice(0, 10);

  if (error) return <div className="scrollable" style={{ padding: 24 }}><h2>Analytics</h2><p>{error}</p></div>;
  if (!overview || !summary) return <div className="scrollable" style={{ padding: 24, color: "var(--text-muted)" }}>Loading regional analytics…</div>;

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <div className="section-heading">
        <div><span className="eyebrow">DECISION INTELLIGENCE</span><h2>Historical & Regional Analytics</h2></div>
        <select value={region} onChange={(e) => setRegion(e.target.value)} className="analytics-region-select">
          {REGIONS.map((r) => <option key={r}>{r}</option>)}
        </select>
      </div>
      <p style={{ marginBottom: 20 }}>Compare current risk concentration, population exposure and district-level patterns across the response region.</p>

      <div className="analytics-kpis">
        <Kpi label="MONITORED LOCATIONS" value={overview.total_villages} />
        <Kpi label="HIGH / CRITICAL POPULATION" value={overview.population_at_risk.toLocaleString()} />
        <Kpi label="CRITICAL LOCATIONS" value={overview.counts.CRITICAL} />
        <Kpi label="REGIONS WITH DATA" value={regionalRows.length} />
      </div>

      <div className="analytics-grid">
        <div className="panel" style={{ padding: 20 }}>
          <h4 className="panel-label">RISK SCORE BY MONITORED LOCATION</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={overview.villages.slice(0, 30)}>
              <CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={9} tickLine={false} axisLine={false} interval={2} />
              <YAxis domain={[0, 100]} stroke="var(--text-muted)" fontSize={10} />
              <Tooltip contentStyle={{ background: "var(--bg-panel-raised)", border: "1px solid var(--border-subtle)", borderRadius: 8 }} />
              <Bar dataKey="risk_score" radius={[4, 4, 0, 0]}>{overview.villages.slice(0, 30).map((v: any, i: number) => <Cell key={i} fill={LEVEL_COLORS[v.level]} />)}</Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="panel" style={{ padding: 20 }}>
          <h4 className="panel-label">RISK DISTRIBUTION</h4>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart><Pie data={pieData} dataKey="value" nameKey="name" innerRadius={58} outerRadius={96} paddingAngle={3}>{pieData.map((d: any, i: number) => <Cell key={i} fill={LEVEL_COLORS[d.name]} />)}</Pie><Legend /><Tooltip /></PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="analytics-section">
        <div className="panel" style={{ padding: 20 }}>
          <h4 className="panel-label">REGIONAL RISK COMPARISON</h4>
          <div className="regional-table">
            {regionalRows.map((r: any) => <div className="regional-row" key={r.region}><strong>{r.region}</strong><span>{r.villages} locations</span><span>Avg risk <b>{r.avg_risk}</b></span><span className="risk-count">{r.critical} critical · {r.high} high</span></div>)}
          </div>
        </div>
        <div className="panel" style={{ padding: 20 }}>
          <h4 className="panel-label">HIGHEST-RISK DISTRICTS</h4>
          <div className="regional-table">{topDistricts.map((d: any, i: number) => <div className="regional-row" key={`${d.region}-${d.district}`}><strong>{i + 1}. {d.district}</strong><span>{d.region}</span><span>Avg risk <b>{d.avg_risk}</b></span></div>)}</div>
        </div>
      </div>

      <div className="panel insight-panel">
        <span className="eyebrow">RESPONSE INSIGHT</span>
        <h3>What this means for officers</h3>
        <p>Prioritize critical and high-risk clusters first, verify safe-site capacity before issuing relocation orders, and use historical incident patterns to validate preparedness actions. Current figures are prototype synthetic intelligence until verified GIS, weather and incident feeds are connected.</p>
      </div>
    </div>
  );
}

function Kpi({ label, value }: { label: string; value: string | number }) { return <div className="panel analytics-kpi"><span>{label}</span><strong className="mono">{value}</strong></div>; }
