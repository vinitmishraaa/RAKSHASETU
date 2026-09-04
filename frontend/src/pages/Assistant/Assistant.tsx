import { useState } from "react";
import { api } from "../../services/api";

interface Message { role: "user" | "assistant"; text: string; }

const SUGGESTIONS = [
  "Which location has the highest risk right now?",
  "What safe site is best for Gosaba Char?",
  "Which regions have the most critical locations?",
  "Summarise the current alert situation.",
];

export default function Assistant() {
  const [messages, setMessages] = useState<Message[]>([{ role: "assistant", text: "RakshaSetu AI is ready. Ask about current risk, villages, safe sites, relocation, alerts, or historical patterns." }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(question: string) {
    if (!question.trim() || loading) return;
    setMessages((m) => [...m, { role: "user", text: question.trim() }]); setInput(""); setLoading(true);
    try {
      const res = await api.assistant.ask(question.trim());
      setMessages((m) => [...m, { role: "assistant", text: res.answer }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", text: "Backend unavailable. Start the FastAPI server and try again." }]);
    } finally { setLoading(false); }
  }

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <div className="section-heading">
        <div><span className="eyebrow">DECISION SUPPORT</span><h2>RakshaSetu AI Assistant</h2></div>
        <span className="status-pill"><span className="status-dot" /> GROUNDED DATA</span>
      </div>
      <p style={{ marginBottom: 18 }}>Evidence-grounded answers from the risk engine, relocation optimizer, safe-site inventory and incident history.</p>
      <div className="panel" style={{ minHeight: "calc(100vh - 190px)", display: "flex", flexDirection: "column", padding: 20 }}>
        <div className="scrollable" style={{ flex: 1, display: "flex", flexDirection: "column", gap: 12, marginBottom: 16, paddingRight: 4 }}>
          {messages.map((m, i) => <div key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "78%", background: m.role === "user" ? "var(--brand)" : "var(--bg-inset)", color: m.role === "user" ? "#1a1206" : "var(--text-primary)", padding: "11px 14px", borderRadius: 10, fontSize: 13.5, whiteSpace: "pre-wrap", lineHeight: 1.55 }}>{m.text}</div>)}
          {loading && <div style={{ color: "var(--text-muted)", fontSize: 13 }}>Analysing system data…</div>}
        </div>
        {messages.length === 1 && <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 14 }}>{SUGGESTIONS.map((s) => <button key={s} className="btn" style={{ fontSize: 12 }} onClick={() => send(s)}>{s}</button>)}</div>}
        <form onSubmit={(e) => { e.preventDefault(); send(input); }} style={{ display: "flex", gap: 10 }}>
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about risk, safe sites, relocation, alerts or history…" style={{ flex: 1, background: "var(--bg-inset)", color: "var(--text-primary)", border: "1px solid var(--border-subtle)", borderRadius: 8, padding: "12px 14px", fontSize: 14 }} />
          <button className="btn btn-primary" type="submit" disabled={loading}>{loading ? "…" : "Send"}</button>
        </form>
      </div>
    </div>
  );
}
