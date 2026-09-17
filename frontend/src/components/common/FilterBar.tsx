import { useState, useMemo } from "react";

interface Props {
  states: string[];
  state: string;
  setState: (v: string) => void;
  districts: string[];
  district: string;
  setDistrict: (v: string) => void;
  cities: string[];
  city: string;
  setCity: (v: string) => void;
  loading?: boolean;
}

export default function FilterBar({
  states,
  state,
  setState,
  districts,
  district,
  setDistrict,
  cities,
  city,
  setCity,
  loading,
}: Props) {
  const [citySearch, setCitySearch] = useState("");

  function stateChange(v: string) {
    setState(v);
    setDistrict("");
    setCity("");
    setCitySearch("");
    if (v) {
      localStorage.setItem("rakshasetu_region", v);
    } else {
      localStorage.removeItem("rakshasetu_region");
    }
    localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  function districtChange(v: string) {
    setDistrict(v);
    setCity("");
    setCitySearch("");
    if (v) {
      localStorage.setItem("rakshasetu_district", v);
    } else {
      localStorage.removeItem("rakshasetu_district");
    }
    localStorage.removeItem("rakshasetu_city");
  }

  function cityChange(v: string) {
    setCity(v);
    setCitySearch(v);
    if (v) {
      localStorage.setItem("rakshasetu_city", v);
    } else {
      localStorage.removeItem("rakshasetu_city");
    }
  }

  function clear() {
    setState("");
    setDistrict("");
    setCity("");
    setCitySearch("");
    localStorage.removeItem("rakshasetu_region");
    localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  const filteredCities = useMemo(() => {
    if (!citySearch) return cities;
    return cities.filter((c) => c.toLowerCase().includes(citySearch.toLowerCase()));
  }, [cities, citySearch]);

  return (
    <div className="filter-bar">
      <div className="filter-title">
        <span className="eyebrow">GEOGRAPHIC SCOPE</span>
        <strong>State / UT → District → City / Town</strong>
      </div>

      {/* 1. State / UT Selection */}
      <label className="filter-field">
        <span>1. State / Union Territory</span>
        <select value={state} onChange={(e) => stateChange(e.target.value)}>
          <option value="">{loading && !state ? "Loading states…" : "-- Select State / UT --"}</option>
          {states.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </label>

      {/* 2. District Selection (Strictly for this state only) */}
      <label className="filter-field">
        <span>2. District {state ? `(${districts.length} official)` : ""}</span>
        <select value={district} disabled={!state} onChange={(e) => districtChange(e.target.value)}>
          <option value="">{state ? `-- All ${districts.length} districts in ${state} --` : "Select state first"}</option>
          {districts.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </label>

      {/* 3. City / Town Selection & Search (Optional) */}
      <div className="filter-field city-filter-group" style={{ position: "relative" }}>
        <span>3. City / Town <small style={{ color: "var(--text-muted)", fontWeight: "normal" }}>(Optional)</small></span>
        <div style={{ display: "flex", gap: "6px" }}>
          <select
            value={city}
            disabled={!district}
            onChange={(e) => cityChange(e.target.value)}
            style={{ flex: 1 }}
          >
            <option value="">{district ? `-- All cities/towns in ${district} --` : "Select district first"}</option>
            {filteredCities.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          {district && cities.length > 0 && (
            <input
              type="text"
              placeholder="Search city…"
              value={citySearch}
              onChange={(e) => setCitySearch(e.target.value)}
              className="city-search-input"
              style={{
                width: "120px",
                padding: "6px 8px",
                fontSize: "12px",
                borderRadius: "6px",
                border: "1px solid var(--border-subtle)",
                background: "var(--bg-elevated)",
                color: "var(--text-primary)",
              }}
              title="Type here to search for a specific city in this district"
            />
          )}
        </div>
      </div>

      {(state || district || city) && (
        <button className="filter-clear" onClick={clear} title="Reset location filters">
          Reset
        </button>
      )}
    </div>
  );
}
