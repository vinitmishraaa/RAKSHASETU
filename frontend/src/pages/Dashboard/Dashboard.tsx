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

  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [cities, setCities] = useState<string[]>([]);

  // Default to West Bengal if nothing saved, or load saved state
  const [state, setState] = useState(() => localStorage.getItem("rakshasetu_region") || "West Bengal");
  const [district, setDistrict] = useState(() => localStorage.getItem("rakshasetu_district") || "");
  const [city, setCity] = useState(() => localStorage.getItem("rakshasetu_city") || "");

  const [villages, setVillages] = useState<Village[]>([]);
  const [safeSites, setSafeSites] = useState<SafeSite[]>([]);
  const [liveFeed, setLiveFeed] = useState<LiveHazardFeed>({ updated_at: "", items: [], sources: [] });
  const [news, setNews] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<VillageDetail | null>(null);

  const [loading, setLoading] = useState(false);
  const [locationLoading, setLocationLoading] = useState(false);
  const [error, setError] = useState("");

  // 1. Fetch Indian States/UTs on Mount
  useEffect(() => {
    api.regions
      .states()
      .then((rows) => {
        const names = rows.map((r) => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
        setStates(names);
        const savedState = localStorage.getItem("rakshasetu_region") || "West Bengal";
        if (savedState && names.includes(savedState)) {
          setState(savedState);
        } else if (names.includes("West Bengal")) {
          setState("West Bengal");
        }
      })
      .catch((e) => {
        setError(e.message);
      })
      .finally(() => {
        restoring.current = false;
      });
  }, []);

  // 2. Fetch official districts for selected state
  useEffect(() => {
    let active = true;
    if (!state) {
      setDistricts([]);
      setDistrict("");
      setCities([]);
      setCity("");
      return;
    }
    setLocationLoading(true);
    api.regions
      .districts(state)
      .then((rows) => {
        if (!active) return;
        const names = rows.map((r) => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
        setDistricts(names);
        // Only keep district if it belongs to this state
        const savedDistrict = localStorage.getItem("rakshasetu_district") || "";
        if (savedDistrict && names.includes(savedDistrict)) {
          setDistrict(savedDistrict);
        } else {
          setDistrict("");
          setCity("");
        }
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setLocationLoading(false);
      });

    return () => {
      active = false;
    };
  }, [state]);

  // 3. Fetch cities for selected district
  useEffect(() => {
    let active = true;
    if (!state || !district) {
      setCities([]);
      setCity("");
      return;
    }
    api.regions
      .cities(state, district)
      .then((rows) => {
        if (!active) return;
        const names = rows.map((r) => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b));
        setCities(names);
        const savedCity = localStorage.getItem("rakshasetu_city") || "";
        if (savedCity && names.includes(savedCity)) {
          setCity(savedCity);
        } else {
          setCity("");
        }
      })
      .catch((e) => {
        if (active) setError(e.message);
      });

    return () => {
      active = false;
    };
  }, [state, district]);

  // 4. LOAD OPERATIONAL DATA IMMEDIATELY ON STATE SELECTION (District & City refine it)
  useEffect(() => {
    let active = true;
    setError("");

    if (!state) {
      setVillages([]);
      setSafeSites([]);
      setLiveFeed({ updated_at: "", items: [], sources: [] });
      setNews([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    localStorage.setItem("rakshasetu_region", state);
    if (district) localStorage.setItem("rakshasetu_district", district);
    else localStorage.removeItem("rakshasetu_district");
    if (city) localStorage.setItem("rakshasetu_city", city);
    else localStorage.removeItem("rakshasetu_city");

    Promise.all([
      api.villages.list({ state, district: district || undefined, city: city || undefined }),
      api.safeSites.list({ state, district: district || undefined, city: city || undefined }),
      api.live.hazards(state, district || undefined),
      api.live.news(state, district || undefined),
    ])
      .then(([v, s, live, n]) => {
        if (!active) return;
        setVillages(v);
        setSafeSites(s);
        setLiveFeed(live);
        setNews(n.articles || []);
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [state, district, city]);

  const [relocationTier, setRelocationTier] = useState<string>("");
  const [mode, setMode] = useState<"PROACTIVE" | "TACTICAL">("TACTICAL");
  const [redZoneOnly, setRedZoneOnly] = useState<boolean>(false);

  const redZonesCount = villages.filter((v) => v.is_red_zone).length;
  const immediateCount = villages.filter((v) => v.relocation_tier === "IMMEDIATE").length;
  const shortTermCount = villages.filter((v) => v.relocation_tier === "SHORT_TERM").length;
  const mediumTermCount = villages.filter((v) => v.relocation_tier === "MEDIUM_TERM").length;

  const displayedVillages = useMemo(() => {
    let list = villages;
    if (redZoneOnly) {
      list = list.filter((v) => v.is_red_zone);
    }
    if (relocationTier) {
      list = list.filter((v) => v.relocation_tier === relocationTier);
    }
    return list;
  }, [villages, relocationTier, redZoneOnly]);

  const critical = villages.filter((v) => v.level === "CRITICAL").length;
  const high = villages.filter((v) => v.level === "HIGH").length;
  const knownPopulation = villages.reduce((sum, v) => sum + (v.population ?? 0), 0);
  const priority = useMemo(() => [...villages].sort((a, b) => b.risk_score - a.risk_score)[0], [villages]);
  const liveItems = liveFeed.items || [];
  const mapHazards = liveItems.filter((h) => h.lat != null && h.lng != null);

  async function selectVillage(v: Village) {
    setSelectedId(v.id);
    try {
      const fullDetail = await api.villages.get(v.id, { state, district, city });
      setDetail(fullDetail);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load settlement details");
    }
  }

  function clearScope() {
    setState("");
    setDistrict("");
    setCity("");
    setCities([]);
    setDistricts([]);
    setVillages([]);
    setSafeSites([]);
    setLiveFeed({ updated_at: "", items: [], sources: [] });
    setNews([]);
    setSelectedId(null);
    setDetail(null);
    localStorage.removeItem("rakshasetu_region");
    localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  const currentScopeTitle = city
    ? `${city}, ${district}, ${state}`
    : district
    ? `${district}, ${state}`
    : state || "India";

  return (
    <div className="dashboard-page">
      <section className="dashboard-hero">
        <div>
          <span className="eyebrow">COMMAND CENTER · DISASTER DECISION INTELLIGENCE</span>
          <h1>RakshaSetu</h1>
          <p>
            Real-time hazard monitoring, GIS risk calculation, and capacity-aware relocation guidance.
          </p>
        </div>
        <div className="hero-live-badge">
          <i /> REAL-TIME CONNECTED
        </div>
      </section>

      {/* Filter Bar: State -> District -> City -> Relocation Tier & Mode */}
      <FilterBar
        states={states}
        state={state}
        setState={setState}
        districts={districts}
        district={district}
        setDistrict={setDistrict}
        cities={cities}
        city={city}
        setCity={setCity}
        relocationTier={relocationTier}
        setRelocationTier={setRelocationTier}
        mode={mode}
        setMode={setMode}
        loading={locationLoading}
      />

      {/* SIH PS 26191 OPERATIONAL DECISION INTELLIGENCE BANNER */}
      <div
        className="panel"
        style={{
          margin: "12px 0",
          padding: "12px 16px",
          background:
            mode === "PROACTIVE"
              ? "linear-gradient(90deg, rgba(63, 178, 127, 0.12), rgba(11, 27, 42, 0.95))"
              : "linear-gradient(90deg, rgba(229, 72, 77, 0.12), rgba(11, 27, 42, 0.95))",
          border: mode === "PROACTIVE" ? "1px solid rgba(63, 178, 127, 0.35)" : "1px solid rgba(229, 72, 77, 0.35)",
          borderRadius: 12,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span
            style={{
              padding: "4px 8px",
              borderRadius: 6,
              fontSize: 10,
              fontWeight: 800,
              background: mode === "PROACTIVE" ? "rgba(63, 178, 127, 0.2)" : "rgba(229, 72, 77, 0.2)",
              color: mode === "PROACTIVE" ? "#3fb27f" : "#ff8095",
              border: mode === "PROACTIVE" ? "1px solid rgba(63, 178, 127, 0.4)" : "1px solid rgba(229, 72, 77, 0.4)",
            }}
          >
            {mode === "PROACTIVE" ? "PROACTIVE RESETTLEMENT MODE" : "EMERGENCY TACTICAL MODE"}
          </span>
          <span style={{ fontSize: 11, color: "var(--text-secondary)" }}>
            {mode === "PROACTIVE"
              ? "Long-term carrying capacity analysis & pre-monsoon habitation relocation planning."
              : "Live Open-Meteo & USGS feeds linked with 0–48h rapid evacuation corridor dispatch."}
          </span>
        </div>

        {/* 3-Tier Relocation Need Quick Badges */}
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              color: "#ff8095",
              background: "rgba(229, 72, 77, 0.15)",
              padding: "4px 9px",
              borderRadius: 6,
            }}
            title="Immediate 0-48h evacuation needs"
          >
            🔴 Immediate: <b>{immediateCount}</b>
          </span>
          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              color: "#f5c94a",
              background: "rgba(245, 201, 74, 0.15)",
              padding: "4px 9px",
              borderRadius: 6,
            }}
            title="Short-term 1-3 months pre-monsoon relocation"
          >
            🟠 Short-Term: <b>{shortTermCount}</b>
          </span>
          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              color: "#3fb27f",
              background: "rgba(63, 178, 127, 0.15)",
              padding: "4px 9px",
              borderRadius: 6,
            }}
            title="Medium-term 6-12 months permanent resettlement"
          >
            🟡 Medium-Term: <b>{mediumTermCount}</b>
          </span>
          {redZonesCount > 0 && (
            <button
              type="button"
              onClick={() => setRedZoneOnly(!redZoneOnly)}
              style={{
                fontSize: 11,
                fontWeight: 800,
                cursor: "pointer",
                color: redZoneOnly ? "#ffffff" : "#ff4466",
                background: redZoneOnly ? "#e5484d" : "rgba(255, 68, 102, 0.2)",
                border: "1px solid rgba(255, 68, 102, 0.4)",
                padding: "4px 9px",
                borderRadius: 6,
                transition: "all 0.2s ease",
              }}
              title="Click to isolate only Multi-Hazard Red Zones (Unsuitable for Habitation)"
            >
              ⚠️ {redZonesCount} Red Zones {redZoneOnly ? "✓ (FILTER APPLIED)" : ""}
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="panel" style={{ margin: "12px 0", padding: 16, borderLeft: "4px solid var(--risk-critical)" }}>
          <strong>Operational Notice</strong>
          <p>{error}</p>
          <button className="btn secondary" onClick={() => window.location.reload()}>
            Retry Connection
          </button>
        </div>
      )}

      {loading && (
        <div className="panel" style={{ margin: "12px 0", padding: 14 }}>
          Fetching real-time data & physical indicators for <strong>{currentScopeTitle}</strong>…
        </div>
      )}

      {/* Primary Command Stage: Map & Selected Area Panel */}
      <section className="command-grid">
        <div className="map-stage">
          <RiskMap
            villages={displayedVillages}
            safeSites={safeSites}
            liveHazards={mapHazards}
            selectedId={selectedId}
            onSelectVillage={selectVillage}
            region={state || "India"}
            district={district}
          />
          <div className="map-overlay-title">
            <strong>{currentScopeTitle}</strong>
            <span>
              {villages.length} monitored locations · {safeSites.length} safe shelters · {critical} critical · {high} high
            </span>
          </div>
          <div className="map-legend">
            <Legend color="var(--risk-critical)" label="Critical Zone (Blow-out buffer)" />
            <Legend color="var(--risk-high)" label="High Risk" />
            <Legend color="var(--risk-moderate)" label="Moderate Risk" />
            <Legend color="var(--risk-low)" label="Low Risk" />
            <Legend color="#10b981" label="Safe Shelter (Green glow)" />
            <Legend color="#ff1744" label="Live Hazard (USGS / FIRMS)" />
          </div>
        </div>

        <aside className="details-stage">
          <div className="panel-heading">
            <div>
              <span className="eyebrow">LOCATION PROFILE</span>
              <h2>{selectedId && detail ? detail.name : currentScopeTitle}</h2>
            </div>
            <span className="status-dot">ACTIVE</span>
          </div>

          {selectedId && detail ? (
            <SelectedAreaPanel
              village={detail}
              onViewRelocation={() => navigate(`/relocation?village=${detail.id}`)}
            />
          ) : state ? (
            <RegionDetailsPanel
              region={state}
              district={district}
              villages={villages}
              safeSites={safeSites}
              recommendedSite={safeSites[0] || null}
            />
          ) : (
            <div className="region-empty panel">
              <span className="eyebrow">COMMAND DATA SCOPE</span>
              <h3>Select a State / UT to Load Operational Intelligence</h3>
              <p>State selection immediately loads monitored settlements, emergency shelters, and live hazard feeds.</p>
            </div>
          )}
        </aside>
      </section>

      {/* Real-time Public Signals Panel */}
      {state && (
        <>
          <section className="live-feed-panel panel">
            <div className="section-heading">
              <div>
                <span className="eyebrow">LIVE ENVIRONMENTAL OBSERVATIONS</span>
                <h2>Public Hazard Feeds · {currentScopeTitle}</h2>
              </div>
              <button
                className="module-action"
                onClick={() =>
                  api.live.hazards(state, district || undefined).then(setLiveFeed).catch((e) => setError(e.message))
                }
              >
                Refresh Feeds
              </button>
            </div>

            <div className="live-kpi-row">
              <span>
                <b>{liveItems.length}</b>
                <small>live signals</small>
              </span>
              <span>
                <b>{liveItems.filter((h) => h.type.toLowerCase().includes("earthquake")).length}</b>
                <small>earthquakes (USGS)</small>
              </span>
              <span>
                <b>{liveItems.filter((h) => h.type.toLowerCase().includes("fire")).length}</b>
                <small>thermal anomalies (FIRMS)</small>
              </span>
              <span>
                <b>{critical}</b>
                <small>critical zones</small>
              </span>
              <span>
                <b>{high}</b>
                <small>high risk zones</small>
              </span>
            </div>

            <div className="live-source-row">
              {liveFeed.sources.map((s) => (
                <span key={s.name} className={s.status.includes("live") ? "source-live" : "source-muted"}>
                  <i />
                  {s.name} · {s.status}
                  {s.count != null ? ` · ${s.count} events` : ""}
                </span>
              ))}
              <span className="live-updated">
                Updated {liveFeed.updated_at ? new Date(liveFeed.updated_at).toLocaleTimeString() : "—"}
              </span>
            </div>

            <div className="live-event-grid">
              {liveItems.slice(0, 6).map((h) => (
                <article className={`live-event-card live-event-${h.severity.toLowerCase()}`} key={h.id}>
                  <div>
                    <span>{h.type}</span>
                    <b>{h.severity}</b>
                  </div>
                  <strong>{h.title || "Live hazard observation"}</strong>
                  <p>{h.detail || "Public real-time observation"}</p>
                  <small>
                    {h.lat != null && h.lng != null
                      ? `${h.lat.toFixed(3)}°, ${h.lng.toFixed(3)}° · `
                      : "Location from source feed · "}
                    {h.source}
                  </small>
                </article>
              ))}
              {!liveItems.length && (
                <div className="live-empty">No critical seismic or wildfire alerts currently detected in this area.</div>
              )}
            </div>
          </section>

          {/* Response Operations & Relocation Module */}
          <section className="dashboard-modules">
            <div className="section-heading">
              <div>
                <span className="eyebrow">DECISION SUPPORT & RELOCATION</span>
                <h2>Response Operations · {district || state}</h2>
              </div>
            </div>

            <div className="dashboard-inline-section">
              <div className="inline-title">
                <h3>Designated Safe Shelters</h3>
                <span>{safeSites.length} verified emergency sites</span>
              </div>
              <div className="safe-site-strip">
                {safeSites.slice(0, 5).map((s) => (
                  <article className="safe-site-card" key={s.id}>
                    <span className="safe-pill" style={{ background: "rgba(16, 185, 129, 0.18)", color: "#10b981", border: "1px solid #10b981" }}>
                      SAFE SHELTER
                    </span>
                    <strong>{s.name}</strong>
                    <small>
                      {s.district || district}, {s.state || state}
                    </small>
                    <span>
                      Available Capacity: <b>{fmt(s.available_capacity ?? s.capacity)}</b>
                    </span>
                    <span>{s.facilities?.slice(0, 3).join(" · ") || "Emergency relief facilities"}</span>
                  </article>
                ))}
                {!safeSites.length && (
                  <article className="safe-site-card">
                    <strong>No mapped safe shelter returned</strong>
                    <small>Check state emergency directory.</small>
                  </article>
                )}
              </div>
            </div>

            {priority && (
              <div className="dashboard-inline-section relocation-inline">
                <div className="inline-title">
                  <h3>Priority Evacuation Target</h3>
                  <span style={{ color: "var(--risk-critical)", fontWeight: "bold" }}>{priority.level} RISK ZONE</span>
                </div>
                <div className="priority-relocation">
                  <div>
                    <strong>{priority.name}</strong>
                    <span>
                      {priority.district || district}, {priority.state || state} · Population{" "}
                      {fmt(priority.population)} · Calculated Risk {priority.risk_score}/100
                    </span>
                  </div>
                  <button className="btn" onClick={() => navigate(`/relocation?village=${priority.id}`)}>
                    Calculate Relocation Plan & Road Route →
                  </button>
                </div>
              </div>
            )}

            <div className="operation-card-grid">
              <article className="operation-card alert-card">
                <span className="eyebrow">ACTIVE ALERTS</span>
                <h3>Incident Center</h3>
                <strong>{critical + high} critical / high alerts</strong>
                <p>Calculated multi-factor risk zones requiring operational attention.</p>
                {villages
                  .filter((v) => v.level === "CRITICAL" || v.level === "HIGH")
                  .slice(0, 3)
                  .map((v) => (
                    <div className="mini-row" key={v.id}>
                      <div>
                        <b style={{ color: v.level === "CRITICAL" ? "var(--risk-critical)" : "var(--risk-high)" }}>
                          {v.level}
                        </b>
                        <strong>{v.name}</strong>
                        <small>
                          {v.district} · Risk {v.risk_score}
                        </small>
                      </div>
                    </div>
                  ))}
              </article>

              <article className="operation-card">
                <span className="eyebrow">REGIONAL NEWS</span>
                <h3>{district || state} Disaster Headlines</h3>
                <strong>{news.length} articles</strong>
                <p>Publisher articles from Google News RSS for situational context.</p>
                {news.slice(0, 4).map((a, i) => (
                  <a className="news-row" href={a.url} target="_blank" rel="noreferrer" key={`${a.url}-${i}`}>
                    {a.title}
                  </a>
                ))}
              </article>

              <article className="operation-card">
                <span className="eyebrow">RISK AGGREGATION</span>
                <h3>Physical & Live Index</h3>
                <div className="mini-stat-grid">
                  <span>
                    <small>Locations</small>
                    <b>{villages.length}</b>
                  </span>
                  <span>
                    <small>Critical</small>
                    <b style={{ color: "var(--risk-critical)" }}>{critical}</b>
                  </span>
                  <span>
                    <small>High</small>
                    <b style={{ color: "var(--risk-high)" }}>{high}</b>
                  </span>
                  <span>
                    <small>Population</small>
                    <b>{knownPopulation ? knownPopulation.toLocaleString() : "—"}</b>
                  </span>
                </div>
                <p className="data-note">
                  Dynamic risk formula: Hazard (40%) + Physical Exposure (30%) + Demographic Vulnerability (30%).
                </p>
              </article>

              <article className="operation-card">
                <span className="eyebrow">GUIDED CORRIDOR</span>
                <h3>Evacuation & Road Route</h3>
                <p>
                  Generates OSRM driving routes with turn-by-turn road steps and Google Maps mobile hand-off for field vehicles.
                </p>
                <button
                  className="btn"
                  disabled={!priority}
                  onClick={() => priority && navigate(`/relocation?village=${priority.id}`)}
                >
                  Open Guided Evacuation
                </button>
              </article>
            </div>
          </section>

          {/* Historical Disaster Events Panel */}
          <RegionHistoryPanel region={state} district={district} />

          <div className="panel" style={{ marginTop: 16, padding: 14 }}>
            <button className="btn secondary" onClick={clearScope}>
              Reset Location Scope
            </button>
          </div>
        </>
      )}
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span>
      <i style={{ background: color }} />
      {label}
    </span>
  );
}
