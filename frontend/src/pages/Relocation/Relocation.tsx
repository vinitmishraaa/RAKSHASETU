import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import RiskMap from "../../components/map/RiskMap";
import RelocationBox from "../../components/relocation/RelocationBox";
import { api } from "../../services/api";
import type { Village, SafeSite, RelocationPlan } from "../../types";

export default function Relocation() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [villages, setVillages] = useState<Village[]>([]);
  const [sites, setSites] = useState<SafeSite[]>([]);
  const [villageId, setVillageId] = useState(searchParams.get("village") || "");
  const [plan, setPlan] = useState<RelocationPlan | null>(null);
  const [route, setRoute] = useState<any>(null);

  useEffect(() => {
    Promise.all([api.villages.list(), api.safeSites.list()]).then(([v, s]) => {
      setVillages(v);
      setSites(s);
      if (!villageId && v.length) setVillageId(v[0].id);
    });
  }, []);

  useEffect(() => {
    if (!villageId) return;
    setSearchParams({ village: villageId });
    api.relocation.plan(villageId).then(setPlan);
    setRoute(null);
  }, [villageId]);

  const selectedVillage = villages.find((v) => v.id === villageId);

  async function handleViewRoute(siteId: string) {
    if (!villageId) return;
    const r = await api.relocation.route(villageId, siteId);
    setRoute(r);
  }

  return (
    <div style={{ display: "flex", flex: 1, minHeight: 0 }}>
      <div style={{ flex: 2, position: "relative", borderRight: "1px solid var(--border-subtle)" }}>
        <RiskMap
          villages={selectedVillage ? [selectedVillage] : villages}
          safeSites={sites}
          selectedId={villageId}
          center={selectedVillage ? [selectedVillage.lat, selectedVillage.lng] : undefined}
        />
      </div>

      <div style={{ flex: 1, minWidth: 340, maxWidth: 420, padding: 20, overflowY: "auto" }}>
        <label style={{ display: "block", marginBottom: 16 }}>
          <span style={{ fontSize: 12, color: "var(--text-muted)", fontWeight: 600 }}>VILLAGE</span>
          <select
            value={villageId}
            onChange={(e) => setVillageId(e.target.value)}
            style={{
              display: "block",
              marginTop: 6,
              width: "100%",
              background: "var(--bg-inset)",
              color: "var(--text-primary)",
              border: "1px solid var(--border-subtle)",
              borderRadius: 6,
              padding: "9px 10px",
              fontSize: 14,
            }}
          >
            {villages.map((v) => (
              <option key={v.id} value={v.id}>
                {v.name} ({v.level})
              </option>
            ))}
          </select>
        </label>

        {plan && <RelocationBox plan={plan} onViewRoute={handleViewRoute} />}

        {plan && plan.ranked_sites.length > 0 && (
          <div className="panel" style={{ padding: 20, marginTop: 16 }}>
            <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 12 }}>
              SITE SUITABILITY RANKING
            </h4>
            {plan.ranked_sites.map((s, i) => (
              <div
                key={s.site_id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "10px 0",
                  borderBottom: i < plan.ranked_sites.length - 1 ? "1px solid var(--border-subtle)" : "none",
                }}
              >
                <div>
                  <div style={{ fontSize: 13.5, fontWeight: 600 }}>{s.site_name}</div>
                  <div style={{ fontSize: 11.5, color: "var(--text-muted)" }}>
                    {s.distance_km} km · {s.road_access} access
                  </div>
                </div>
                <div className="mono" style={{ fontSize: 16, fontWeight: 700, color: i === 0 ? "var(--brand)" : "var(--text-primary)" }}>
                  {s.suitability}
                </div>
              </div>
            ))}
          </div>
        )}

        {route && (
          <div className="panel" style={{ padding: 20, marginTop: 16 }}>
            <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 10 }}>ROUTE</h4>
            <p style={{ fontSize: 13 }}>
              {route.from.name} → {route.to.name}: <strong className="mono">{route.distance_km} km</strong>
            </p>
            <p style={{ fontSize: 11.5, marginTop: 8, color: "var(--text-muted)" }}>{route.note}</p>
          </div>
        )}
      </div>
    </div>
  );
}
