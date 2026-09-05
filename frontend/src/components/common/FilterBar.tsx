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

function Select({ label, value, onChange, options, disabled = false }: { label: string; value: string; onChange: (v: string) => void; options: string[]; disabled?: boolean }) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} disabled={disabled} onChange={(e) => onChange(e.target.value)}>
        <option value="">All</option>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );
}

export default function FilterBar({ countries, country, setCountry, states, state, setState, districts, district, setDistrict, level, setLevel }: FilterBarProps) {
  return (
    <div className="filter-bar">
      <div className="filter-title"><span className="eyebrow">GEOGRAPHIC SCOPE</span><strong>Country → State → District</strong></div>
      <Select label="Country" value={country} onChange={setCountry} options={countries} />
      <Select label="State / Province" value={state} onChange={setState} options={states} disabled={!country} />
      <Select label="District" value={district} onChange={setDistrict} options={districts} disabled={!state} />
      <Select label="Risk Level" value={level} onChange={setLevel} options={LEVELS} />
      {(country || state || district || level) && (
        <button className="filter-clear" onClick={() => { setCountry(""); setState(""); setDistrict(""); setLevel(""); }}>Clear filters</button>
      )}
    </div>
  );
}
