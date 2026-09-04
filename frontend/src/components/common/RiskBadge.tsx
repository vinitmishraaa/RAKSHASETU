import type { RiskLevel } from "../../types";

const COLORS: Record<string, string> = {
  CRITICAL: "var(--risk-critical)",
  HIGH: "var(--risk-high)",
  MODERATE: "var(--risk-moderate)",
  LOW: "var(--risk-low)",
};

export default function RiskBadge({ level }: { level: RiskLevel | string }) {
  const color = COLORS[level] || "var(--text-muted)";
  return (
    <span
      className="badge"
      style={{
        color,
        background: `${color}1a`,
        border: `1px solid ${color}55`,
      }}
    >
      <span
        style={{
          width: 6,
          height: 6,
          borderRadius: "50%",
          background: color,
          display: "inline-block",
        }}
      />
      {level}
    </span>
  );
}
