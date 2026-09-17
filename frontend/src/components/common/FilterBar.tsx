import { useEffect, useState } from "react";

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

function Select({ label, value, onChange, options, disabled, loading }: { label: string; value: string; onChange: (v: string) => void; options: string[]; disabled?: boolean; loading?: boolean }) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} disabled={disabled} onChange={e => onChange(e.target.value)}>
        <option value="">{loading ? "Loading…" : "Select"}</option>
        {options.map(x => <option key={x} value={x}>{x}</option>)}
      </select>
    </label>
  );
}

export default function FilterBar({ states, state, setState, districts, district, setDistrict, cities, city, setCity, loading }: Props) {
  function stateChange(v: string) {
    setState(v);
    setDistrict("");
    setCity("");
    localStorage.setItem("rakshasetu_region", v);
    localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  function districtChange(v: string) {
    setDistrict(v);
    setCity("");
    localStorage.setItem("rakshasetu_district", v);
    localStorage.removeItem("rakshasetu_city");
  }

  function cityChange(v: string) {
    setCity(v);
    localStorage.setItem("rakshasetu_city", v);
  }

  function clear() {
    setState("");
    setDistrict("");
    setCity("");
    localStorage.removeItem("rakshasetu_region");
    localStorage.removeItem("rakshasetu_district");
    localStorage.removeItem("rakshasetu_city");
  }

  return (
    <div className="filter-bar">
      <div className="filter-title">
        <span className="eyebrow">GEOGRAPHIC SCOPE</span>
        <strong>State / UT → District → City / Town</strong>
      </div>
      <Select label="State / Union Territory" value={state} onChange={stateChange} options={states} loading={loading && !state} />
      <Select label="District" value={district} onChange={districtChange} options={districts} disabled={!state} loading={loading && !!state && !district} />
      <Select label="City / Town" value={city} onChange={cityChange} options={cities} disabled={!district} loading={loading && !!district && !city} />
      {(state || district || city) && <button className="filter-clear" onClick={clear}>Clear</button>}
    </div>
  );
}
