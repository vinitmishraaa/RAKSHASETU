import type { SafeSite, Village } from "../../types";
import "./region-details.css";

const known = (v: unknown): v is number => typeof v === "number" && Number.isFinite(v);
const sumKnown = (values: unknown[]) => values.filter(known).reduce((n, v) => n + v, 0);
const display = (v: unknown) => known(v) ? v.toLocaleString() : "—";

function Stat({ label, value, sub }: { label: string; value: string; sub?: string }) { return <div className="region-stat"><span>{label}</span><strong className="mono">{value}</strong>{sub && <small>{sub}</small>}</div>; }

export default function RegionDetailsPanel({ region, district, villages, safeSites, recommendedSite }: { region: string; district: string; villages: Village[]; safeSites: SafeSite[]; recommendedSite?: any }) {
  const populationValues = villages.map(v => v.population).filter(known);
  const population = populationValues.length === villages.length ? sumKnown(populationValues) : null;
  const childrenValues = villages.map(v => v.children).filter(known);
  const elderlyValues = villages.map(v => v.elderly).filter(known);
  const otherValues = villages.map(v => v.other_vulnerable).filter(known);
  const children = childrenValues.length ? sumKnown(childrenValues) : null;
  const elderly = elderlyValues.length ? sumKnown(elderlyValues) : null;
  const other = otherValues.length ? sumKnown(otherValues) : null;
  const vulnerable = children !== null && elderly !== null && other !== null ? children + elderly + other : null;
  const adults = population !== null && vulnerable !== null ? Math.max(0, population - vulnerable) : null;
  const avgRisk = villages.length ? Math.round(villages.reduce((n, v) => n + (known(v.risk_score) ? v.risk_score : 0), 0) / villages.length) : 0;
  const critical = villages.filter(v => v.level === "CRITICAL").length;
  const high = villages.filter(v => v.level === "HIGH").length;
  const capacityValues = safeSites.map(s => s.available_capacity).filter(known);
  const capacity = capacityValues.length ? sumKnown(capacityValues) : null;
  const highestRisk = [...villages].sort((a, b) => (b.risk_score || 0) - (a.risk_score || 0))[0];

  if (!region) return <div className="region-empty panel"><span className="eyebrow">READY</span><h3>Select a state or country</h3><p>Choose a region first, then a district. The map and response intelligence will narrow automatically.</p></div>;
  return <div className="region-details panel"><div className="region-title-row"><div><span className="eyebrow">DISTRICT VIEW</span><h3>{district || region}</h3><p>{district ? `${region} · focused district intelligence` : "Regional risk picture"}</p></div><span className={`risk-score-pill ${avgRisk >= 75 ? "critical" : avgRisk >= 55 ? "high" : avgRisk >= 35 ? "moderate" : "low"}`}>{avgRisk} RISK</span></div>
    <div className="region-stats"><Stat label="Population" value={display(population)} sub={population === null ? "not fully mapped" : `${villages.length} monitored zones`} /><Stat label="Children" value={display(children)} sub="only when mapped" /><Stat label="Adults" value={display(adults)} sub={adults === null ? "not derived" : "derived from mapped values"} /><Stat label="Elderly" value={display(elderly)} sub="only when mapped" /></div>
    <div className="region-risk-strip"><span><b>{critical}</b> Critical</span><span><b>{high}</b> High</span><span><b>{display(vulnerable)}</b> Vulnerable</span><span><b>{display(capacity)}</b> Safe capacity</span></div>
    {recommendedSite && <div className="safe-recommendation"><span className="eyebrow">MAPPED SAFE SITE</span><strong>{recommendedSite.site_name || recommendedSite.name || "Mapped site"}</strong><small>Operational capacity is shown only when verified by the source.</small><p>OpenStreetMap provides the mapped location; RakshaSetu does not infer occupancy, capacity or operational readiness.</p></div>}
    {highestRisk && <div className="region-action-card"><div><span className="eyebrow">PRIORITY ZONE</span><strong>{highestRisk.name}</strong><small>{highestRisk.district || district} · Risk {highestRisk.risk_score ?? "—"} · {highestRisk.level}</small></div><div><span className="eyebrow">RELOCATION LOGIC</span><p>Use official emergency instructions and verified shelter capacity for operational relocation decisions.</p></div></div>}
  </div>;
}
