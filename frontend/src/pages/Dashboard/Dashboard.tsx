import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import FilterBar from "../../components/common/FilterBar";
import RiskMap from "../../components/map/RiskMap";
import RegionDetailsPanel from "../../components/risk/RegionDetailsPanel";
import SelectedAreaPanel from "../../components/risk/SelectedAreaPanel";
import RegionHistoryPanel from "../../components/charts/RegionHistoryPanel";
import { api } from "../../services/api";
import type { Village, VillageDetail, SafeSite, LiveHazardFeed } from "../../types";

const fmt = (v: unknown) => typeof v === "number" && Number.isFinite(v) ? v.toLocaleString() : "—";

export default function Dashboard() {
  const navigate = useNavigate();
  const restoring = useRef(true);
  const [states, setStates] = useState<string[]>([]), [cities, setCities] = useState<string[]>([]), [districts, setDistricts] = useState<string[]>([]);
  const [state, setState] = useState(""), [city, setCity] = useState(""), [district, setDistrict] = useState("");
  const [villages, setVillages] = useState<Village[]>([]), [safeSites, setSafeSites] = useState<SafeSite[]>([]);
  const [liveFeed, setLiveFeed] = useState<LiveHazardFeed>({ updated_at: "", items: [], sources: [] });
  const [news, setNews] = useState<any[]>([]), [selectedId, setSelectedId] = useState<string | null>(null), [detail, setDetail] = useState<VillageDetail | null>(null);
  const [loading, setLoading] = useState(false), [locationLoading, setLocationLoading] = useState(false), [error, setError] = useState("");

  useEffect(() => {
    api.regions.states().then(rows => {
      const names = rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
      setStates(names);
      const savedState = localStorage.getItem("rakshasetu_region") || "";
      const savedDistrict = localStorage.getItem("rakshasetu_district") || "";
      const savedCity = localStorage.getItem("rakshasetu_city") || "";
      if (savedState && names.includes(savedState)) { setDistrict(savedDistrict); setCity(savedCity); setState(savedState); }
      else restoring.current = false;
    }).catch(e => { restoring.current = false; setError(e.message); });
  }, []);

  useEffect(() => {
    let active = true;
    const restoringDistrict = restoring.current && !!district;
    setDistricts([]); setCities([]);
    if (!restoringDistrict) { setDistrict(""); setCity(""); }
    setVillages([]); setSafeSites([]); setSelectedId(null); setDetail(null);
    if (!state) { restoring.current = false; return; }
    setLocationLoading(true);
    api.regions.districts(state).then(rows => {
      if (!active) return;
      const names = rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
      setDistricts(names);
      const wanted = restoringDistrict ? district : localStorage.getItem("rakshasetu_district") || "";
      if (wanted && names.includes(wanted)) setDistrict(wanted); else if (!restoringDistrict) setDistrict("");
    }).catch(e => active && setError(e.message)).finally(() => { if (active) { setLocationLoading(false); restoring.current = false; } });
    return () => { active = false; };
  }, [state]);

  useEffect(() => {
    let active = true;
    const restoringCity = restoring.current && !!city;
    setCities([]); setVillages([]); setSafeSites([]); setSelectedId(null); setDetail(null);
    if (!state || !district) { if (!district) setCity(""); return; }
    setLocationLoading(true);
    api.regions.cities(state, district).then(rows => {
      if (!active) return;
      const names = rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
      setCities(names);
      const wanted = restoringCity ? city : localStorage.getItem("rakshasetu_city") || "";
      if (wanted && names.includes(wanted)) setCity(wanted); else if (!restoringCity) setCity("");
    }).catch(e => active && setError(e.message)).finally(() => active && setLocationLoading(false));
    return () => { active = false; };
  }, [state, district]);

  useEffect(() => {
    let active = true;
    setError("");
    if (!state || !district || !city) { setVillages([]); setSafeSites([]); setLiveFeed({ updated_at: "", items: [], sources: [] }); setNews([]); setLoading(false); return; }
    setLoading(true);
    localStorage.setItem("rakshasetu_region", state); localStorage.setItem("rakshasetu_district", district); localStorage.setItem("rakshasetu_city", city);
    Promise.all([api.villages.list({ state, district, city }), api.safeSites.list({ state, district, city }), api.live.hazards(state, district), api.live.news(state, district)])
      .then(([v, s, live, n]) => { if (!active) return; setVillages(v); setSafeSites(s); setLiveFeed(live); setNews(n.articles || []); })
      .catch(e => active && setError(e.message)).finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [state, district, city]);

  const critical = villages.filter(v => v.level === "CRITICAL").length;
  const high = villages.filter(v => v.level === "HIGH").length;
  const knownPopulation = villages.reduce((sum, v) => sum + (v.population ?? 0), 0);
  const priority = useMemo(() => [...villages].sort((a, b) => b.risk_score - a.risk_score)[0], [villages]);
  const liveItems = liveFeed.items || [];
  const mapHazards = liveItems.filter(h => h.lat != null && h.lng != null);

  async function selectVillage(v: Village) { setSelectedId(v.id); try { setDetail(await api.villages.get(v.id, { state, district, city })); } catch (e) { setError(e instanceof Error ? e.message : "Could not load settlement details"); } }
  function clearScope() { setState(""); setDistrict(""); setCity(""); setCities([]); setDistricts([]); setVillages([]); setSafeSites([]); setLiveFeed({ updated_at: "", items: [], sources: [] }); setNews([]); setSelectedId(null); setDetail(null); localStorage.removeItem("rakshasetu_region"); localStorage.removeItem("rakshasetu_district"); localStorage.removeItem("rakshasetu_city"); }

  return <div className="dashboard-page">
    <section className="dashboard-hero"><div><span className="eyebrow">COMMAND CENTER · INDIA</span><h1>RakshaSetu</h1><p>Live hazard intelligence, mapped risk zones and response planning from public open-data sources.</p></div><div className="hero-live-badge"><i />LIVE DATA</div></section>
    <FilterBar states={states} state={state} setState={setState} cities={cities} city={city} setCity={setCity} districts={districts} district={district} setDistrict={setDistrict} loading={locationLoading} />
    {error && <div className="panel" style={{ margin: "12px 0", padding: 16 }}><strong>Live data error</strong><p>{error}</p><button className="btn secondary" onClick={() => window.location.reload()}>Retry</button></div>}
    {!state && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Select a State / Union Territory first.</div>}
    {state && !district && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Select a District from <strong>{state}</strong>. Only that state's districts are shown.</div>}
    {state && district && !city && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Select a City / Town from <strong>{district}, {state}</strong>. Only this district's mapped cities and towns are shown.</div>}
    {loading && <div className="panel" style={{ margin: "12px 0", padding: 16 }}>Fetching live data for <strong>{city}, {district}, {state}</strong>…</div>}
    <section className="command-grid"><div className="map-stage"><RiskMap villages={villages} safeSites={safeSites} liveHazards={mapHazards} selectedId={selectedId} onSelectVillage={selectVillage} region={state || "India"} district={district} /><div className="map-overlay-title"><strong>{city || district || state || "India"}</strong><span>{city ? `${villages.length} mapped locations · ${critical} critical · ${high} high` : "Choose State → District → City / Town"}</span></div><div className="map-legend"><Legend color="var(--risk-critical)" label="Critical" /><Legend color="var(--risk-high)" label="High" /><Legend color="var(--risk-moderate)" label="Moderate" /><Legend color="var(--risk-low)" label="Low" /><Legend color="#20c7ff" label="Mapped safe site" /><Legend color="#ff1744" label="Live signal" /></div></div>
      <aside className="details-stage"><div className="panel-heading"><div><span className="eyebrow">SELECTED AREA</span><h2>{city || district || state || "India"}</h2></div><span className="status-dot">LIVE</span></div>{selectedId && detail ? <SelectedAreaPanel village={detail} onViewRelocation={() => navigate(`/relocation?village=${detail.id}`)} /> : city ? <RegionDetailsPanel region={state} district={district} villages={villages} safeSites={safeSites} recommendedSite={safeSites[0] || null} /> : <div className="region-empty panel"><span className="eyebrow">DATA SCOPE</span><h3>State → District → City / Town</h3><p>Complete the three location steps to load the operational dashboard.</p></div>}</aside>
    </section>
    {city && <><section className="live-feed-panel panel"><div className="section-heading"><div><span className="eyebrow">REAL-TIME PUBLIC SIGNALS</span><h2>Live Hazard Feed · {district}</h2></div><button className="module-action" onClick={() => api.live.hazards(state, district).then(setLiveFeed).catch(e => setError(e.message))}>Refresh now</button></div><div className="live-kpi-row"><span><b>{liveItems.length}</b><small>live signals</small></span><span><b>{liveItems.filter(h => h.type.toLowerCase().includes("earthquake")).length}</b><small>earthquakes</small></span><span><b>{liveItems.filter(h => h.type.toLowerCase().includes("fire")).length}</b><small>fire hotspots</small></span><span><b>{liveItems.filter(h => h.severity === "CRITICAL").length}</b><small>critical</small></span><span><b>{liveItems.filter(h => h.severity === "HIGH").length}</b><small>high</small></span></div><div className="live-source-row">{liveFeed.sources.map(s => <span key={s.name} className={s.status === "live" ? "source-live" : "source-muted"}><i />{s.name} · {s.status}{s.count != null ? ` · ${s.count}` : ""}</span>)}<span className="live-updated">Updated {liveFeed.updated_at ? new Date(liveFeed.updated_at).toLocaleTimeString() : "—"}</span></div><div className="live-event-grid">{liveItems.slice(0, 6).map(h => <article className={`live-event-card live-event-${h.severity.toLowerCase()}`} key={h.id}><div><span>{h.type}</span><b>{h.severity}</b></div><strong>{h.title || "Live hazard observation"}</strong><p>{h.detail || "Public real-time observation"}</p><small>{h.lat != null && h.lng != null ? `${h.lat.toFixed(3)}°, ${h.lng.toFixed(3)}° · ` : "Location from source feed · "}{h.source}</small></article>)}{!liveItems.length && <div className="live-empty">No current public hazard signal was returned for this district.</div>}</div></section>
      <section className="dashboard-modules"><div className="section-heading"><div><span className="eyebrow">RESPONSE OPERATIONS</span><h2>{city} Operations</h2></div></div><div className="dashboard-inline-section"><div className="inline-title"><h3>Mapped Safe Sites</h3><span>{safeSites.length} OpenStreetMap records</span></div><div className="safe-site-strip">{safeSites.slice(0, 5).map(s => <article className="safe-site-card" key={s.id}><span className="safe-pill">MAPPED SITE</span><strong>{s.name}</strong><small>{s.district || district}, {s.region || state}</small><span>Capacity <b>{fmt(s.capacity)}</b></span><span>{s.facilities?.slice(0, 3).join(" · ") || "Facilities not published"}</span></article>)}{!safeSites.length && <article className="safe-site-card"><strong>No mapped shelter returned</strong><small>OpenStreetMap has no matching shelter record in this district at the moment.</small></article>}</div></div>{priority && <div className="dashboard-inline-section relocation-inline"><div className="inline-title"><h3>Priority Relocation</h3><span>{priority.level} live indicator</span></div><div className="priority-relocation"><div><strong>{priority.name}</strong><span>{priority.district || district}, {priority.state || state} · Published population {fmt(priority.population)}</span></div><button className="btn" onClick={() => navigate(`/relocation?village=${priority.id}`)}>Build relocation plan</button></div></div>}<div className="operation-card-grid"><article className="operation-card alert-card"><span className="eyebrow">LIVE ALERTS</span><h3>Alert Center</h3><strong>{liveItems.length} source signals</strong><p>{liveItems.filter(h => h.severity === "CRITICAL").length} critical · {liveItems.filter(h => h.severity === "HIGH").length} high</p>{liveItems.slice(0, 3).map(h => <div className="mini-row" key={h.id}><div><b>{h.severity}</b><strong>{h.title || h.type}</strong><small>{h.source}</small></div></div>)}{!liveItems.length && <div className="mini-row"><span>No live alert signal returned.</span></div>}</article><article className="operation-card"><span className="eyebrow">CURRENT PUBLISHER SIGNALS</span><h3>{district} News</h3><strong>{news.length} results</strong><p>Current publisher results for the selected district.</p>{news.slice(0, 4).map((a, i) => <a className="news-row" href={a.url} target="_blank" rel="noreferrer" key={`${a.url}-${i}`}>{a.title}</a>)}</article><article className="operation-card"><span className="eyebrow">RISK SNAPSHOT</span><h3>Current live indicator</h3><div className="mini-stat-grid"><span><small>Mapped locations</small><b>{villages.length}</b></span><span><small>Critical</small><b>{critical}</b></span><span><small>High</small><b>{high}</b></span><span><small>Known population</small><b>{knownPopulation ? knownPopulation.toLocaleString() : "—"}</b></span></div><p className="data-note">Risk is an operational indicator derived from current public observations; it is not an official government hazard rating.</p></article><article className="operation-card"><span className="eyebrow">GUIDED RESPONSE</span><h3>Relocation workflow</h3><p>Select a danger location on the map, open its relocation plan, choose a mapped safe site and then generate a live road route.</p><button className="btn" disabled={!priority} onClick={() => priority && navigate(`/relocation?village=${priority.id}`)}>Open guided relocation</button></article></div></section><RegionHistoryPanel region={state} district={district} /><div className="panel" style={{ marginTop: 16, padding: 14 }}><button className="btn secondary" onClick={clearScope}>Reset location</button></div></>}
  </div>;
}
function Legend({ color, label }: { color: string; label: string }) { return <span><i style={{ background: color }} />{label}</span>; }
