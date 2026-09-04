interface FilterBarProps {
  regions: string[];
  region: string;
  setRegion: (v: string) => void;
  districts: string[];
  district: string;
  setDistrict: (v: string) => void;
  level: string;
  setLevel: (v: string) => void;
}

const LEVELS = ["CRITICAL", "HIGH", "MODERATE", "LOW"];

function Select({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: string[] }) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">All</option>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </label>
  );
}

export default function FilterBar({ regions, region, setRegion, districts, district, setDistrict, level, setLevel }: FilterBarProps) {
  return (
    <div className="filter-bar">
      <div className="filter-title"><span className="eyebrow">FILTERS</span><strong>Regional Scope</strong></div>
      <Select label="Region / State" value={region} onChange={setRegion} options={regions} />
      <Select label="District" value={district} onChange={setDistrict} options={districts} />
      <Select label="Risk Level" value={level} onChange={setLevel} options={LEVELS} />
      {(region || district || level) && (
        <button className="filter-clear" onClick={() => { setRegion(""); setDistrict(""); setLevel(""); }}>Clear filters</button>
      )}
    </div>
  );
}
