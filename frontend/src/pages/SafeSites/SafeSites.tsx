import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import type { SafeSite } from "../../types";

const value = (v: number | null | undefined) => (v == null ? "Not published" : v.toLocaleString());

export default function SafeSites() {
  const [sites, setSites] = useState<SafeSite[]>([]);
  const [states, setStates] = useState<string[]>([]);
  const [state, setState] = useState(() => localStorage.getItem("rakshasetu_region") || "West Bengal");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.regions
      .states()
      .then((rows) => {
        const names = rows.map((r) => r.name).filter(Boolean).sort();
        setStates(names);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    api.safeSites
      .list({ state: state || undefined })
      .then(setSites)
      .catch(() => setSites([]))
      .finally(() => setLoading(false));
  }, [state]);

  const visibleSites = useMemo(() => sites, [sites]);

  const knownCapacity = visibleSites
    .filter((s) => s.capacity != null)
    .reduce((n, s) => n + (s.capacity || 0), 0);

  const knownAvailable = visibleSites
    .filter((s) => s.available_capacity != null)
    .reduce((n, s) => n + (s.available_capacity || 0), 0);

  function changeState(v: string) {
    setState(v);
    if (v) localStorage.setItem("rakshasetu_region", v);
    else localStorage.removeItem("rakshasetu_region");
  }

  return (
    <div className="page-shell">
      <div className="page-hero">
        <div>
          <span className="eyebrow">MAPPED EMERGENCY SHELTER INFRASTRUCTURE</span>
          <h2>Relocation Centres & Safe Shelters</h2>
          <p>
            Real shelter locations mapped from open geospatial sources. Operational capacity and verified status are displayed transparently.
          </p>
        </div>
        <select value={state} onChange={(e) => changeState(e.target.value)}>
          <option value="">All States / UTs</option>
          {states.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
      </div>

      <div className="alert-summary-strip">
        <span>
          <b>{visibleSites.length}</b>
          <small>mapped shelters</small>
        </span>
        <span>
          <b>{knownCapacity ? knownCapacity.toLocaleString() : "—"}</b>
          <small>total capacity</small>
        </span>
        <span>
          <b>{knownAvailable ? knownAvailable.toLocaleString() : "—"}</b>
          <small>available capacity</small>
        </span>
        <span>
          <b>OSM</b>
          <small>open data</small>
        </span>
      </div>

      {loading && <div style={{ padding: 20, color: "var(--text-muted)" }}>Loading shelters…</div>}

      <div className="safe-site-page-grid">
        {visibleSites.map((s) => (
          <article className="safe-site-detail-card" key={s.id}>
            <div className="safe-site-detail-head">
              <div>
                <span className="safe-pill">MAPPED SHELTER</span>
                <h3>{s.name}</h3>
                <small>
                  {s.district || s.state || s.region || state} · {s.lat.toFixed(4)}, {s.lng.toFixed(4)}
                </small>
              </div>
              <strong>
                {value(s.available_capacity)}
                <small> availability</small>
              </strong>
            </div>

            <div className="safe-metric-grid">
              <span>
                <small>Capacity</small>
                <b>{value(s.capacity)}</b>
              </span>
              <span>
                <small>Occupancy</small>
                <b>{value(s.current_occupancy)}</b>
              </span>
              <span>
                <small>Hazard clearance</small>
                <b>{value(s.hazard_risk)}</b>
              </span>
              <span>
                <small>Infrastructure</small>
                <b>{value(s.infrastructure_score)}</b>
              </span>
            </div>

            <div className="safe-facilities">
              {s.facilities && s.facilities.length > 0 ? (
                s.facilities.map((f) => <span key={f}>{f}</span>)
              ) : (
                <span>Standard emergency shelter facilities</span>
              )}
            </div>

            <div style={{ marginTop: 10, fontSize: 9, color: "var(--text-muted)" }}>
              {s.note || "Mapped operational disaster shelter."}{" "}
              {s.source_url && (
                <a href={s.source_url} target="_blank" rel="noreferrer">
                  OpenStreetMap source
                </a>
              )}
            </div>
          </article>
        ))}

        {!visibleSites.length && !loading && (
          <div className="panel empty-state">No mapped emergency shelters found in {state || "the selected scope"}.</div>
        )}
      </div>
    </div>
  );
}
