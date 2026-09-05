import { useEffect, useState } from "react";
import { api } from "../../services/api";
import type { Alert } from "../../types";
import AlertsSummary from "../../components/alerts/AlertsSummary";

const LEVEL_STYLE: Record<string, { icon: string; color: string }> = {
  CRITICAL: { icon: "CRITICAL", color: "var(--risk-critical)" },
  HIGH: { icon: "HIGH", color: "var(--risk-high)" },
  WARNING: { icon: "WARNING", color: "var(--risk-moderate)" },
};

const OFFICIALS = [
  { name: "Anushko Adhikary", email: "anushkoadhikary8918@gmail.com", phone: "8918552039" },
  { name: "Medha Mallick", email: "medha.mallick2020@gmail.com", phone: "9007564988" },
  { name: "Ayan Acharya", email: "ayanacharya06@gmail.com", phone: "9433172520" },
  { name: "Soumyadeep Palit", email: "soumyadeeppalit546@gmail.com", phone: "8697453997" },
  { name: "Prithiwi Barui", email: "prithiwibarui@gmail.com", phone: "9748069930" },
];
const SOURCE_EMAIL = "mishravinit923@gmail.com";

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [soundOn, setSoundOn] = useState(false);
  async function refresh() { try { setAlerts(await api.alerts.list()); } catch { setAlerts([]); } }
  useEffect(() => { refresh(); const id = window.setInterval(refresh, 30000); return () => window.clearInterval(id); }, []);
  function testSiren() {
    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext; if (!AudioContextClass) return;
    const ctx = new AudioContextClass(); const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.connect(gain); gain.connect(ctx.destination); osc.type = "sawtooth"; gain.gain.value = 0.035; osc.frequency.value = 720; osc.start();
    window.setTimeout(() => { osc.frequency.value = 420; }, 450); window.setTimeout(() => { osc.stop(); ctx.close(); }, 900); setSoundOn(true); window.setTimeout(() => setSoundOn(false), 1000);
  }
  const critical = alerts.filter((a) => a.level === "CRITICAL");
  function mailOfficer(o: typeof OFFICIALS[number], a?: Alert) {
    const subject = a ? `[RakshaSetu] ${a.level} alert · ${a.village_name}` : "[RakshaSetu] Disaster response alert";
    const body = a ? `RakshaSetu alert\n\nZone: ${a.village_name}\nLevel: ${a.level}\nRisk score: ${a.risk_score}\nMessage: ${a.message}\n\nSource/admin contact: ${SOURCE_EMAIL}` : `RakshaSetu response notification.\n\nPlease review the selected regional dashboard and active alerts.\n\nSource/admin contact: ${SOURCE_EMAIL}`;
    window.location.href = `mailto:${o.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }
  function smsOfficer(o: typeof OFFICIALS[number], a?: Alert) {
    const body = a ? `RakshaSetu ${a.level}: ${a.village_name}. Risk ${a.risk_score}. ${a.message}` : "RakshaSetu response notification: please review the active regional alert dashboard.";
    window.location.href = `sms:${o.phone}?body=${encodeURIComponent(body)}`;
  }
  return <div className="scrollable" style={{ padding: 24, flex: 1 }}>
    {critical.length > 0 && <div className="critical-alert-banner"><span className="pulse-dot" /><div><strong>{critical.length} CRITICAL ALERT{critical.length > 1 ? "S" : ""}</strong><span>Immediate officer review and relocation assessment required.</span></div><button onClick={testSiren}>{soundOn ? "SIREN ACTIVE" : "TEST SIREN"}</button></div>}
    <div style={{ display: "flex", gap: 20 }}>
      <div style={{ flex: 1 }}>
        <div className="section-heading"><div><span className="eyebrow">INCIDENT ESCALATION</span><h2>Alerts &amp; Response</h2></div><button className="module-action" onClick={refresh}>Refresh</button></div>
        <p style={{ marginBottom: 20 }}>Active risk alerts are refreshed automatically. Select an administration contact to compose an email or SMS alert.</p>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {alerts.length === 0 && <div className="panel" style={{ padding: 18 }}>No active alerts.</div>}
          {alerts.map((a, i) => { const style = LEVEL_STYLE[a.level] || LEVEL_STYLE.WARNING; return <div key={`${a.village_id}-${a.level}-${i}`} className="panel alert-card" style={{ borderLeft: `3px solid ${style.color}` }}><div className="alert-level" style={{ color: style.color }}>{style.icon} · {a.village_name}</div><div className="alert-message">{a.message}</div><span className="mono alert-score">Risk score {a.risk_score}</span><div className="officer-actions">{OFFICIALS.slice(0, 3).map(o => <button key={o.email} className="contact-chip" onClick={() => mailOfficer(o, a)}>{o.name} · Email</button>)}</div></div>; })}
        </div>
      </div>
      <div style={{ width: 330, flexShrink: 0 }}><AlertsSummary alerts={alerts} /></div>
    </div>
    <section className="panel officer-panel"><div className="section-heading"><div><span className="eyebrow">ADMINISTRATION CONTACTS</span><h2>Officer Alert Desk</h2></div><span className="mono">FROM {SOURCE_EMAIL}</span></div><div className="officer-grid">{OFFICIALS.map(o => <article className="officer-card" key={o.email}><div><strong>{o.name}</strong><small>{o.email}</small><small>{o.phone}</small></div><div className="officer-buttons"><button className="btn" onClick={() => mailOfficer(o)}>Email</button><button className="btn secondary" onClick={() => smsOfficer(o)}>SMS</button></div></article>)}</div><p className="data-note">The Email/SMS actions open the device's configured composer. Actual automated sending requires an authenticated notification provider.</p></section>
  </div>;
}
