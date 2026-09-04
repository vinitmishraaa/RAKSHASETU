import type { SafeSite, Village } from "../../types";

function Stat({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return <div className="region-stat"><span>{label}</span><strong className="mono">{value}</strong>{sub && <small>{sub}</small>}</div>;
}

export default function RegionDetailsPanel({
  region,
  district,
  villages,
  safeSites,
}: {
  region: string;
  district: string;
  villages: Village[];
  safeSites: SafeSite[];
}) {
  const population = villages.reduce((n, v) => n + v.population, 0);
  const children = villages.reduce((n, v) => n + (v.children || 0), 0);
  const elderly = villages.reduce((n, v) => n + (v.elderly || 0), 0);
  const other = villages.reduce((n, v) => n + (v.other_vulnerable || 0), 0);
  const vulnerable = children + elderly + other;
  const adults = Math.max(0, population - vulnerable);
  const avgRisk = villages.length ? Math.round(villages.reduce((n, v) => n + v.risk_score, 0) / villages.length) : 0;
  const critical = villages.filter((v) => v.level === "CRITICAL").length;
  const high = villages.filter((v) => v.level === "HIGH").length;
  const regionSites = safeSites.filter((s) => !s.region || s.region === region);
  const capacity = regionSites.reduce((n, s) => n + s.available_capacity, 0);
  const highestRisk = [...villages].sort((a, b) => b.risk_score - a.risk_score)[0];

  if (!region) {
    return <div className="region-empty panel"><span className="eyebrow">READY</span><h3>Select a state or country</h3><p>Choose a region first, then optionally choose a district. The map and response intelligence will narrow automatically.</p></div>;
  }

  return (
    <div className="region-details panel">
      <div className="region-title-row">
        <div><span className="eyebrow">{district ? "DISTRICT VIEW" : "REGION VIEW"}</span><h3>{district || region}</h3><p>{district ? `${region} · focused district intelligence` : "Full regional risk and population picture"}</p></div>
        <span className={`risk-score-pill ${avgRisk >= 75 ? "critical" : avgRisk >= 55 ? "high" : avgRisk >= 35 ? "moderate" : "low"}`}>{avgRisk} RISK</span>
      </div>

      <div className="region-stats">
        <Stat label="Population" value={population.toLocaleString()} sub={`${villages.length} monitored zones`} />
        <Stat label="Children" value={children.toLocaleString()} sub="priority group" />
        <Stat label="Adults" value={adults.toLocaleString()} sub="estimated" />
        <Stat label="Elderly" value={elderly.toLocaleString()} sub="priority group" />
      </div>

      <div className="region-risk-strip">
        <span><b>{critical}</b> Critical</span><span><b>{high}</b> High</span><span><b>{vulnerable.toLocaleString()}</b> Vulnerable</span><span><b>{capacity.toLocaleString()}</b> Safe capacity</span>
      </div>

      {highestRisk && (
        <div className="region-action-card">
          <div><span className="eyebrow">PRIORITY ZONE</span><strong>{highestRisk.name}</strong><small>{highestRisk.district} · Risk {highestRisk.risk_score} · {highestRisk.level}</small></div>
          <div><span className="eyebrow">RELOCATION LOGIC</span><p>Prioritize children, elderly and other vulnerable residents for the nearest high-suitability safe site; preserve capacity for the remaining population.</p></div>
        </div>
      )}
    </div>
  );
}
