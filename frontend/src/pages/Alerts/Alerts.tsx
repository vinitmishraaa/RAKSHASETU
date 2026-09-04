import { useEffect, useState } from "react";
import { api } from "../../services/api";
import type { Alert } from "../../types";
import AlertsSummary from "../../components/alerts/AlertsSummary";

const LEVEL_STYLE: Record<string, { icon: string; color: string }> = {
  CRITICAL: { icon: "🔴", color: "var(--risk-critical)" },
  HIGH: { icon: "🟠", color: "var(--risk-high)" },
  WARNING: { icon: "🟡", color: "var(--risk-moderate)" },
};

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    api.alerts.list().then(setAlerts);
  }, []);

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1, display: "flex", gap: 20 }}>
      <div style={{ flex: 1 }}>
        <h2 style={{ fontSize: 20, marginBottom: 4 }}>Alerts &amp; Escalation</h2>
        <p style={{ marginBottom: 20 }}>
          Auto-generated from live risk classification and relocation capacity checks.
          SMS / WhatsApp / voice-siren dispatch is a later-phase integration —
          see README for the SMS_API_KEY placeholder.
        </p>

        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {alerts.length === 0 && <p>No active alerts.</p>}
          {alerts.map((a, i) => {
            const style = LEVEL_STYLE[a.level] || LEVEL_STYLE.WARNING;
            return (
              <div
                key={i}
                className="panel"
                style={{
                  padding: 16,
                  display: "flex",
                  gap: 14,
                  alignItems: "flex-start",
                  borderLeft: `3px solid ${style.color}`,
                }}
              >
                <span style={{ fontSize: 18 }}>{style.icon}</span>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: style.color, marginBottom: 4 }}>
                    {a.level} · {a.village_name}
                  </div>
                  <div style={{ fontSize: 13.5, color: "var(--text-secondary)" }}>{a.message}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div style={{ width: 300, flexShrink: 0 }}>
        <AlertsSummary alerts={alerts} />
      </div>
    </div>
  );
}
