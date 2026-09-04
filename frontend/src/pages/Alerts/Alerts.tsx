import { useEffect, useState } from "react";
import { api } from "../../services/api";
import type { Alert } from "../../types";
import AlertsSummary from "../../components/alerts/AlertsSummary";

const LEVEL_STYLE: Record<string, { icon: string; color: string }> = {
  CRITICAL: { icon: "CRITICAL", color: "var(--risk-critical)" },
  HIGH: { icon: "HIGH", color: "var(--risk-high)" },
  WARNING: { icon: "WARNING", color: "var(--risk-moderate)" },
};

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [soundOn, setSoundOn] = useState(false);

  async function refresh() { try { setAlerts(await api.alerts.list()); } catch { setAlerts([]); } }
  useEffect(() => { refresh(); const id = window.setInterval(refresh, 30000); return () => window.clearInterval(id); }, []);

  function testSiren() {
    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    const osc = ctx.createOscillator(); const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination); osc.type = "sawtooth"; gain.gain.value = 0.035;
    osc.frequency.value = 720; osc.start();
    window.setTimeout(() => { osc.frequency.value = 420; }, 450);
    window.setTimeout(() => { osc.stop(); ctx.close(); }, 900);
    setSoundOn(true); window.setTimeout(() => setSoundOn(false), 1000);
  }

  const critical = alerts.filter((a) => a.level === "CRITICAL");
  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      {critical.length > 0 && <div className="critical-alert-banner"><span className="pulse-dot" /><div><strong>{critical.length} CRITICAL ALERT{critical.length > 1 ? "S" : ""}</strong><span>Immediate officer review and relocation assessment required.</span></div><button onClick={testSiren}>{soundOn ? "SIREN ACTIVE" : "TEST SIREN"}</button></div>}
      <div style={{ display: "flex", gap: 20 }}>
        <div style={{ flex: 1 }}>
          <div className="section-heading"><div><span className="eyebrow">INCIDENT ESCALATION</span><h2>Alerts &amp; Response</h2></div><button className="module-action" onClick={refresh}>Refresh</button></div>
          <p style={{ marginBottom: 20 }}>Risk-based alerts refresh automatically. External SMS, WhatsApp and email dispatch can be connected through notification providers without exposing credentials in the frontend.</p>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {alerts.length === 0 && <div className="panel" style={{ padding: 18 }}>No active alerts.</div>}
            {alerts.map((a, i) => { const style = LEVEL_STYLE[a.level] || LEVEL_STYLE.WARNING; return <div key={`${a.village_id}-${a.level}-${i}`} className="panel alert-card" style={{ borderLeft: `3px solid ${style.color}` }}><div className="alert-level" style={{ color: style.color }}>{style.icon} · {a.village_name}</div><div className="alert-message">{a.message}</div><span className="mono alert-score">Risk score {a.risk_score}</span></div>; })}
          </div>
        </div>
        <div style={{ width: 300, flexShrink: 0 }}><AlertsSummary alerts={alerts} /></div>
      </div>
    </div>
  );
}
