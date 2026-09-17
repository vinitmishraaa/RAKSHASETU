import { useEffect, useState } from "react";
import { api } from "../../services/api";

interface FilterBarProps {
  states: string[];
  state: string;
  setState: (v: string) => void;
  cities: string[];
  city: string;
  setCity: (v: string) => void;
  districts: string[];
  district: string;
  setDistrict: (v: string) => void;
}

function Select({ label, value, onChange, options, disabled = false, loading = false }: { label: string; value: string; onChange: (v: string) => void; options: string[]; disabled?: boolean; loading?: boolean }) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} disabled={disabled} onChange={(e) => onChange(e.target.value)}>
        <option value="">{loading ? "Loading…" : "Select"}</option>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );
}

export default function FilterBar({ states, state, setState, cities, city, setCity, districts, district, setDistrict }: FilterBarProps) {
  const [liveStates, setLiveStates] = useState<string[]>(states);
  const [liveCities, setLiveCities] = useState<string[]>(cities);
  const [liveDistricts, setLiveDistricts] = useState<string[]>(districts);
  const [loadingStates, setLoadingStates] = useState(false);
  const [loadingCities, setLoadingCities] = useState(false);
  const [loadingDistricts, setLoadingDistricts] = useState(false);

  useEffect(() => {
    let active = true;
    setLoadingStates(true);
    api.regions.states().then(rows => {
      if (active) setLiveStates(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b)));
    }).catch(() => { if (active) setLiveStates(states); }).finally(() => active && setLoadingStates(false));
    return () => { active = false; };
  }, [states]);

  useEffect(() => {
    let active = true;
    if (!state) { setLiveCities([]); return; }
    setLoadingCities(true);
    api.regions.cities(state).then(rows => {
      if (active) setLiveCities(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b)));
    }).catch(() => { if (active) setLiveCities(cities); }).finally(() => active && setLoadingCities(false));
    return () => { active = false; };
  }, [state, cities]);

  useEffect(() => {
    let active = true;
    if (!state || !city) { setLiveDistricts([]); return; }
    setLoadingDistricts(true);
    api.regions.districts(state, city).then(rows => {
      if (active) setLiveDistricts(rows.map(r => r.name).filter(Boolean).sort((a, b) => a.localeCompare(b)));
    }).catch(() => { if (active) setLiveDistricts(districts); }).finally(() => active && setLoadingDistricts(false));
    return () => { active = false; };
  }, [state, city, districts]);

  function changeState(value: string) {
    setState(value); setCity(""); setDistrict("");
    localStorage.setItem("rakshasetu_region", value);
    localStorage.removeItem("rakshasetu_city"); localStorage.removeItem("rakshasetu_district");
  }
  function changeCity(value: string) {
    setCity(value); setDistrict("");
    localStorage.setItem("rakshasetu_city", value); localStorage.removeItem("rakshasetu_district");
  }
  function changeDistrict(value: string) {
    setDistrict(value); localStorage.setItem("rakshasetu_district", value);
  }

  return (
    <div className="filter-bar">
      <div className="filter-title"><span className="eyebrow">GEOGRAPHIC SCOPE</span><strong>State / UT → City → District</strong></div>
      <Select label="State / Union Territory" value={state} onChange={changeState} options={liveStates} loading={loadingStates} />
      <Select label="City / Town" value={city} onChange={changeCity} options={liveCities} disabled={!state} loading={loadingCities} />
      <Select label="District" value={district} onChange={changeDistrict} options={liveDistricts} disabled={!city} loading={loadingDistricts} />
      {(state || city || district) && (
        <button className="filter-clear" onClick={() => { setState(""); setCity(""); setDistrict(""); localStorage.removeItem("rakshasetu_region"); localStorage.removeItem("rakshasetu_city"); localStorage.removeItem("rakshasetu_district"); }}>Clear</button>
      )}
    </div>
  );
}
