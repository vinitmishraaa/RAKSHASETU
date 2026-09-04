import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import FilterBar from "../../components/common/FilterBar";
import RiskMap from "../../components/map/RiskMap";
import SelectedAreaPanel from "../../components/risk/SelectedAreaPanel";
import PopulationProfile from "../../components/villages/PopulationProfile";
import HazardBars from "../../components/risk/HazardBars";
import HistoryTimeline from "../../components/charts/HistoryTimeline";
import RainfallTrendChart from "../../components/charts/RainfallTrendChart";
import RelocationBox from "../../components/relocation/RelocationBox";
import { api } from "../../services/api";
import type { Village, VillageDetail, RelocationPlan, SafeSite } from "../../types";

const TARGET_REGIONS = ["West Bengal", "Bihar", "Odisha", "Jharkhand", "Sikkim", "Nepal"];

const QUICK_MODULES = [
  { title: "Risk Analysis", description: "Live hazard, exposure and vulnerability assessment", path: "/" },
  { title: "Safe Sites", description: "Find and inspect nearby evacuation locations", path: "/safe-sites" },
  { title: "Relocation", description: "Plan capacity-aware evacuation and routes", path: "/relocation" },
  { title: "Past Incidents", description: "Review regional disaster history and lessons", path: "/analytics" },
  { title: "Alerts", description: "Review critical warnings and response status", path: "/alerts" },
  { title: "Analytics", description: "Compare current conditions with historical events", path: "/analytics" },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const [villages, setVillages] = useState<Village[]>([]);
  const [safeSites, setSafeSites] = useState<SafeSite[]>([]);
  const [region, setRegion] = useState("");
  const [district, setDistrict] = useState("");
  const [level, setLevel] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<VillageDetail | null>(null);
  const [plan, setPlan] = useState<RelocationPlan | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.villages.list(), api.safeSites.list()])
      .then(([villageData, siteData]) => {
        setVillages(villageData);
        setSafeSites(siteData);
      })
      .finally(() => setLoading(false));
  }, []);

  const regions = useMemo(() => {
    const available = Array.from(new Set(villages.map((v) => v.state))).filter(Boolean);
    return Array.from(new Set([...TARGET_REGIONS, ...available]));
  }, [villages]);

  const filtered = useMemo(() => villages.filter((v) => {
    if (region && v.state !== region) return false;
    if (district && v.district !== district) return false;
    if (level && v.level !== level) return false;
    return true;
  }), [villages, region, district, level]);

  const districts = useMemo(() => {
    const source = region ? villages.filter((v) => v.state === region) : villages;
    return Array.from(new Set(source.map((v) => v.district))).sort();
  }, [villages, region]);

  useEffect(() => {
    if (district && !districts.includes(district)) setDistrict("");
  }, [district, districts]);

  async function handleSelect(v: Village) {
    setSelectedId(v.id);
    const [d, p] = await Promise.all([api.villages.get(v.id), api.relocation.plan(v.id)]);
    setDetail(d);
    setPlan(p);
  }

  function changeRegion(value: string) {
    setRegion(value);
    setDistrict("");
    setSelectedId(null);
    setDetail(null);
    setPlan(null);
  }

  return (
    <div className="dashboard-page">
      <section className="dashboard-hero">
        <div>
          <span className="eyebrow">DISASTER RESPONSE COMMAND CENTER</span>
          <h1>RakshaSetu</h1>
          <p>Regional risk intelligence, safe-site discovery and coordinated evacuation planning.</p>
        </div>
        <div className="region-pills">
          {regions.map((item) => (
            <button
              key={item}
              className={`region-pill ${region === item ? "active" : ""}`}
              onClick={() => changeRegion(region === item ? "" : item)}
            >
              {item}
            </button>
          ))}
        </div>
      </section>

      <FilterBar
        regions={regions}
        region={region}
        setRegion={changeRegion}
        districts={districts}
        district={district}
        setDistrict={setDistrict}
        level={level}
        setLevel={setLevel}
      />

      <section className="command-grid">
        <div className="map-stage">
          {loading ? (
            <div className="map-loading">Loading regional intelligence…</div>
          ) : (
            <RiskMap villages={filtered} safeSites={safeSites} selectedId={selectedId} onSelectVillage={handleSelect} />
          )}
          <div className="map-overlay-title">
            <strong>{region || "Eastern Response Region"}</strong>
            <span>{filtered.length} monitored locations</span>
          </div>
          <div className="map-legend">
            <Legend color="var(--risk-critical)" label="Critical" />
            <Legend color="var(--risk-high)" label="High" />
            <Legend color="var(--risk-moderate)" label="Moderate" />
            <Legend color="var(--risk-low)" label="Low" />
            <Legend color="var(--safe)" label="Safe Site" />
          </div>
        </div>

        <aside className="details-stage">
          <div className="panel-heading">
            <div><span className="eyebrow">LIVE SELECTION</span><h2>Area Details</h2></div>
            <span className="status-dot">LIVE</span>
          </div>
          <SelectedAreaPanel
            village={detail}
            onViewRelocation={() => detail && navigate(`/relocation?village=${detail.id}`)}
          />
        </aside>
      </section>

      <section className="dashboard-modules">
        <div className="section-heading">
          <div><span className="eyebrow">RESPONSE WORKSPACE</span><h2>Operational Modules</h2></div>
          <span>{region || "All target regions"}</span>
        </div>
        <div className="module-grid">
          {QUICK_MODULES.map((module) => (
            <button key={module.title} className="module-card" onClick={() => navigate(module.path)}>
              <span className="module-kicker">RAKSHASETU</span>
              <strong>{module.title}</strong>
              <span>{module.description}</span>
              <b>Open module →</b>
            </button>
          ))}
        </div>
      </section>

      {detail && (
        <section className="detail-workspace">
          <div className="section-heading">
            <div><span className="eyebrow">SELECTED LOCATION</span><h2>{detail.name}</h2></div>
            <span>{detail.district}, {detail.state}</span>
          </div>
          <div className="detail-grid">
            <PopulationProfile village={detail} />
            <HazardBars village={detail} />
            <RainfallTrendChart village={detail} />
            <HistoryTimeline village={detail} />
            {plan && <RelocationBox plan={plan} onViewRoute={() => navigate(`/relocation?village=${detail.id}`)} />}
          </div>
        </section>
      )}

      <button className="floating-assistant" onClick={() => navigate("/assistant")} aria-label="Open RakshaSetu AI Assistant">
        <span className="assistant-orb">AI</span>
        <span><strong>RakshaSetu</strong><small>AI Assistant</small></span>
      </button>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return <span className="legend-item"><i style={{ background: color }} />{label}</span>;
}
