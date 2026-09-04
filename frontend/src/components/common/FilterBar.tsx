interface FilterBarProps {
  districts: string[];
  district: string;
  setDistrict: (v: string) => void;
  level: string;
  setLevel: (v: string) => void;
}

const LEVELS = ["", "CRITICAL", "HIGH", "MODERATE", "LOW"];

function Select({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
}) {
  return (
    <label style={{ display: "flex", flexDirection: "column", gap: 4, fontSize: 12 }}>
      <span style={{ color: "var(--text-muted)", fontWeight: 600 }}>{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{
          background: "var(--bg-inset)",
          color: "var(--text-primary)",
          border: "1px solid var(--border-subtle)",
          borderRadius: 6,
          padding: "7px 10px",
          fontSize: 13,
          minWidth: 150,
        }}
      >
        <option value="">All</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function FilterBar({
  districts,
  district,
  setDistrict,
  level,
  setLevel,
}: FilterBarProps) {
  return (
    <div
      style={{
        display: "flex",
        gap: 16,
        padding: "12px 20px",
        borderBottom: "1px solid var(--border-subtle)",
        background: "var(--bg-panel)",
        flexWrap: "wrap",
      }}
    >
      <Select label="District" value={district} onChange={setDistrict} options={districts} />
      <Select
        label="Risk Level"
        value={level}
        onChange={setLevel}
        options={LEVELS.filter(Boolean)}
      />
    </div>
  );
}
