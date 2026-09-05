import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import FilterBar from "../../components/common/FilterBar";
import RiskMap from "../../components/map/RiskMap";
import RegionDetailsPanel from "../../components/risk/RegionDetailsPanel";
import SelectedAreaPanel from "../../components/risk/SelectedAreaPanel";
import PopulationProfile from "../../components/villages/PopulationProfile";
import HazardBars from "../../components/risk/HazardBars";
import HistoryTimeline from "../../components/charts/HistoryTimeline";
import RainfallTrendChart from "../../components/charts/RainfallTrendChart";
import RelocationBox from "../../components/relocation/RelocationBox";
import { api } from "../../services/api";
import type { Village, VillageDetail, RelocationPlan, SafeSite } from "../../types";

const COUNTRIES = ["India", "Nepal", "China"];
const INDIA_STATES = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry"];
const NEPAL_PROVINCES = ["Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"];
const CHINA_PROVINCES = ["Anhui", "Beijing", "Chongqing", "Fujian", "Gansu", "Guangdong", "Guangxi", "Guizhou", "Hainan", "Hebei", "Heilongjiang", "Henan", "Hubei", "Hunan", "Inner Mongolia", "Jiangsu", "Jiangxi", "Jilin", "Liaoning", "Ningxia", "Qinghai", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan", "Tianjin", "Tibet", "Xinjiang", "Yunnan", "Zhejiang"];
const DATA_STATE_TO_COUNTRY: Record<string, string> = { Nepal: "Nepal" };
const QUICK_MODULES = [
  { title: "Relocation Center", description: "Capacity-aware evacuation sites, allocations and route planning", path: "/relocation" },
  { title: "Alerts", description: "Critical warnings, risk escalation and response status", path: "/alerts" },
  { title: "Analytics", description: "Historical comparison, trends and regional risk charts", path: "/analytics" },
  { title: "Safe Sites", description: "Inspect shelters, capacity, facilities and suitability", path: "/safe-sites" },
  { title: "Past Incidents", description: "Review floods, rainfall, cyclones, droughts and earthquakes", path: "/analytics" },
  { title: "AI Decision Support", description: "Ask RakshaSetu for grounded response recommendations", path: "/assistant" },
];

export default function Dashboard() {
  const navigate = useNavigate(); const [villages, setVillages] = useState<Village[]>([]); const [safeSites, setSafeSites] = useState<SafeSite[]>([]);
  const [country, setCountry] = useState(""); const [state, setStateValue] = useState(""); const [district, setDistrict] = useState(""); const [level, setLevel] = useState(""); const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<VillageDetail | null>(null); const [plan, setPlan] = useState<RelocationPlan | null>(null); const [regionBestSite, setRegionBestSite] = useState<any>(null); const [loading, setLoading] = useState(true);

  useEffect(() => { Promise.all([api.villages.list(), api.safeSites.list()]).then(([v, s]) => { setVillages(v); setSafeSites(s); }).finally(() => setLoading(false)); }, []);

  const states = useMemo(() => country === "India" ? INDIA_STATES : country === "Nepal" ? NEPAL_PROVINCES : country === "China" ? CHINA_PROVINCES : [], [country]);
  const dataRegion = useMemo(() => {
    if (!state) return "";
    if (DATA_STATE_TO_COUNTRY[state]) return state;
    return state;
  }, [state]);
  const districts = useMemo(() => Array.from(new Set((dataRegion ? villages.filter((v) => v.state === dataRegion) : []).map((v) => v.district))).sort(), [villages, dataRegion]);
  const filtered = useMemo(() => villages.filter((v) => (!dataRegion || v.state === dataRegion) && (!district || v.district === district) && (!level || v.level === level)), [villages, dataRegion, district, level]);
  const mapRegion = state || country;
  const regionSites = useMemo(() => safeSites.filter((s) => !dataRegion || !s.region || s.region === dataRegion), [safeSites, dataRegion]);
  const priorityVillage = useMemo(() => [...filtered].sort((a, b) => b.risk_score - a.risk_score)[0], [filtered]);

  useEffect(() => { let cancelled = false; setRegionBestSite(null); if (!priorityVillage) return; api.safeSites.rankFor(priorityVillage.id).then((sites) => { if (!cancelled) setRegionBestSite(sites[0] || null); }).catch(() => { if (!cancelled) setRegionBestSite(null); }); return () => { cancelled = true; }; }, [priorityVillage?.id]);
  useEffect(() => { if (district && !districts.includes(district)) setDistrict(""); }, [district, districts]);

  async function handleSelect(v: Village) { setSelectedId(v.id); try { const [d, p] = await Promise.all([api.villages.get(v.id), api.relocation.plan(v.id)]); setDetail(d); setPlan(p); } catch { setDetail(null); setPlan(null); } }
  function changeCountry(value: string) { setCountry(value); setStateValue(""); setDistrict(""); setSelectedId(null); setDetail(null); setPlan(null); }
  function changeState(value: string) { setStateValue(value); setDistrict(""); setSelectedId(null); setDetail(null); setPlan(null); }

  return <div className="dashboard-page">
    <section className="dashboard-hero"><div><span className="eyebrow">DISASTER RESPONSE COMMAND CENTER</span><h1>RakshaSetu</h1><p>One geographic workflow: Country → State / Province → District → response intelligence.</p></div></section>
    <FilterBar countries={COUNTRIES} country={country} setCountry={changeCountry} states={states} state={state} setState={changeState} districts={districts} district={district} setDistrict={setDistrict} level={level} setLevel={setLevel} />
    <section className="command-grid">
      <div className="map-stage">{loading ? <div className="map-loading">Loading regional intelligence…</div> : <RiskMap villages={filtered} safeSites={regionSites} selectedId={selectedId} onSelectVillage={handleSelect} region={mapRegion} district={district} />}<div className="map-overlay-title"><strong>{district || state || country || "India · Nepal · China"}</strong><span>{filtered.length ? `${filtered.length} monitored zones` : "Select a supported state / district for detailed zones"}</span></div><div className="map-legend"><Legend color="var(--risk-critical)" label="Critical" /><Legend color="var(--risk-high)" label="High" /><Legend color="var(--risk-moderate)" label="Moderate" /><Legend color="var(--risk-low)" label="Low" /><Legend color="var(--safe)" label="Safe Site" /></div><div className="map-help">Scroll / buttons to zoom · drag to explore · click a zone</div></div>
      <aside className="details-stage"><div className="panel-heading"><div><span className="eyebrow">LIVE SELECTION</span><h2>{district || state || country || "Area Details"}</h2></div><span className="status-dot">LIVE</span></div>{state && dataRegion && filtered.length && !selectedId ? <RegionDetailsPanel region={dataRegion} district={district} villages={filtered} safeSites={regionSites} recommendedSite={regionBestSite} /> : selectedId ? <SelectedAreaPanel village={detail} onViewRelocation={() => detail && navigate(`/relocation?village=${detail.id}`)} /> : <div className="region-empty panel"><span className="eyebrow">READY</span><h3>{state ? `${state} map ready` : country ? `${country} scope ready` : "Choose a country first"}</h3><p>{filtered.length ? "Select a zone on the map to open detailed demographics and relocation logic." : "Detailed prototype risk zones are currently populated for the eastern response pilot; the geographic hierarchy is ready for full national GIS data."}</p></div>}</aside>
    </section>
    <section className="dashboard-modules"><div className="section-heading"><div><span className="eyebrow">RESPONSE WORKSPACE</span><h2>{state ? `${district || state} Operations` : country ? `${country} Operations` : "Operational Modules"}</h2></div><span>{filtered.length} zones in scope</span></div><div className="module-stack">{QUICK_MODULES.map((module) => <button key={module.title} className="module-card" onClick={() => navigate(module.path)}><span className="module-kicker">RAKSHASETU · {state || country || "GLOBAL"}</span><strong>{module.title}</strong><span>{module.description}</span><b>Open module →</b></button>)}</div></section>
    {detail && <section className="detail-workspace"><div className="section-heading"><div><span className="eyebrow">SELECTED ZONE INTELLIGENCE</span><h2>{detail.name}</h2></div><span>{detail.district}, {detail.state}</span></div><div className="detail-grid"><PopulationProfile village={detail} /><HazardBars village={detail} /><RainfallTrendChart village={detail} /><HistoryTimeline village={detail} />{plan && <RelocationBox plan={plan} onViewRoute={() => navigate(`/relocation?village=${detail.id}`)} />}</div></section>}
    <button className="floating-assistant" onClick={() => navigate("/assistant")} aria-label="Open RakshaSetu AI Assistant"><span className="assistant-orb">AI</span><span><strong>RakshaSetu</strong><small>AI Assistant</small></span></button>
  </div>;
}
function Legend({ color, label }: { color: string; label: string }) { return <span className="legend-item"><i style={{ background: color }} />{label}</span>; }
