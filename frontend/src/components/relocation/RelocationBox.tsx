import type { RelocationPlan } from "../../types";

export default function RelocationBox({
  plan,
  onViewRoute,
}: {
  plan: RelocationPlan;
  onViewRoute?: (siteId: string) => void;
}) {
  const best = plan.best_site;

  return (
    <div className="panel" style={{ padding: 20 }}>
      <h4 style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 4 }}>
        RELOCATION RECOMMENDATION
      </h4>
      <div style={{ fontSize: 15, fontWeight: 700, marginBottom: 2 }}>{plan.village_name}</div>
      <div className="mono" style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 16 }}>
        Population: {plan.population.toLocaleString()}
      </div>

      {best && (
        <div
          style={{
            background: "var(--bg-inset)",
            border: "1px solid var(--border-subtle)",
            borderRadius: 10,
            padding: 16,
            marginBottom: plan.allocations.length > 1 ? 16 : 0,
          }}
        >
          <div style={{ fontSize: 11, color: "var(--brand)", fontWeight: 700, marginBottom: 6 }}>
            BEST SITE
          </div>
          <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>{best.site_name}</div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 14 }}>
            <Field label="Suitability" value={`${best.suitability}/100`} />
            <Field label="Available capacity" value={best.available_capacity.toLocaleString()} />
            <Field label="Distance" value={`${best.distance_km} km`} />
            <Field label="Road access" value={best.road_access} />
          </div>

          <button className="btn btn-primary" style={{ width: "100%" }} onClick={() => onViewRoute?.(best.site_id)}>
            View Route
          </button>
        </div>
      )}

      {plan.allocations.length > 1 && (
        <div>
          <div style={{ fontSize: 11, color: "var(--text-muted)", fontWeight: 700, marginBottom: 8 }}>
            RELOCATION PLAN (SPLIT ALLOCATION)
          </div>
          {plan.allocations.map((a) => (
            <div
              key={a.site_id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: 13,
                padding: "8px 0",
                borderBottom: "1px solid var(--border-subtle)",
              }}
            >
              <span>{a.site_name}</span>
              <span className="mono">{a.people.toLocaleString()} people</span>
            </div>
          ))}
          {plan.reason && (
            <p style={{ fontSize: 12, marginTop: 10, color: "var(--risk-high)" }}>
              Reason: {plan.reason}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div style={{ fontSize: 10.5, color: "var(--text-muted)" }}>{label}</div>
      <div className="mono" style={{ fontSize: 13.5, fontWeight: 600 }}>{value}</div>
    </div>
  );
}
