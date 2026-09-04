import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import type { SafeSite } from "../../types";

const REGIONS = ["All regions", "West Bengal", "Bihar", "Odisha", "Jharkhand", "Sikkim", "Nepal"];

export default function SafeSites() {
  const [sites, setSites] = useState<SafeSite[]>([]);
  const [region, setRegion] = useState("All regions");

  useEffect(() => { api.safeSites.list().then(setSites); }, []);

  const visibleSites = useMemo(() => region === "All regions" ? sites : sites.filter((s) => (s as SafeSite & { region?: string }).region === region), [sites, region]);
  const totalCapacity = visibleSites.reduce((sum, s) => sum + s.capacity, 0);
  const availableCapacity = visibleSites.reduce((sum, s) => sum + s.available_capacity, 0);

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "flex-start", marginBottom: 20 }}>
        <div>
          <h2 style={{ fontSize: 20, marginBottom: 4 }}>Safe Sites</h2>
          <p>Regional emergency shelters ranked for safety, capacity, access and suitability.</p>
        </div>
        <select value={region} onChange={(e) => setRegion(e.target.value)} className="filter-select" aria-label="Filter safe sites by region">
          {REGIONS.map((r) => <option key={r}>{r}</option>)}
        </select>
      </div>

      <div className="kpi-grid" style={{ marginBottom: 16 }}>
        <div className="panel kpi-card"><span>SAFE SITES</span><strong>{visibleSites.length}</strong></div>
        <div className="panel kpi-card"><span>TOTAL CAPACITY</span><strong>{totalCapacity.toLocaleString()}</strong></div>
        <div className="panel kpi-card"><span>AVAILABLE CAPACITY</span><strong>{availableCapacity.toLocaleString()}</strong></div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16 }}>
        {visibleSites.map((s) => {
          const occupancyPct = s.capacity ? Math.min(100, Math.round((s.current_occupancy / s.capacity) * 100)) : 0;
          const siteRegion = (s as SafeSite & { region?: string }).region || "Regional";
          return (
            <div key={s.id} className="panel" style={{ padding: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
                <div><h3 style={{ fontSize: 15, marginBottom: 2 }}>{s.name}</h3><div className="mono" style={{ fontSize: 11, color: "var(--text-muted)" }}>{siteRegion} · {s.id}</div></div>
                <span className="status-pill status-safe">SAFE</span>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, margin: "18px 0 16px" }}>
                <Field label="Capacity" value={s.capacity.toLocaleString()} /><Field label="Available" value={s.available_capacity.toLocaleString()} />
                <Field label="Hazard risk" value={`${s.hazard_risk}/100`} /><Field label="Infrastructure" value={`${s.infrastructure_score}/100`} />
              </div>
              <div style={{ marginBottom: 16 }}><div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 5 }}><span style={{ color: "var(--text-muted)" }}>Occupancy</span><span className="mono">{occupancyPct}%</span></div><div style={{ height: 7, background: "var(--bg-inset)", borderRadius: 4, overflow: "hidden" }}><div style={{ width: `${occupancyPct}%`, height: "100%", background: occupancyPct > 80 ? "var(--risk-high)" : "var(--info)" }} /></div></div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>{s.facilities.map((f) => <span key={f} className="tag">{f}</span>)}</div>
            </div>
          );
        })}
      </div>
      {visibleSites.length === 0 && <div className="panel" style={{ padding: 24, marginTop: 16 }}>No safe sites are available for this region.</div>}
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return <div><div style={{ fontSize: 10.5, color: "var(--text-muted)" }}>{label}</div><div className="mono" style={{ fontSize: 14, fontWeight: 700 }}>{value}</div></div>;
}
