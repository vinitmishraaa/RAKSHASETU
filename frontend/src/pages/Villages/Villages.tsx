import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import RiskBadge from "../../components/common/RiskBadge";
import { api } from "../../services/api";
import type { Village } from "../../types";

export default function Villages() {
  const [villages, setVillages] = useState<Village[]>([]);
  const [states, setStates] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [params] = useSearchParams();
  const [state, setState] = useState(() => {
    return params.get("region") || localStorage.getItem("rakshasetu_region") || "West Bengal";
  });
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
    api.villages
      .list({ state: state || undefined })
      .then(setVillages)
      .catch(() => setVillages([]))
      .finally(() => setLoading(false));
  }, [state]);

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim();
    return villages
      .filter((v) => {
        if (!q) return true;
        const text = `${v.name} ${v.district || ""} ${v.state || ""}`.toLowerCase();
        return text.includes(q);
      })
      .sort((a, b) => b.risk_score - a.risk_score);
  }, [villages, search]);

  function changeState(v: string) {
    setState(v);
    if (v) localStorage.setItem("rakshasetu_region", v);
    else localStorage.removeItem("rakshasetu_region");
  }

  return (
    <div className="villages-page">
      <div className="villages-header">
        <div>
          <span className="eyebrow">FIELD LOCATIONS · INDIA</span>
          <h2>Monitored Settlements & Villages</h2>
          <p>{state ? `${state} monitored locations` : "National monitored settlements"}</p>
        </div>
        <div className="village-filters">
          <select value={state} onChange={(e) => changeState(e.target.value)} aria-label="State">
            <option value="">All States / UTs</option>
            {states.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search village, district…"
          />
        </div>
      </div>

      {loading && <div style={{ padding: 20, color: "var(--text-muted)" }}>Loading settlements…</div>}

      <div className="village-grid">
        {filtered.map((v) => (
          <article className="village-card" key={v.id}>
            <div className="village-card-top">
              <span className="village-index">MONITORED ZONE</span>
              <RiskBadge level={v.level} />
            </div>
            <h3>{v.name}</h3>
            <p>
              {v.district || "District unmapped"}, {v.state || state}
            </p>
            <div className="village-metrics">
              <span>
                <small>Population</small>
                <b>{v.population != null ? v.population.toLocaleString() : "Not published"}</b>
              </span>
              <span>
                <small>Risk</small>
                <b>{v.risk_score}/100</b>
              </span>
            </div>
            <button className="btn" onClick={() => window.location.assign(`/?village=${v.id}`)}>
              View on command center
            </button>
          </article>
        ))}
      </div>

      {!filtered.length && !loading && (
        <div className="panel village-empty">No monitored villages match this state / search filter.</div>
      )}
    </div>
  );
}
