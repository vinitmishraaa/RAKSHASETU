import { useEffect, useState } from "react";
import { api } from "../../services/api";
import "./region-history.css";

type EventRow = { year: number; hazard: string; severity: string; zones_affected: number };

export default function RegionHistoryPanel({ region, district }: { region: string; district?: string }) {
  const [data, setData] = useState<{ events: EventRow[]; hazard_counts: Record<string, number> } | null>(null);
  useEffect(() => { let active = true; setData(null); api.history.region(region, district).then((value) => active && setData(value)).catch(() => active && setData({ events: [], hazard_counts: {} })); return () => { active = false; }; }, [region, district]);
  if (!region) return null;
  const hazards = Object.entries(data?.hazard_counts || {}).sort((a, b) => b[1] - a[1]);
  const max = Math.max(1, ...hazards.map(([, value]) => value));
  return <section className="region-history-panel panel">
    <div className="section-heading"><div><span className="eyebrow">HISTORICAL INTELLIGENCE</span><h2>{district || region} Past Incidents</h2></div><span>{data?.events.length || 0} event records</span></div>
    <div className="history-analytics-grid">
      <div className="history-chart"><strong>Hazard recurrence</strong>{hazards.length ? hazards.map(([hazard, count]) => <div className="hazard-row" key={hazard}><span>{hazard}</span><div><i style={{ width: `${Math.max(8, (count / max) * 100)}%` }} /></div><b>{count}</b></div>) : <p>Historical records will appear here when verified datasets are connected.</p>}</div>
      <div className="incident-list"><strong>Recent incident context</strong>{data?.events.slice(0, 6).map((event) => <article key={`${event.year}-${event.hazard}-${event.severity}`}><div><b>{event.year}</b><span>{event.hazard}</span></div><small>{event.severity} · {event.zones_affected} monitored zones</small></article>) || <p>Loading historical intelligence…</p>}</div>
    </div>
    <div className="response-benefits"><span className="eyebrow">WHY THIS HELPS</span><div><span>01 <b>Compare recurrence</b><small>Prioritize hazards repeatedly affecting the selected geography.</small></span><span>02 <b>Plan vulnerable groups</b><small>Use population and safe-site capacity before evacuation pressure peaks.</small></span><span>03 <b>Measure readiness</b><small>Compare current risk with previous incidents and response actions.</small></span></div></div>
    <p className="data-note">Prototype historical layer — verify every incident against authoritative records before operational use.</p>
  </section>;
}
