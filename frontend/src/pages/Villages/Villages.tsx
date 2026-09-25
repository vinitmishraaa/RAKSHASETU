import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import RiskBadge from "../../components/common/RiskBadge";
import { api } from "../../services/api";
import type { Village } from "../../types";

export default function Villages() {
  const [villages, setVillages] = useState<Village[]>([]);
  const [states, setStates] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [tierFilter, setTierFilter] = useState("");
  const [redZoneOnly, setRedZoneOnly] = useState(false);
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
        if (redZoneOnly && !v.is_red_zone) return false;
        if (tierFilter && v.relocation_tier !== tierFilter) return false;
        if (!q) return true;
        const text = `${v.name} ${v.district || ""} ${v.state || ""}`.toLowerCase();
        return text.includes(q);
      })
      .sort((a, b) => b.risk_score - a.risk_score);
  }, [villages, search, tierFilter, redZoneOnly]);

  function changeState(v: string) {
    setState(v);
    if (v) localStorage.setItem("rakshasetu_region", v);
    else localStorage.removeItem("rakshasetu_region");
  }

  function exportCSV() {
    if (!filtered.length) return;
    const headers = [
      "ID",
      "Settlement Name",
      "District",
      "State",
      "Latitude",
      "Longitude",
      "Population",
      "Risk Score (0-100)",
      "Risk Level",
      "Red Zone Status",
      "Relocation Priority Tier",
      "Relocation Horizon",
      "Primary Trigger Hazard",
    ];
    const rows = filtered.map((v) => [
      `"${v.id}"`,
      `"${v.name}"`,
      `"${v.district || ""}"`,
      `"${v.state || state}"`,
      v.lat,
      v.lng,
      v.population ?? "",
      v.risk_score,
      v.level,
      v.is_red_zone ? "RED ZONE (UNSUITABLE FOR HABITATION)" : "SAFE / REGULAR",
      v.relocation_tier || "MEDIUM_TERM",
      `"${v.relocation_horizon || (v.level === "CRITICAL" ? "0–48 Hours" : "1–3 Months")}"`,
      `"${v.primary_hazard_trigger || "Multi-Hazard Confluence"}"`,
    ]);
    const csvContent = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `SDMA_Relocation_Registry_${(state || "All_India").replace(/\s+/g, "_")}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  return (
    <div className="villages-page">
      <div className="villages-header">
        <div>
          <span className="eyebrow">NATIONAL DISASTER MANAGEMENT REGISTRY · FIELD HABITATIONS</span>
          <h2>Monitored Settlements & Red Zones</h2>
          <p>{state ? `${state} monitored habitations` : "National monitored habitations"}</p>
        </div>
        <div className="village-filters" style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
          <select value={state} onChange={(e) => changeState(e.target.value)} aria-label="State">
            <option value="">All States / UTs</option>
            {states.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <select
            value={tierFilter}
            onChange={(e) => setTierFilter(e.target.value)}
            style={{ fontWeight: tierFilter ? 700 : "normal" }}
          >
            <option value="">All Relocation Tiers</option>
            <option value="IMMEDIATE">🔴 Immediate (0–48h)</option>
            <option value="SHORT_TERM">🟠 Short-Term (1–3m)</option>
            <option value="MEDIUM_TERM">🟡 Medium-Term (6–12m)</option>
          </select>
          <button
            type="button"
            onClick={() => setRedZoneOnly(!redZoneOnly)}
            style={{
              padding: "7px 10px",
              borderRadius: 6,
              fontSize: 11,
              fontWeight: 800,
              cursor: "pointer",
              border: "1px solid rgba(255, 68, 102, 0.4)",
              background: redZoneOnly ? "#e5484d" : "rgba(255, 68, 102, 0.15)",
              color: redZoneOnly ? "#ffffff" : "#ff4466",
            }}
          >
            ⚠️ Red Zones {redZoneOnly ? "✓" : ""}
          </button>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search habitation, district…"
            style={{ minWidth: 160 }}
          />
          <button
            type="button"
            className="btn secondary"
            onClick={exportCSV}
            style={{ fontSize: 11, padding: "7px 12px", display: "inline-flex", alignItems: "center", gap: 6 }}
            title="Download complete habitation assessment spreadsheet for SDMA / DDMA planning"
          >
            📥 Export SDMA CSV
          </button>
        </div>
      </div>

      {loading && <div style={{ padding: 20, color: "var(--text-muted)" }}>Loading settlements…</div>}

      <div className="village-grid">
        {filtered.map((v) => (
          <article className="village-card" key={v.id} style={v.is_red_zone ? { borderLeft: "3px solid #ff4466" } : undefined}>
            <div className="village-card-top">
              <span className="village-index" style={v.is_red_zone ? { color: "#ff4466", fontWeight: 800 } : undefined}>
                {v.is_red_zone ? "⚠️ RED ZONE" : "MONITORED HABITATION"}
              </span>
              <RiskBadge level={v.level} />
            </div>

            {v.is_red_zone && (
              <div style={{ color: "#ff8095", fontSize: 9, fontWeight: 800, margin: "2px 0 4px" }}>
                UNSUITABLE FOR PERMANENT HABITATION
              </div>
            )}

            <h3>{v.name}</h3>
            <p>
              {v.district || "District unmapped"}, {v.state || state}
            </p>

            <div style={{ display: "flex", gap: 6, margin: "6px 0", flexWrap: "wrap", alignItems: "center" }}>
              <span
                style={{
                  fontSize: 9,
                  fontWeight: 800,
                  padding: "2px 6px",
                  borderRadius: 4,
                  background:
                    v.relocation_tier === "IMMEDIATE"
                      ? "rgba(229,72,77,0.15)"
                      : v.relocation_tier === "SHORT_TERM"
                      ? "rgba(245,158,11,0.15)"
                      : "rgba(16,185,129,0.15)",
                  color:
                    v.relocation_tier === "IMMEDIATE"
                      ? "#ff8095"
                      : v.relocation_tier === "SHORT_TERM"
                      ? "#f59e0b"
                      : "#10b981",
                }}
              >
                {v.relocation_horizon || (v.level === "CRITICAL" ? "0–48 Hours" : "1–3 Months")}
              </span>
              {v.primary_hazard_trigger && (
                <span style={{ fontSize: 9, color: "var(--text-secondary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 190 }} title={v.primary_hazard_trigger}>
                  Trigger: {v.primary_hazard_trigger}
                </span>
              )}
            </div>

            <div className="village-metrics">
              <span>
                <small>Population</small>
                <b>{v.population != null ? v.population.toLocaleString() : "Not published"}</b>
              </span>
              <span>
                <small>Risk Score</small>
                <b>{v.risk_score}/100</b>
              </span>
            </div>
            <button className="btn" onClick={() => window.location.assign(`/?village=${v.id}`)}>
              View on Command Center
            </button>
          </article>
        ))}
      </div>

      {!filtered.length && !loading && (
        <div className="panel village-empty">No habitations match this filter criteria.</div>
      )}
    </div>
  );
}
