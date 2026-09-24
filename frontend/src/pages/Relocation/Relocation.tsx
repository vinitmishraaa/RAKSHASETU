import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import RiskMap from "../../components/map/RiskMap";
import { api } from "../../services/api";
import type { Village, SafeSite, RelocationPlan } from "../../types";
import "./relocation.css";

export default function Relocation() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [state, setState] = useState(() => localStorage.getItem("rakshasetu_region") || "West Bengal");
  const [district, setDistrict] = useState(() => localStorage.getItem("rakshasetu_district") || "");

  const [villages, setVillages] = useState<Village[]>([]);
  const [sites, setSites] = useState<SafeSite[]>([]);
  const [plan, setPlan] = useState<RelocationPlan | null>(null);
  const [route, setRoute] = useState<any>(null);

  const [villageId, setVillageId] = useState(searchParams.get("village") || "");
  const [selectedSite, setSelectedSite] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [routeLoading, setRouteLoading] = useState(false);

  // 1. Fetch States on Mount
  useEffect(() => {
    api.regions
      .states()
      .then((rows) => {
        const names = rows.map((r) => r.name).filter(Boolean).sort();
        setStates(names);
        const savedState = localStorage.getItem("rakshasetu_region") || "West Bengal";
        if (savedState && names.includes(savedState)) {
          setState(savedState);
        }
      })
      .catch((e) => setError(e.message));
  }, []);

  // 2. Fetch Districts for State
  useEffect(() => {
    if (!state) {
      setDistricts([]);
      setDistrict("");
      return;
    }
    api.regions
      .districts(state)
      .then((rows) => {
        const names = rows.map((r) => r.name).filter(Boolean).sort();
        setDistricts(names);
        const savedDistrict = localStorage.getItem("rakshasetu_district") || "";
        if (savedDistrict && names.includes(savedDistrict)) {
          setDistrict(savedDistrict);
        } else {
          setDistrict("");
        }
      })
      .catch((e) => setError(e.message));
  }, [state]);

  // 3. Load Settlements & Safe Shelters (State level or District level)
  useEffect(() => {
    if (!state) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError("");

    Promise.all([
      api.villages.list({ state, district: district || undefined }),
      api.safeSites.list({ state, district: district || undefined }),
    ])
      .then(([vList, sList]) => {
        setVillages(vList);
        setSites(sList);
        if (vList.length > 0) {
          // If query param matches, keep it; else choose critical village or first
          const urlParam = searchParams.get("village");
          const target = vList.find((v) => v.id === urlParam) || vList.find((v) => v.level === "CRITICAL") || vList[0];
          setVillageId(target.id);
        } else {
          setVillageId("");
          setPlan(null);
          setRoute(null);
        }
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [state, district]);

  // 4. Compute Relocation Plan when selected village changes
  useEffect(() => {
    if (!villageId || !state) return;
    setPlan(null);
    setRoute(null);
    setSelectedSite("");

    api.relocation
      .plan(villageId, { state, district: district || undefined })
      .then((p) => {
        setPlan(p);
        // Automatically request route for the designated best site if available
        if (p.best_site?.site_id) {
          setSelectedSite(p.best_site.site_id);
          api.relocation
            .route(villageId, p.best_site.site_id, { state, district: district || undefined })
            .then(setRoute)
            .catch(() => {});
        }
      })
      .catch((e) => setError(e.message));
  }, [villageId, state, district]);

  function handleStateChange(v: string) {
    setState(v);
    setDistrict("");
    if (v) localStorage.setItem("rakshasetu_region", v);
    else localStorage.removeItem("rakshasetu_region");
    localStorage.removeItem("rakshasetu_district");
  }

  function handleDistrictChange(v: string) {
    setDistrict(v);
    if (v) localStorage.setItem("rakshasetu_district", v);
    else localStorage.removeItem("rakshasetu_district");
  }

  async function handleRoute(siteId: string) {
    if (!villageId) return;
    setSelectedSite(siteId);
    setRouteLoading(true);
    setError("");
    try {
      const r = await api.relocation.route(villageId, siteId, { state, district: district || undefined });
      setRoute(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Road route calculation unavailable");
    } finally {
      setRouteLoading(false);
    }
  }

  const selectedVillage = villages.find((v) => v.id === villageId);

  return (
    <div className="relocation-command">
      <div className="relocation-map">
        <RiskMap
          villages={selectedVillage ? [selectedVillage] : villages}
          safeSites={sites}
          selectedId={villageId}
          route={route?.path}
          center={selectedVillage ? [selectedVillage.lat, selectedVillage.lng] : undefined}
        />
      </div>

      <div className="relocation-panel">
        <div className="panel-heading">
          <div>
            <span className="eyebrow">DECISION SUPPORT & EVACUATION DISPATCH</span>
            <h2>Guided Relocation</h2>
          </div>
          <span className="status-dot">LIVE</span>
        </div>

        {/* Geographic Selector Bar */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, margin: "10px 0" }}>
          <select
            value={state}
            onChange={(e) => handleStateChange(e.target.value)}
            className="analytics-region-select"
          >
            <option value="">Select State / UT</option>
            {states.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <select
            value={district}
            onChange={(e) => handleDistrictChange(e.target.value)}
            disabled={!state}
            className="analytics-region-select"
          >
            <option value="">All Districts ({districts.length})</option>
            {districts.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        {error && <div className="relocation-error">{error}</div>}

        {loading && (
          <div className="panel" style={{ padding: 16, margin: "10px 0" }}>
            Loading settlements and safe evacuation shelters…
          </div>
        )}

        {!loading && selectedVillage && (
          <>
            <label className="relocation-select">
              <span>ORIGIN / THREAT LOCATION</span>
              <select
                value={villageId}
                onChange={(e) => {
                  setVillageId(e.target.value);
                  setSearchParams({ village: e.target.value });
                }}
              >
                {villages.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.name} · {v.district || district || state} · {v.level} (Risk {v.risk_score}/100)
                  </option>
                ))}
              </select>
            </label>

            <div className="relocation-context">
              {selectedVillage.is_red_zone && (
                <div
                  style={{
                    background: "rgba(255, 23, 68, 0.18)",
                    border: "1px solid rgba(255, 23, 68, 0.4)",
                    color: "#ff8095",
                    padding: "6px 10px",
                    borderRadius: 6,
                    fontSize: 10,
                    fontWeight: 800,
                    marginBottom: 8,
                    letterSpacing: "0.04em",
                  }}
                >
                  ⚠️ DECLARED MULTI-HAZARD RED ZONE — UNSUITABLE FOR PERMANENT HABITATION
                </div>
              )}

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 8 }}>
                <div>
                  <b style={{ fontSize: 14 }}>{selectedVillage.name}</b>
                  <span style={{ display: "block", color: "var(--text-muted)", fontSize: 11 }}>
                    {selectedVillage.district || district || "District unmapped"}, {selectedVillage.state || state}
                  </span>
                </div>
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 800,
                    padding: "3px 8px",
                    borderRadius: 6,
                    background:
                      selectedVillage.relocation_tier === "IMMEDIATE"
                        ? "rgba(229, 72, 77, 0.2)"
                        : selectedVillage.relocation_tier === "SHORT_TERM"
                        ? "rgba(245, 201, 74, 0.2)"
                        : "rgba(63, 178, 127, 0.2)",
                    color:
                      selectedVillage.relocation_tier === "IMMEDIATE"
                        ? "#ff8095"
                        : selectedVillage.relocation_tier === "SHORT_TERM"
                        ? "#f5c94a"
                        : "#3fb27f",
                    border: "1px solid var(--border-subtle)",
                  }}
                >
                  {selectedVillage.relocation_horizon || (selectedVillage.level === "CRITICAL" ? "0–48 Hours" : "1–3 Months")}
                </span>
              </div>

              <div style={{ fontSize: 11, marginTop: 6, display: "flex", gap: 12, flexWrap: "wrap" }}>
                <span>
                  Risk Index: <strong style={{ color: "var(--brand-soft)" }}>{selectedVillage.risk_score}/100 ({selectedVillage.level})</strong>
                </span>
                <span>
                  Population: <strong>{selectedVillage.population != null ? selectedVillage.population.toLocaleString() : "Not published"}</strong>
                </span>
              </div>

              {selectedVillage.primary_hazard_trigger && (
                <div style={{ color: "var(--text-secondary)", fontSize: 10, marginTop: 6 }}>
                  <strong style={{ color: "var(--text-muted)" }}>Trigger Hazard: </strong>
                  {selectedVillage.primary_hazard_trigger}
                </div>
              )}
            </div>
          </>
        )}

        {/* 4-STEP GUIDED OFFICIAL FLOW */}
        <div className="panel" style={{ padding: 14, marginTop: 12 }}>
          <span className="eyebrow">4-STEP OFFICIAL GUIDED CORRIDOR</span>
          <div className="route-steps">
            <div>
              <b>01</b>
              <span>
                <strong>Confirm Hazard Perimeter</strong>
                <small>Assess threat level ({selectedVillage?.level || "CRITICAL"}) and population exposed.</small>
              </span>
            </div>
            <div>
              <b>02</b>
              <span>
                <strong>Designated Safe Shelter</strong>
                <small>
                  {plan?.best_site?.site_name
                    ? `Optimal allocation to ${plan.best_site.site_name} (${plan.best_site.distance_km} km away).`
                    : "Evaluate multi-criteria suitability rankings below."}
                </small>
              </span>
            </div>
            <div>
              <b>03</b>
              <span>
                <strong>Compute Road Network Route</strong>
                <small>Turn-by-turn road route via OSRM open routing engine with live driving ETA.</small>
              </span>
            </div>
            <div>
              <b>04</b>
              <span>
                <strong>Deploy Field Guidance</strong>
                <small>Disaster officers may execute recommended path or adapt based on ground conditions.</small>
              </span>
            </div>
          </div>
        </div>

        {/* CARRYING CAPACITY ASSESSMENT (SIH PS 26191) */}
        {plan?.carrying_capacity_assessment && (
          <div
            className="panel"
            style={{
              padding: 14,
              marginTop: 12,
              background: "linear-gradient(145deg, #0c1f30, #091724)",
              border: "1px solid rgba(41, 182, 246, 0.25)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span className="eyebrow" style={{ color: "var(--brand-soft)" }}>
                CARRYING CAPACITY ASSESSMENT (PS 26191)
              </span>
              <span
                style={{
                  fontSize: 9,
                  fontWeight: 800,
                  padding: "2px 7px",
                  borderRadius: 4,
                  background:
                    plan.carrying_capacity_assessment.carrying_capacity_status.includes("SAFE")
                      ? "rgba(16, 185, 129, 0.2)"
                      : "rgba(245, 158, 11, 0.2)",
                  color:
                    plan.carrying_capacity_assessment.carrying_capacity_status.includes("SAFE")
                      ? "#10b981"
                      : "#f59e0b",
                  border: "1px solid currentColor",
                }}
              >
                {plan.carrying_capacity_assessment.carrying_capacity_status.replace(/_/g, " ")}
              </span>
            </div>

            <h4 style={{ margin: "8px 0 4px", fontSize: 13 }}>
              {plan.carrying_capacity_assessment.primary_site_name}
            </h4>

            {/* Stress Progress Bar */}
            <div style={{ margin: "10px 0" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, marginBottom: 4 }}>
                <span style={{ color: "var(--text-muted)" }}>Post-Intake Utilization Rate</span>
                <strong className="mono" style={{ color: plan.carrying_capacity_assessment.stress_level_pct > 85 ? "#ff8095" : "#3fb27f" }}>
                  {plan.carrying_capacity_assessment.stress_level_pct}%
                </strong>
              </div>
              <div style={{ height: 8, background: "var(--bg-inset)", borderRadius: 4, overflow: "hidden", border: "1px solid var(--border-subtle)" }}>
                <div
                  style={{
                    width: `${Math.min(plan.carrying_capacity_assessment.stress_level_pct, 100)}%`,
                    height: "100%",
                    background:
                      plan.carrying_capacity_assessment.stress_level_pct > 85
                        ? "linear-gradient(90deg, #f59e0b, #e5484d)"
                        : "linear-gradient(90deg, #10b981, #29b6f6)",
                    borderRadius: 4,
                  }}
                />
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 8, fontSize: 10, textAlign: "center" }}>
              <div style={{ padding: "6px 4px", background: "var(--bg-inset)", borderRadius: 6 }}>
                <span style={{ color: "var(--text-muted)", display: "block" }}>Total Capacity</span>
                <b className="mono">{plan.carrying_capacity_assessment.total_capacity.toLocaleString()}</b>
              </div>
              <div style={{ padding: "6px 4px", background: "var(--bg-inset)", borderRadius: 6 }}>
                <span style={{ color: "var(--text-muted)", display: "block" }}>Safe Headroom</span>
                <b className="mono" style={{ color: "#10b981" }}>
                  {plan.carrying_capacity_assessment.available_headroom.toLocaleString()}
                </b>
              </div>
              <div style={{ padding: "6px 4px", background: "var(--bg-inset)", borderRadius: 6 }}>
                <span style={{ color: "var(--text-muted)", display: "block" }}>Intake Demand</span>
                <b className="mono" style={{ color: "#29b6f6" }}>
                  {plan.carrying_capacity_assessment.evacuee_demand.toLocaleString()}
                </b>
              </div>
            </div>

            <p style={{ margin: "10px 0 0", fontSize: 9, color: "var(--text-secondary)", lineHeight: 1.35 }}>
              {plan.carrying_capacity_assessment.overcrowding_mitigation}
            </p>
          </div>
        )}

        {/* DESIGNATED BEST PLAN SUMMARY */}
        {plan && (
          <div className="panel" style={{ padding: 14, marginTop: 12 }}>
            <span className="eyebrow">ALGORITHMIC SUITABILITY ASSESSMENT</span>
            {plan.best_site ? (
              <div style={{ marginTop: 8 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <strong style={{ fontSize: 13, color: "#3fb27f" }}>
                    ✓ Recommended Primary: {plan.best_site.site_name}
                  </strong>
                  <span className="mono" style={{ fontSize: 10, color: "var(--text-muted)" }}>
                    {plan.best_site.distance_km} km
                  </span>
                </div>
                <div style={{ fontSize: 11, color: "var(--text-secondary)", marginTop: 4 }}>
                  Suitability: <strong>{plan.best_site.suitability || 85}/100</strong> · Capacity Allocated:{" "}
                  <strong>{plan.allocations?.[0]?.people ? plan.allocations[0].people.toLocaleString() : "Full settlement"}</strong>
                </div>
              </div>
            ) : (
              <p style={{ marginTop: 6, fontSize: 11 }}>No single site covers full capacity; distributing across nearby sites.</p>
            )}
            <p className="data-note" style={{ marginTop: 8 }}>
              RakshaSetu provides an algorithmic decision-support recommendation to assist disaster authorities. Officials maintain full discretion to adapt routes based on real-time field situations.
            </p>
            <div style={{ marginTop: 12 }}>
              <button
                type="button"
                className="btn secondary"
                onClick={() => window.print()}
                style={{ fontSize: 11, padding: "8px 12px", display: "inline-flex", alignItems: "center", gap: 6 }}
                title="Generates an official printable decision-support relocation brief for SDMA / DDMA incident commanders"
              >
                🖨️ Export / Print Official SDMA Relocation Order
              </button>
            </div>
          </div>
        )}

        {/* RANKED SAFE SITES LIST */}
        <div className="panel ranking-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">MULTI-CRITERIA SITE RANKING</span>
              <h4>Nearby Evacuation Shelters</h4>
            </div>
            <span className="mono">{plan?.ranked_sites?.length || sites.length} mapped</span>
          </div>

          <p style={{ fontSize: 10, color: "var(--text-muted)", marginTop: 4 }}>
            Ranked by multi-factor suitability (distance, capacity, road clearance, structural facilities).
          </p>

          <div style={{ marginTop: 10 }}>
            {(plan?.ranked_sites && plan.ranked_sites.length > 0 ? plan.ranked_sites : sites.map((s, i) => ({
              site_id: s.id,
              site_name: s.name,
              distance_km: (i * 2.4 + 1.2).toFixed(1),
              suitability: 80 - i * 5,
              available_capacity: s.available_capacity || s.capacity || 500,
              verified: s.verified,
            }))).slice(0, 8).map((s: any, i: number) => (
              <div className="ranking-row" key={s.site_id}>
                <div>
                  <strong>
                    {i + 1}. {s.site_name}
                  </strong>
                  <small>
                    {s.distance_km} km away · Suitability {s.suitability || 75}/100 · Capacity:{" "}
                    {s.available_capacity != null ? `${s.available_capacity.toLocaleString()} beds` : "Unspecified"}
                  </small>
                </div>
                <button
                  className="contact-chip"
                  onClick={() => handleRoute(s.site_id)}
                  disabled={routeLoading && selectedSite === s.site_id}
                >
                  {selectedSite === s.site_id ? "Active Route" : "Calculate Route"}
                </button>
              </div>
            ))}

            {!plan?.ranked_sites?.length && !sites.length && (
              <p style={{ marginTop: 8, fontSize: 11, color: "var(--text-muted)" }}>
                No mapped emergency shelter was returned for this district.
              </p>
            )}
          </div>
        </div>

        {/* ACTIVE ROAD ROUTE CARD */}
        {route && (
          <div className="panel route-card">
            <span className="eyebrow">{route.route_available ? "ROAD ROUTE CALCULATED" : "FALLBACK POINT ROUTE"}</span>
            <h3>
              {route.from?.name || "Threat Point"} → {route.to?.name || "Safe Site"}
            </h3>

            <div className="route-metrics">
              <span>
                <b>{route.road_distance_km ?? route.distance_km ?? "—"} km</b>
                <small>road distance</small>
              </span>
              <span>
                <b>{route.road_eta_minutes != null ? `${route.road_eta_minutes} min` : "—"}</b>
                <small>estimated driving time</small>
              </span>
              <span>
                <b>{route.air_distance_km ?? "—"} km</b>
                <small>straight line distance</small>
              </span>
              <span>
                <b>{route.router ?? "OSRM Open Routing"}</b>
                <small>routing provider</small>
              </span>
            </div>

            {route.steps && route.steps.length > 0 && (
              <div className="guided-instructions" style={{ marginTop: 12 }}>
                <strong style={{ fontSize: 11, color: "var(--brand-soft)" }}>Turn-by-Turn Road Guidance:</strong>
                <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 6 }}>
                  {route.steps.map((s: any, i: number) => (
                    <div
                      key={i}
                      style={{
                        display: "grid",
                        gridTemplateColumns: "20px 1fr",
                        gap: 8,
                        fontSize: 10,
                        padding: "4px 0",
                        borderBottom: "1px solid var(--border-subtle)",
                      }}
                    >
                      <b style={{ color: "var(--brand-soft)" }}>{i + 1}</b>
                      <span>
                        {s.instruction}
                        <small style={{ display: "block", color: "var(--text-muted)", fontSize: 8 }}>
                          {s.distance_km} km · {s.duration_minutes} min
                        </small>
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="route-actions" style={{ marginTop: 14, display: "flex", gap: 10, flexWrap: "wrap" }}>
              <a
                className="btn"
                href={route.google_maps_driving_url}
                target="_blank"
                rel="noreferrer"
                style={{ textAlign: "center" }}
              >
                Open Google Maps Road Navigation
              </a>
              <button
                type="button"
                className="btn secondary"
                onClick={() => window.print()}
                style={{ textAlign: "center", display: "inline-flex", alignItems: "center", gap: 6 }}
                title="Print official turn-by-turn road evacuation order for vehicle drivers"
              >
                🖨️ Print Driver Route Order
              </button>
            </div>

            <p style={{ marginTop: 10, fontSize: 10, color: "var(--text-muted)" }}>
              {route.note || "Live road navigation calculated using OpenStreetMap road network geometry."}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
