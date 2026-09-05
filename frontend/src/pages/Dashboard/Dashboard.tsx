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
import RegionHistoryPanel from "../../components/charts/RegionHistoryPanel";
import RelocationBox from "../../components/relocation/RelocationBox";
import { api } from "../../services/api";
import type { Village, VillageDetail, RelocationPlan, SafeSite } from "../../types";

const COUNTRIES=["India","Nepal","China"];
const INDIA_STATES=["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Delhi","Jammu and Kashmir","Ladakh","Puducherry"];
const NEPAL_PROVINCES=["Koshi","Madhesh","Bagmati","Gandaki","Lumbini","Karnali","Sudurpashchim"];
const CHINA_PROVINCES=["Anhui","Beijing","Chongqing","Fujian","Gansu","Guangdong","Guangxi","Guizhou","Hainan","Hebei","Heilongjiang","Henan","Hubei","Hunan","Inner Mongolia","Jiangsu","Jiangxi","Jilin","Liaoning","Ningxia","Qinghai","Shaanxi","Shandong","Shanghai","Shanxi","Sichuan","Tianjin","Tibet","Xinjiang","Yunnan","Zhejiang"];

export default function Dashboard(){
 const navigate=useNavigate(); const [villages,setVillages]=useState<Village[]>([]); const [safeSites,setSafeSites]=useState<SafeSite[]>([]);
 const [country,setCountry]=useState(""); const [state,setStateValue]=useState(""); const [district,setDistrict]=useState(""); const [level,setLevel]=useState(""); const [selectedId,setSelectedId]=useState<string|null>(null); const [detail,setDetail]=useState<VillageDetail|null>(null); const [plan,setPlan]=useState<RelocationPlan|null>(null); const [regionBestSite,setRegionBestSite]=useState<any>(null); const [loading,setLoading]=useState(true);
 useEffect(()=>{Promise.all([api.villages.list(),api.safeSites.list()]).then(([v,s])=>{setVillages(v);setSafeSites(s)}).finally(()=>setLoading(false))},[]);
 const states=useMemo(()=>country==="India"?INDIA_STATES:country==="Nepal"?NEPAL_PROVINCES:country==="China"?CHINA_PROVINCES:[],[country]);
 const dataRegion=useMemo(()=>country==="India"?state:(state&&villages.some(v=>v.state===state)?state:country),[country,state,villages]);
 const districts=useMemo(()=>Array.from(new Set(villages.filter(v=>!state||v.state===dataRegion).map(v=>v.district))).sort(),[villages,state,dataRegion]);
 const filtered=useMemo(()=>villages.filter(v=>(!dataRegion||v.state===dataRegion)&&(!district||v.district===district)&&(!level||v.level===level)),[villages,dataRegion,district,level]);
 const mapRegion=state||country; const regionSites=useMemo(()=>safeSites.filter(s=>!dataRegion||!s.region||s.region===dataRegion),[safeSites,dataRegion]); const priorityVillage=useMemo(()=>[...filtered].sort((a,b)=>b.risk_score-a.risk_score)[0],[filtered]);
 useEffect(()=>{let c=false;setRegionBestSite(null);if(priorityVillage)api.safeSites.rankFor(priorityVillage.id).then(x=>{if(!c)setRegionBestSite(x[0]||null)}).catch(()=>{});return()=>{c=true}},[priorityVillage?.id]);
 useEffect(()=>{if(district&&!districts.includes(district))setDistrict("")},[district,districts]);
 async function handleSelect(v:Village){setSelectedId(v.id);try{const[d,p]=await Promise.all([api.villages.get(v.id),api.relocation.plan(v.id)]);setDetail(d);setPlan(p)}catch{setDetail(null);setPlan(null)}}
 function changeCountry(v:string){setCountry(v);setStateValue("");setDistrict("");setSelectedId(null);setDetail(null);setPlan(null)} function changeState(v:string){setStateValue(v);setDistrict("");setSelectedId(null);setDetail(null);setPlan(null)}
 const topSites=regionSites.slice(0,5);
 return <div className="dashboard-page">
  <section className="dashboard-hero"><div><span className="eyebrow">DISASTER RESPONSE</span><h1>RakshaSetu</h1><p>AI-powered hazard, vulnerability & relocation intelligence.</p></div></section>
  <FilterBar countries={COUNTRIES} country={country} setCountry={changeCountry} states={states} state={state} setState={changeState} districts={districts} district={district} setDistrict={setDistrict} level={level} setLevel={setLevel}/>
  <section className="command-grid"><div className="map-stage">{loading?<div className="map-loading">Loading regional intelligence…</div>:<RiskMap villages={filtered} safeSites={regionSites} selectedId={selectedId} onSelectVillage={handleSelect} region={mapRegion} district={district}/>}<div className="map-overlay-title"><strong>{district||state||country||"Regional risk map"}</strong><span>{filtered.length?`${filtered.length} monitored zones`:country?`${country} map · live data layer pending`:"Select a country, state or district"}</span></div><div className="map-legend"><Legend color="var(--risk-critical)" label="Critical"/><Legend color="var(--risk-high)" label="High"/><Legend color="var(--risk-moderate)" label="Moderate"/><Legend color="var(--risk-low)" label="Low"/><Legend color="var(--safe)" label="Safe"/></div></div>
   <aside className="details-stage"><div className="panel-heading"><div><span className="eyebrow">SELECTED AREA</span><h2>{district||state||country||"Area Details"}</h2></div><span className="status-dot">LIVE</span></div>{state&&filtered.length&&!selectedId?<RegionDetailsPanel region={dataRegion} district={district} villages={filtered} safeSites={regionSites} recommendedSite={regionBestSite}/>:selectedId?<SelectedAreaPanel village={detail} onViewRelocation={()=>detail&&navigate(`/relocation?village=${detail.id}`)}/>:<div className="region-empty panel"><span className="eyebrow">GEOGRAPHIC SCOPE</span><h3>{country?`${country} selected`:"Select a country to begin"}</h3><p>{country?"Choose a state / province and district to narrow the operational view.":"India, Nepal and China are available in the geographic selector."}</p></div>}</aside>
  </section>
  {state&&<RegionHistoryPanel region={dataRegion} district={district}/>} 
  <section className="dashboard-modules"><div className="section-heading"><div><span className="eyebrow">OPERATIONS</span><h2>{state?`${district||state} Operations`:country?`${country} Operations`:"Response Operations"}</h2></div></div>
   {topSites.length>0&&<div className="dashboard-inline-section"><div className="inline-title"><h3>Relocation & Safe Sites</h3><span>{regionSites.length} available in scope</span></div><div className="safe-site-strip">{topSites.map(s=><article className="safe-site-card" key={s.id}><span className="safe-pill">SAFE</span><strong>{s.name}</strong><small>{s.district||s.region||"Regional"}</small><span>Capacity <b>{s.available_capacity.toLocaleString()}</b></span><span>{s.facilities.slice(0,3).join(" · ")}</span></article>)}{regionSites.length>5&&<article className="safe-site-more">+{regionSites.length-5}<small>more safe sites</small></article>}</div></div>}
   {priorityVillage&&<div className="dashboard-inline-section relocation-inline"><div className="inline-title"><h3>Priority Relocation</h3><span>{priorityVillage.level} risk</span></div><div className="priority-relocation"><div><strong>{priorityVillage.name}</strong><span>{priorityVillage.district}, {priorityVillage.state} · Population {priorityVillage.population.toLocaleString()}</span></div><button className="btn" onClick={()=>navigate(`/relocation?village=${priorityVillage.id}`)}>Plan relocation</button></div></div>}
  </section>
  {detail&&<section className="detail-workspace"><div className="section-heading"><div><span className="eyebrow">ZONE INTELLIGENCE</span><h2>{detail.name}</h2></div><span>{detail.district}, {detail.state}</span></div><div className="detail-grid"><PopulationProfile village={detail}/><HazardBars village={detail}/><RainfallTrendChart village={detail}/><HistoryTimeline village={detail}/>{plan&&<RelocationBox plan={plan} onViewRoute={()=>navigate(`/relocation?village=${detail.id}`)}/>}</div></section>}
  <button className="floating-assistant" onClick={()=>navigate("/assistant")} aria-label="Open RakshaSetu AI Assistant"><span className="assistant-orb">AI</span><span><strong>RakshaSetu</strong><small>AI Assistant</small></span></button>
 </div>
}
function Legend({color,label}:{color:string;label:string}){return <span className="legend-item"><i style={{background:color}}/>{label}</span>}
