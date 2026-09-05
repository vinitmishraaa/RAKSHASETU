import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import RiskBadge from "../../components/common/RiskBadge";
import { api } from "../../services/api";
import type { Village } from "../../types";

export default function Villages(){
 const [villages,setVillages]=useState<Village[]>([]); const [search,setSearch]=useState(""); const [params]=useSearchParams();
 const [region,setRegion]=useState(()=>params.get("region")||localStorage.getItem("rakshasetu_region")||"");
 useEffect(()=>{api.villages.list().then(setVillages)},[]);
 const regions=useMemo(()=>Array.from(new Set(villages.map(v=>v.state))).sort(),[villages]);
 const filtered=useMemo(()=>villages.filter(v=>(!region||v.state===region)&&(!search||`${v.name} ${v.district} ${v.state}`.toLowerCase().includes(search.toLowerCase()))).sort((a,b)=>b.risk_score-a.risk_score),[villages,region,search]);
 function changeRegion(v:string){setRegion(v);if(v)localStorage.setItem("rakshasetu_region",v);else localStorage.removeItem("rakshasetu_region")}
 return <div className="villages-page"><div className="villages-header"><div><span className="eyebrow">FIELD LOCATIONS</span><h2>Villages & Habitations</h2><p>{region?`${region} monitored locations`:"All monitored locations"}</p></div><div className="village-filters"><select value={region} onChange={e=>changeRegion(e.target.value)} aria-label="Region"><option value="">All regions</option>{regions.map(r=><option key={r} value={r}>{r}</option>)}</select><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search village, district…" /></div></div><div className="village-grid">{filtered.map(v=><article className="village-card" key={v.id}><div className="village-card-top"><span className="village-index">ZONE</span><RiskBadge level={v.level}/></div><h3>{v.name}</h3><p>{v.district}, {v.state}</p><div className="village-metrics"><span><small>Population</small><b>{v.population.toLocaleString()}</b></span><span><small>Risk</small><b>{v.risk_score}/100</b></span></div><button className="btn" onClick={()=>window.location.assign(`/?village=${v.id}`)}>View on map</button></article>)}</div>{!filtered.length&&<div className="panel village-empty">No monitored villages match this region/search.</div>}</div>;
}
