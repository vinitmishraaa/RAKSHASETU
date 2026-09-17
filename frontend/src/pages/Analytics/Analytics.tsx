import { useEffect, useMemo, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, PieChart, Pie, Cell, Legend } from "recharts";
import { api } from "../../services/api";
import type { Village } from "../../types";

const LEVEL_COLORS: Record<string, string> = { CRITICAL: "#e5484d", HIGH: "#f2994a", MODERATE: "#f5c94a", LOW: "#3fb27f" };
const n = (v: unknown) => typeof v === "number" && Number.isFinite(v) ? v : 0;

export default function Analytics() {
  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [villages, setVillages] = useState<Village[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.regions.states().then(rows => setStates(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b)))).catch(e => setError(e.message));
  }, []);

  useEffect(() => {
    setDistrict(""); setDistricts([]); setVillages([]);
    if (!state) return;
    api.regions.districts(state).then(rows => setDistricts(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b)))).catch(e => setError(e.message));
  }, [state]);

  useEffect(() => {
    setVillages([]); setError("");
    if (!state || !district) return;
    setLoading(true);
    api.villages.list({ state, district }).then(setVillages).catch(e => setError(e.message)).finally(() => setLoading(false));
  }, [state, district]);

  const counts = useMemo(() => ({
    CRITICAL: villages.filter(v => v.level === "CRITICAL").length,
    HIGH: villages.filter(v => v.level === "HIGH").length,
    MODERATE: villages.filter(v => v.level === "MODERATE").length,
    LOW: villages.filter(v => v.level === "LOW").length,
  }), [villages]);
  const populationAtRisk = villages.filter(v => v.level === "CRITICAL" || v.level === "HIGH").reduce((sum, v) => sum + n(v.population), 0);
  const barData = villages.slice(0, 30).map(v => ({ name: v.name, risk_score: n(v.risk_score), level: v.level }));
  const pieData = Object.entries(counts).map(([name, value]) => ({ name, value }));

  return <div className="scrollable" style={{ padding: 24, flex: 1 }}>
    <div className="section-heading"><div><span className="eyebrow">DECISION INTELLIGENCE</span><h2>Live Risk Analytics</h2></div><div style={{ display: "flex", gap: 10 }}><select value={state} onChange={e => setState(e.target.value)} className="analytics-region-select"><option value="">Select state / UT</option>{states.map(s => <option key={s}>{s}</option>)}</select><select value={district} onChange={e => setDistrict(e.target.value)} disabled={!state} className="analytics-region-select"><option value="">Select district</option>{districts.map(d => <option key={d}>{d}</option>)}</select></div></div>
    {error && <div className="panel" style={{ padding: 16, marginBottom: 16 }}>{error}</div>}
    {!state && <div className="panel" style={{ padding: 20 }}>Select a real Indian state or Union Territory. Districts are then loaded from live OpenStreetMap administrative data.</div>}
    {state && !district && <div className="panel" style={{ padding: 20 }}>Select a district to load its real mapped villages and calculate the analytics from the returned live records.</div>}
    {loading && <div style={{ padding: 20, color: "var(--text-muted)" }}>Loading live analytics for {district}, {state}…</div>}
    {state && district && !loading && <>
      <div className="analytics-kpis"><Kpi label="MAPPED LOCATIONS" value={villages.length}/><Kpi label="HIGH / CRITICAL POPULATION" value={populationAtRisk.toLocaleString()}/><Kpi label="CRITICAL LOCATIONS" value={counts.CRITICAL}/><Kpi label="LIVE DATA SCOPE" value={`${district}, ${state}`}/></div>
      <div className="analytics-grid"><div className="panel" style={{ padding: 20 }}><h4 className="panel-label">RISK SCORE BY LOCATION</h4><ResponsiveContainer width="100%" height={300}><BarChart data={barData}><CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" vertical={false}/><XAxis dataKey="name" stroke="var(--text-muted)" fontSize={9} tickLine={false} axisLine={false} interval={2}/><YAxis domain={[0,100]} stroke="var(--text-muted)" fontSize={10}/><Tooltip/><Bar dataKey="risk_score" radius={[4,4,0,0]}>{barData.map((v, i) => <Cell key={i} fill={LEVEL_COLORS[v.level]}/>)}</Bar></BarChart></ResponsiveContainer></div><div className="panel" style={{ padding: 20 }}><h4 className="panel-label">RISK DISTRIBUTION</h4><ResponsiveContainer width="100%" height={300}><PieChart><Pie data={pieData} dataKey="value" nameKey="name" innerRadius={58} outerRadius={96} paddingAngle={3}>{pieData.map(d => <Cell key={d.name} fill={LEVEL_COLORS[d.name]}/>)}</Pie><Legend/><Tooltip/></PieChart></ResponsiveContainer></div></div>
      <div className="analytics-section"><div className="panel" style={{ padding: 20 }}><h4 className="panel-label">RESPONSE SNAPSHOT</h4><div className="analytics-stat-row"><span><small>Population at risk</small><b>{populationAtRisk.toLocaleString()}</b></span><span><small>Critical share</small><b>{villages.length ? Math.round(counts.CRITICAL * 100 / villages.length) : 0}%</b></span></div><p className="data-note">Risk values are calculated from current Open-Meteo precipitation/wind and nearest USGS earthquake observations. They are not official government hazard ratings.</p></div></div>
    </>}
  </div>;
}
function Kpi({ label, value }: { label: string; value: string | number }) { return <div className="panel analytics-kpi"><span>{label}</span><strong className="mono">{value}</strong></div>; }
