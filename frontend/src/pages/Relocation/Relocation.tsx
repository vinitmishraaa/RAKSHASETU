import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import RiskMap from "../../components/map/RiskMap";
import RelocationBox from "../../components/relocation/RelocationBox";
import { api } from "../../services/api";
import type { Village, SafeSite, RelocationPlan } from "../../types";
import "./relocation.css";

export default function Relocation() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [villages, setVillages] = useState<Village[]>([]); const [sites, setSites] = useState<SafeSite[]>([]);
  const [villageId, setVillageId] = useState(searchParams.get("village") || ""); const [plan, setPlan] = useState<RelocationPlan | null>(null);
  const [route, setRoute] = useState<any>(null); const [routeLoading, setRouteLoading] = useState(false); const [error, setError] = useState("");
  useEffect(() => { Promise.all([api.villages.list(), api.safeSites.list()]).then(([v, s]) => { setVillages(v); setSites(s); if (!villageId && v.length) setVillageId(v[0].id); }).catch(() => setError("Could not load relocation data.")); }, []);
  useEffect(() => { if (!villageId) return; setSearchParams({ village: villageId }); setRoute(null); setError(""); api.relocation.plan(villageId).then(setPlan).catch(() => setError("Could not generate a relocation recommendation.")); }, [villageId, setSearchParams]);
  const selectedVillage = villages.find((v) => v.id === villageId);
  const regionalSites = selectedVillage ? sites.filter((s) => !s.region || s.region === selectedVillage.state) : sites;
  async function handleViewRoute(siteId: string) { if (!villageId) return; setRouteLoading(true); setError(""); try { setRoute(await api.relocation.route(villageId, siteId)); } catch { setError("Route could not be generated. Try another safe site."); } finally { setRouteLoading(false); } }
  return <div className="relocation-command">
    <div className="relocation-map"><RiskMap villages={selectedVillage ? [selectedVillage] : villages} safeSites={regionalSites} selectedId={villageId} route={route?.path} center={selectedVillage ? [selectedVillage.lat, selectedVillage.lng] : undefined} /></div>
    <div className="relocation-panel">
      <div className="panel-heading"><div><span className="eyebrow">EVACUATION COMMAND</span><h2>Safe relocation</h2></div><span className="status-dot">LIVE</span></div>
      <label className="relocation-select"><span>SELECT ZONE</span><select value={villageId} onChange={(e) => setVillageId(e.target.value)}>{villages.map((v) => <option key={v.id} value={v.id}>{v.name} · {v.district} · {v.level}</option>)}</select></label>
      {selectedVillage && <div className="relocation-context"><b>{selectedVillage.district}, {selectedVillage.state}</b><span>Population {selectedVillage.population.toLocaleString()} · Risk {selectedVillage.risk_score}</span></div>}
      {error && <div className="relocation-error">{error}</div>}
      {plan && <RelocationBox plan={plan} onViewRoute={handleViewRoute} />}
      {routeLoading && <div className="panel route-status">Generating route…</div>}
      {route && <div className="panel route-card"><span className="eyebrow">ROUTE GENERATED</span><h3>{route.from.name} → {route.to.name}</h3><div className="route-metrics"><span><b>{route.distance_km} km</b><small>distance</small></span><span><b>SAFE SITE</b><small>destination</small></span></div><p>{route.note}</p></div>}
      {plan && plan.ranked_sites.length > 0 && <div className="panel ranking-panel"><h4>SITE SUITABILITY · BEST FIRST</h4>{plan.ranked_sites.map((s, i) => <div className="ranking-row" key={s.site_id}><div><strong>{i + 1}. {s.site_name}</strong><small>{s.distance_km} km · {s.road_access} access · {s.available_capacity.toLocaleString()} free</small></div><b>{s.suitability}/100</b></div>)}</div>}
    </div>
  </div>;
}
