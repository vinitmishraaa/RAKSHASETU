import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import FilterBar from "../../components/common/FilterBar";
import RiskMap from "../../components/map/RiskMap";
import RegionDetailsPanel from "../../components/risk/RegionDetailsPanel";
import SelectedAreaPanel from "../../components/risk/SelectedAreaPanel";
import RegionHistoryPanel from "../../components/charts/RegionHistoryPanel";
import { api } from "../../services/api";
import type { Village, VillageDetail, RelocationPlan, SafeSite, Alert, LiveHazardFeed } from "../../types";

const COUNTRIES = ["India"];
const LEVELS = ["CRITICAL", "HIGH", "MODERATE", "LOW"];
const OFFICIALS = [
  { name: "Anushko Adhikary", email: "anushkoadhikary8918@gmail.com", phone: "8918552039" },
  { name: "Medha Mallick", email: "medha.mallick2020@gmail.com", phone: "9007564988" },
  { name: "Ayan Acharya", email: "ayanacharya06@gmail.com", phone: "9433172520" },
  { name: "Soumyadeep Palit", email: "soumyadeeppalit546@gmail.com", phone: "8697453997" },
  { name: "Prithiwi Barui", email: "prithiwibarui@gmail.com", phone: "9748069930" },
];
const SOURCE_EMAIL = "mishravinit923@gmail.com";
const n = (v: unknown) => typeof v === "number" && Number.isFinite(v) ? v : 0;
const fmt = (v: unknown) => typeof v === "number" && Number.isFinite(v) ? v.toLocaleString() : "—";

export default function Dashboard() {
  const navigate = useNavigate();
  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [villages, setVillages] = useState<Village[]>([]);
  const [safeSites, setSafeSites] = useState<SafeSite[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [liveFeed, setLiveFeed] = useState<LiveHazardFeed>({ updated_at: "", items: [], sources: [] });
  const [news, setNews] = useState<any[]>([]);
  const [country, setCountry] = useState("India");
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [level, setLevel] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<VillageDetail | null>(null);
  const [plan, setPlan] = useState<RelocationPlan | null>(null);
  const [loadingStates, setLoadingStates] = useState(true);
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    api.regions.states().then(rows => {
      if (!active) return;
      const names = rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
      setStates(names);
      const saved = localStorage.getItem("rakshasetu_region") || "";
      if (saved && names.includes(saved)) setState(saved);
    }).catch(e => active && setError(e.message)).finally(() => active && setLoadingStates(false));
    return () => { active = false; };
  }, []);

  useEffect(() => {
    let active = true;
    setDistrict("");
    setDistricts([]);
    setVillages([]);
    setSafeSites([]);
    setSelectedId(null);
    setDetail(null);
    setPlan(null);
    localStorage.removeItem("rakshasetu_district");
    if (!state) return;
    api.regions.districts(state).then(rows => {
      if (active) setDistricts(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b)));
    }).catch(e => active && setError(e.message));
    return () => { active = false; };
  }, [state]);

  useEffect(() => {
    let active = true;
    setError("");
    setLoadingData(!!state && !!district);
    if (!state || !district) {
      setVillages([]); setSafeSites([]); setAlerts([]); setNews([]); setLiveFeed({ updated_at: "", items: [], sources: [] });
      setLoadingData(false);
      return;
    }
    localStorage.setItem("rakshasetu_region", state);
    localStorage.setItem("rakshasetu_district", district);
    Promise.all([
      api.villages.list({ state, district }),
      api.safeSites.list({ state, district }),
      api.alerts.list(),
      api.live.hazards(state),
      api.live.news(`${district}, ${state}`),
    ]).then(([v, s, a, l, newsData]) => {
      if (!active) return;
      setVillages(v); setSafeSites(s); setAlerts(a); setLiveFeed(l); setNews(newsData.articles || []);
    }).catch(e => active && setError(e.message)).finally(() => active && setLoadingData(false));
    return () => { active = false; };
  }, [state, district]);

  const filtered = useMemo(() => villages.filter(v => !level || v.level === level), [villages, level]);
  const regionAlerts = useMemo(() => alerts.filter(a => filtered.some(v => v.id === a.village_id)), [alerts, filtered]);
  const priorityVillage = useMemo(() => [...filtered].sort((a, b) => n(b.risk_score) - n(a.risk_score))[0], [filtered]);
  const critical = filtered.filter(v => v.level === "CRITICAL").length;
  const high = filtered.filter(v => v.level === "HIGH").length;
  const totalPopulation = filtered.reduce((sum, v) => sum + n(v.population), 0);
  const regionLive = liveFeed.items || [];
  const latestLive = regionLive.slice(0, 4);

  async function handleSelect(v: Village) {
    setSelectedId(v.id);
    try {
      const [d, p] = await Promise.all([
        api.villages.get(v.id, { state, district }),
        api.relocation.plan(v.id),
      ]);
      setDetail(d); setPlan(p);
    } catch { setDetail(null); setPlan(null); }
  }

  function changeState(value: string) {
    setState(value);
    setDistrict("");
    localStorage.setItem("rakshasetu_region", value || "India");
    localStorage.removeItem("rakshasetu_district");
  }

  function changeCountry(value: string) {
    setCountry(value);
    setState(""); setDistrict("");
    setVillages([]); setSafeSites([]); setDistricts([]);
    localStorage.removeItem("rakshasetu_region"); localStorage.removeItem("rakshasetu_district");
  }

  function mailOfficer(o: typeof OFFICIALS[number], a?: Alert) {
    const subject = a ? `[RakshaSetu] ${a.level} alert · ${a.village_name}` : "[RakshaSetu] Regional disaster response alert";
    const body = a ? `RakshaSetu alert\n\nLocation: ${a.village_name}, ${a.district || ""}, ${a.state || ""}\nLevel: ${a.level}\nRisk score: ${a.risk_score}\nMessage: ${a.message}\n\nAdmin/source contact: ${SOURCE_EMAIL}` : `RakshaSetu response notification.\n\nSelected region: ${district}, ${state}\nAdmin/source contact: ${SOURCE_EMAIL}`;
    window.location.href = `mailto:${o.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  return (
    <div className="dashboard-page">
      <section className="dashboard-hero">
        <div><span className="eyebrow">COMMAND CENTER · INDIA</span><h1>RakshaSetu</h1><p>Live hazard intelligence, risk zones and response decisions using public open-data sources.</p></div>
        <div className="hero-live-badge"><i />LIVE DATA</div>
      </section>

      <FilterBar countries={COUNTRIES} country={country} setCountry={changeCountry} states={states} state={state} setState={changeState} districts={districts} district={district} setDistrict={setDistrict} level={level} setLevel={setLevel} />

      {error && <div className="panel" style={{ margin: "12px 0", padding: 16 }}><strong>Live data error</strong><p>{error}</p></div>}
      {loadingStates && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Loading real Indian states and Union Territories…</div>}
      {state && !district && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Select a district in <strong>{state}</strong> to load its real villages, mapped safe sites, hazards and analytics.</div>}
      {loadingData && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Loading live data for <strong>{district}, {state}</strong>…</div>}

      <section className="command-grid">
        <div className="map-stage">
          <RiskMap villages={filtered} safeSites={safeSites} liveHazards={state ? regionLive : []} selectedId={selectedId} onSelectVillage={handleSelect} region={state || "India"} district={district} />
          <div className="map-overlay-title"><strong>{district || state || "India"}</strong><span>{district ? `${filtered.length} mapped locations · ${critical} critical · ${high} high` : "Select state → district to load the operational view"}</span></div>
          <div className="map-legend"><Legend color="var(--risk-critical)" label="Critical" /><Legend color="var(--risk-high)" label="High" /><Legend color="var(--risk-moderate)" label="Moderate" /><Legend color="var(--risk-low)" label="Low" /><Legend color="#20c7ff" label="Safe" /><Legend color="#ff1744" label="Live" /></div>
        </div>
        <aside className="details-stage">
          <div className="panel-heading"><div><span className="eyebrow">SELECTED AREA</span><h2>{district || state || "India"}</h2></div><span className="status-dot">LIVE</span></div>
          {selectedId && detail ? <SelectedAreaPanel village={detail} onViewRelocation={() => navigate(`/relocation?village=${detail.id}`)} /> : state && district ? <RegionDetailsPanel region={state} district={district} villages={filtered} safeSites={safeSites} recommendedSite={safeSites[0] || null} /> : <div className="region-empty panel"><span className="eyebrow">DATA SCOPE</span><h3>India → State → District</h3><p>Choose a real state and district first. All downstream panels use that same scope.</p></div>}
        </aside>
      </section>

      {state && district && <section className="live-feed-panel panel"><div className="section-heading"><div><span className="eyebrow">REAL-TIME PUBLIC SIGNALS</span><h2>Live Hazard Feed · {district}</h2></div><button className="module-action" onClick={() => api.live.hazards(state).then(setLiveFeed).catch(e => setError(e.message))}>Refresh now</button></div><div className="live-kpi-row"><span><b>{regionLive.length}</b><small>live signals</small></span><span><b>{regionLive.filter(h => h.type.toLowerCase().includes("earthquake")).length}</b><small>earthquakes</small></span><span><b>{regionLive.filter(h => h.type.toLowerCase().includes("fire")).length}</b><small>fire hotspots</small></span><span><b>{regionLive.filter(h => h.severity === "CRITICAL").length}</b><small>critical</small></span><span><b>{regionLive.filter(h => h.severity === "HIGH").length}</b><small>high</small></span></div><div className="live-source-row">{liveFeed.sources.map(s => <span key={s.name} className={s.status === "live" ? "source-live" : "source-muted"}><i />{s.name} · {s.status}{s.count != null ? ` · ${s.count}` : ""}</span>)}<span className="live-updated">Updated {liveFeed.updated_at ? new Date(liveFeed.updated_at).toLocaleTimeString() : "—"}</span></div><div className="live-event-grid">{latestLive.map(h => <article className={`live-event-card live-event-${h.severity.toLowerCase()}`} key={h.id}><div><span>{h.type}</span><b>{h.severity}</b></div><strong>{h.title || "Live hazard observation"}</strong><p>{h.detail || "Public real-time observation"}</p><small>{h.lat.toFixed(3)}°, {h.lng.toFixed(3)}° · {h.source}</small></article>)}{!latestLive.length && <div className="live-empty">No live hazard signal currently inside the selected state.</div>}</div></section>}

      {state && district && <RegionHistoryPanel region={state} district={district} />}

      <section className="dashboard-modules"><div className="section-heading"><div><span className="eyebrow">RESPONSE OPERATIONS</span><h2>{district ? `${district} Operations` : state ? `${state} Operations` : "Select a state and district"}</h2></div></div>
        {state && district && <>
          <div className="dashboard-inline-section"><div className="inline-title"><h3>Relocation & Safe Sites</h3><span>{safeSites.length} mapped sites</span></div><div className="safe-site-strip">{safeSites.slice(0, 5).map(s => <article className="safe-site-card" key={s.id}><span className="safe-pill">MAPPED SITE</span><strong>{s.name}</strong><small>{s.district || district}, {s.region || state}</small><span>Capacity <b>{fmt(s.capacity)}</b></span><span>{s.facilities?.slice(0, 3).join(" · ") || "Facilities not verified"}</span></article>)}{!safeSites.length && <article className="safe-site-card"><strong>No mapped shelter found</strong><small>OpenStreetMap currently has no mapped shelter for this district.</small></article>}</div></div>
          {priorityVillage && <div className="dashboard-inline-section relocation-inline"><div className="inline-title"><h3>Priority Relocation</h3><span>{priorityVillage.level} risk</span></div><div className="priority-relocation"><div><strong>{priorityVillage.name}</strong><span>{priorityVillage.district || district}, {priorityVillage.state || state} · Population {fmt(priorityVillage.population)}</span></div><button className="btn" onClick={() => navigate(`/relocation?village=${priorityVillage.id}`)}>Plan relocation</button></div></div>}
          <div className="operation-card-grid">
            <article className="operation-card alert-card"><span className="eyebrow">LIVE ALERTS</span><h3>Alert Center</h3><strong>{regionAlerts.length} active signals</strong><p>{regionAlerts.filter(a => a.level === "CRITICAL").length} critical · {regionAlerts.filter(a => a.level === "HIGH").length} high</p>{regionAlerts.slice(0, 3).map(a => <div className="mini-row" key={`${a.village_id}-${a.level}`}><div><b>{a.level}</b><strong>{a.village_name}</strong><small>{a.district}, {a.state}</small></div><button className="contact-chip" onClick={() => mailOfficer(OFFICIALS[0], a)}>Notify</button></div>)}{!regionAlerts.length && <div className="mini-row"><span>No alert record matched this live village scope.</span></div>}<button className="btn secondary" onClick={() => navigate("/alerts")}>Open full alert desk</button></article>
            <article className="operation-card"><span className="eyebrow">CURRENT PUBLISHER SIGNALS</span><h3>{district} News</h3><strong>{news.length} results</strong><p>Publisher results for the selected district and state.</p>{news.slice(0, 3).map((a, i) => <a className="news-row" href={a.url} target="_blank" rel="noreferrer" key={`${a.url}-${i}`}>{a.title}</a>)}</article>
            <article className="operation-card"><span className="eyebrow">ANALYTICS</span><h3>{district} Risk Analytics</h3><strong>{filtered.length} locations</strong><p>Critical {critical} · High {high} · Population {fmt(totalPopulation)}</p><div className="analytics-stat-row"><span><small>Critical share</small><b>{filtered.length ? Math.round(critical * 100 / filtered.length) : 0}%</b></span><span><small>High-risk population</small><b>{fmt(filtered.filter(v => v.level === "CRITICAL" || v.level === "HIGH").reduce((sum, v) => sum + n(v.population), 0))}</b></span></div><div className="risk-meter"><i style={{ width: `${Math.min(100, critical * 100 / Math.max(1, filtered.length))}%` }} /></div></article>
            <article className="operation-card"><span className="eyebrow">AI DECISION SUPPORT</span><h3>RakshaSetu AI</h3><strong>Ask about {district}</strong><p>Use the selected live region context for risk, relocation and incidents.</p><button className="btn" onClick={() => navigate("/assistant")}>Ask AI</button></article>
          </div>
          <div className="dashboard-inline-section officer-inline"><div className="inline-title"><h3>Officer Alert Desk</h3><span>Direct email composer</span></div><div className="dashboard-officer-grid">{OFFICIALS.map(o => <article key={o.email}><div><strong>{o.name}</strong><small>{o.email}</small><small>{o.phone}</small></div><button className="contact-chip" onClick={() => mailOfficer(o)}>Email</button></article>)}</div><p className="data-note">Mapped shelter capacity/occupancy is shown as unknown unless the open source provides a verified value.</p></div>
        </>}
      </section>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) { return <span><i style={{ background: color }} />{label}</span>; }
