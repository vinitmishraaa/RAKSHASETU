import { useEffect, useMemo, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { api } from "../../services/api";
import type { Village } from "../../types";

const LEVEL_COLORS: Record<string, string> = {
  CRITICAL: "#e5484d",
  HIGH: "#f2994a",
  MODERATE: "#f5c94a",
  LOW: "#3fb27f",
};

const n = (v: unknown) => (typeof v === "number" && Number.isFinite(v) ? v : 0);

export default function Analytics() {
  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [cities, setCities] = useState<string[]>([]);

  const [state, setState] = useState(() => localStorage.getItem("rakshasetu_region") || "West Bengal");
  const [district, setDistrict] = useState(() => localStorage.getItem("rakshasetu_district") || "");
  const [city, setCity] = useState(() => localStorage.getItem("rakshasetu_city") || "");

  const [villages, setVillages] = useState<Village[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // 1. Fetch States on Mount
  useEffect(() => {
    api.regions
      .states()
      .then((rows) => {
        const names = rows.map((x) => x.name).filter(Boolean).sort();
        setStates(names);
        const saved = localStorage.getItem("rakshasetu_region") || "West Bengal";
        if (saved && names.includes(saved)) {
          setState(saved);
        }
      })
      .catch((e) => setError(e.message));
  }, []);

  // 2. Cascade: When State changes, fetch official Districts of that state
  useEffect(() => {
    if (!state) {
      setDistricts([]);
      setDistrict("");
      setCities([]);
      setCity("");
      return;
    }
    api.regions
      .districts(state)
      .then((rows) => {
        const names = rows.map((x) => x.name).filter(Boolean).sort();
        setDistricts(names);
        const savedDistrict = localStorage.getItem("rakshasetu_district") || "";
        if (savedDistrict && names.includes(savedDistrict)) {
          setDistrict(savedDistrict);
        } else {
          setDistrict("");
          setCity("");
        }
      })
      .catch((e) => setError(e.message));
  }, [state]);

  // 3. Cascade: When District changes, fetch prominent Cities/Towns of that district
  useEffect(() => {
    if (!state || !district) {
      setCities([]);
      setCity("");
      return;
    }
    api.regions
      .cities(state, district)
      .then((rows) => {
        const names = rows.map((x) => x.name).filter(Boolean).sort();
        setCities(names);
        const savedCity = localStorage.getItem("rakshasetu_city") || "";
        if (savedCity && names.includes(savedCity)) {
          setCity(savedCity);
        } else {
          setCity("");
        }
      })
      .catch((e) => setError(e.message));
  }, [state, district]);

  // 4. Load Operational Settlements Data Immediately on State Selection (refining on District/City)
  useEffect(() => {
    if (!state) {
      setVillages([]);
      return;
    }
    setLoading(true);
    setError("");

    api.villages
      .list({ state, district: district || undefined, city: city || undefined })
      .then((vList) => setVillages(vList))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [state, district, city]);

  function handleStateChange(v: string) {
    setState(v);
    setDistrict("");
    setCity("");
    if (v) localStorage.setItem("rakshasetu_region", v);
    else localStorage.removeItem("rakshasetu_region");
    localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  function handleDistrictChange(v: string) {
    setDistrict(v);
    setCity("");
    if (v) localStorage.setItem("rakshasetu_district", v);
    else localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  function handleCityChange(v: string) {
    setCity(v);
    if (v) localStorage.setItem("rakshasetu_city", v);
    else localStorage.removeItem("rakshasetu_city");
  }

  const counts = useMemo(
    () => ({
      CRITICAL: villages.filter((v) => v.level === "CRITICAL").length,
      HIGH: villages.filter((v) => v.level === "HIGH").length,
      MODERATE: villages.filter((v) => v.level === "MODERATE").length,
      LOW: villages.filter((v) => v.level === "LOW").length,
    }),
    [villages]
  );

  const populationAtRisk = useMemo(
    () =>
      villages
        .filter((v) => v.level === "CRITICAL" || v.level === "HIGH")
        .reduce((s, v) => s + n(v.population), 0),
    [villages]
  );

  const barData = useMemo(
    () =>
      villages.slice(0, 30).map((v) => ({
        name: v.name,
        risk_score: n(v.risk_score),
        level: v.level,
      })),
    [villages]
  );

  const pieData = useMemo(
    () => Object.entries(counts).map(([name, value]) => ({ name, value })),
    [counts]
  );

  const scopeLabel = useMemo(() => {
    const parts = [city, district, state].filter(Boolean);
    return parts.length > 0 ? parts.join(", ") : "National scope";
  }, [city, district, state]);

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <div className="section-heading">
        <div>
          <span className="eyebrow">DECISION INTELLIGENCE & STATISTICAL PROFILING</span>
          <h2>Live Risk Analytics</h2>
        </div>

        {/* Strict State → District → City hierarchy */}
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
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

          <select
            value={city}
            onChange={(e) => handleCityChange(e.target.value)}
            disabled={!district || cities.length === 0}
            className="analytics-region-select"
          >
            <option value="">All Cities / Towns {cities.length > 0 ? `(${cities.length})` : ""}</option>
            {cities.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="panel" style={{ padding: 16, marginBottom: 16 }}>
          {error}
        </div>
      )}

      {!state && (
        <div className="panel" style={{ padding: 24 }}>
          Please select a State or Union Territory above. Analytics immediately load for the entire state, and can be refined to any specific district or city.
        </div>
      )}

      {loading && (
        <div style={{ padding: 24, color: "var(--text-muted)" }}>
          Loading live risk metrics for {scopeLabel}…
        </div>
      )}

      {state && !loading && (
        <>
          <div className="analytics-kpis">
            <Kpi label="MONITORED SETTLEMENTS" value={villages.length} />
            <Kpi label="POPULATION AT CRITICAL / HIGH RISK" value={populationAtRisk.toLocaleString()} />
            <Kpi label="CRITICAL ZONES" value={counts.CRITICAL} />
            <Kpi label="ACTIVE GEOGRAPHIC SCOPE" value={scopeLabel} />
          </div>

          <div className="analytics-grid">
            <div className="panel" style={{ padding: 20 }}>
              <h4 className="panel-label">RISK SCORE BY SETTLEMENT (TOP 30)</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={barData}>
                  <CartesianGrid stroke="var(--border-subtle)" strokeDasharray="3 3" vertical={false} />
                  <XAxis
                    dataKey="name"
                    stroke="var(--text-muted)"
                    fontSize={9}
                    tickLine={false}
                    axisLine={false}
                    interval={2}
                  />
                  <YAxis domain={[0, 100]} stroke="var(--text-muted)" fontSize={10} />
                  <Tooltip />
                  <Bar dataKey="risk_score" radius={[4, 4, 0, 0]}>
                    {barData.map((v, i) => (
                      <Cell key={i} fill={LEVEL_COLORS[v.level] || "#f5c94a"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="panel" style={{ padding: 20 }}>
              <h4 className="panel-label">RISK LEVEL DISTRIBUTION</h4>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={58}
                    outerRadius={96}
                    paddingAngle={3}
                  >
                    {pieData.map((d) => (
                      <Cell key={d.name} fill={LEVEL_COLORS[d.name] || "#f5c94a"} />
                    ))}
                  </Pie>
                  <Legend />
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="analytics-section">
            <div className="panel" style={{ padding: 20 }}>
              <h4 className="panel-label">DISASTER IMPACT PROFILE & METHODOLOGY</h4>
              <div className="analytics-stat-row">
                <span>
                  <small>Population at risk</small>
                  <b>{populationAtRisk.toLocaleString()}</b>
                </span>
                <span>
                  <small>Critical zone share</small>
                  <b>{villages.length ? Math.round((counts.CRITICAL * 100) / villages.length) : 0}%</b>
                </span>
                <span>
                  <small>Data latency</small>
                  <b>Real-time stream</b>
                </span>
              </div>
              <p className="data-note">
                Risk values are computed dynamically from live Open-Meteo precipitation/wind gusts, USGS seismic hypocenter distance and magnitude, and local topographical hazard weights. They serve as actionable decision-support indicators for emergency response teams.
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function Kpi({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="panel analytics-kpi">
      <span>{label}</span>
      <strong className="mono">{value}</strong>
    </div>
  );
}
