import { useEffect, useState } from "react";
import { api } from "../../services/api";

interface FilterBarProps {
  countries: string[];
  country: string;
  setCountry: (v: string) => void;
  states: string[];
  state: string;
  setState: (v: string) => void;
  districts: string[];
  district: string;
  setDistrict: (v: string) => void;
  level: string;
  setLevel: (v: string) => void;
}

const LEVELS = ["CRITICAL", "HIGH", "MODERATE", "LOW"];

function Select({ label, value, onChange, options, disabled = false, loading = false }: { label: string; value: string; onChange: (v: string) => void; options: string[]; disabled?: boolean; loading?: boolean }) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} disabled={disabled} onChange={(e) => onChange(e.target.value)}>
        <option value="">{loading ? "Loading…" : "All"}</option>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );
}

export default function FilterBar({ countries, country, setCountry, states, state, setState, districts, district, setDistrict, level, setLevel }: FilterBarProps) {
  const [liveStates, setLiveStates] = useState<string[]>(states);
  const [liveDistricts, setLiveDistricts] = useState<string[]>([]);
  const [loadingStates, setLoadingStates] = useState(true);
  const [loadingDistricts, setLoadingDistricts] = useState(false);

  useEffect(() => {
    let active = true;
    setLoadingStates(true);
    api.regions.states()
      .then(rows => { if (active) setLiveStates(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b))); })
      .catch(() => { if (active) setLiveStates(states); })
      .finally(() => { if (active) setLoadingStates(false); });
    return () => { active = false; };
  }, [states]);

  useEffect(() => {
    let active = true;
    if (!state) { setLiveDistricts([]); return; }
    setLoadingDistricts(true);
    api.regions.districts(state)
      .then(rows => { if (active) setLiveDistricts(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b))); })
      .catch(() => { if (active) setLiveDistricts(districts); })
      .finally(() => { if (active) setLoadingDistricts(false); });
    return () => { active = false; };
  }, [state, districts]);

  function changeState(value: string) {
    setDistrict("");
    setState(value);
    localStorage.setItem("rakshasetu_region", value || "India");
    localStorage.removeItem("rakshasetu_district");
  }

  function changeDistrict(value: string) {
    setDistrict(value);
    localStorage.setItem("rakshasetu_district", value);
  }

  return (
    <div className="filter-bar">
      <div className="filter-title"><span className="eyebrow">GEOGRAPHIC SCOPE</span><strong>Country → State → District</strong></div>
      <Select label="Country" value={country} onChange={setCountry} options={countries} />
      <Select label="State / Union Territory" value={state} onChange={changeState} options={liveStates} disabled={!country} loading={loadingStates} />
      <Select label="District" value={district} onChange={changeDistrict} options={liveDistricts} disabled={!state} loading={loadingDistricts} />
      <Select label="Risk Level" value={level} onChange={setLevel} options={LEVELS} />
      {(country || state || district || level) && (
        <button className="filter-clear" onClick={() => { setCountry(""); setState(""); setDistrict(""); setLevel(""); localStorage.removeItem("rakshasetu_region"); localStorage.removeItem("rakshasetu_district"); }}>Clear filters</button>
      )}
    </div>
  );
}
