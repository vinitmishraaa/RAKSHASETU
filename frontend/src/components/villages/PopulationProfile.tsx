import type { VillageDetail } from "../../types";

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div>
      <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 4 }}>{label}</div>
      <div className="mono" style={{ fontSize: 22, fontWeight: 700 }}>
        {typeof value === "number" ? value.toLocaleString() : value}
      </div>
    </div>
  );
}

export default function PopulationProfile({ village }: { village: VillageDetail }) {
  return (
    <div className="panel" style={{ padding: 20 }}>
      <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
        POPULATION PROFILE
      </h4>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: 20 }}>
        <Stat label="Total population" value={village.population} />
        <Stat label="Households" value={village.households} />
        <Stat label="Children" value={village.children} />
        <Stat label="Elderly" value={village.elderly} />
        <Stat label="Other vulnerable" value={village.other_vulnerable} />
      </div>
    </div>
  );
}
