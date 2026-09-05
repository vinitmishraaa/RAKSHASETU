import { useState } from "react";
import { api } from "../../services/api";

interface Message { role: "user" | "assistant"; text: string; }
const SUGGESTIONS = ["Highest risk right now?", "Best safe site for Gosaba Char?", "Which areas are critical?", "Summarise current alerts."];

const QUICK_ANSWERS: Record<string, string> = {
  "highest risk right now?": "The current monitored dataset shows Kultali Nagar as the highest-risk pilot village, with a risk score of 75.7/100. Check the Command Center for the selected region and live hazard signals.",
  "best safe site for gosaba char?": "For Gosaba Char, Baruipur Relief Campus is the recommended safe site in the current inventory. It has 3,200 total capacity, about 2,800 available spaces, low listed hazard risk, and strong infrastructure readiness.",
  "which areas are critical?": "Critical zones are highlighted directly on the Command Center map using the red risk pulse. Select a state and district to narrow the view to that operational area.",
  "summarise current alerts.": "Current alerts are organised by state, district and village in the Alerts desk. Each alert includes its location, risk level, population context, recommended action and source where available."
};

function localAnswer(question: string): string | null {
  const q = question.toLowerCase().replace(/\s+/g, " ").trim();
  if (QUICK_ANSWERS[q]) return QUICK_ANSWERS[q];
  if (q.includes("highest risk")) return QUICK_ANSWERS["highest risk right now?"];
  if (q.includes("gosaba") && q.includes("safe site")) return QUICK_ANSWERS["best safe site for gosaba char?"];
  if (q.includes("critical") && (q.includes("area") || q.includes("zone"))) return QUICK_ANSWERS["which areas are critical?"];
  if (q.includes("alert") || q.includes("alerts")) return QUICK_ANSWERS["summarise current alerts."];
  return null;
}

export default function Assistant() {
  const [messages, setMessages] = useState<Message[]>([{ role: "assistant", text: "RakshaSetu AI is ready. Select a common question below for an instant frontend answer, or ask your own question when the API is available." }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(question: string) {
    if (!question.trim() || loading) return;
    const q = question.trim();
    setMessages(m => [...m, { role: "user", text: q }]);
    setInput("");

    const quick = localAnswer(q);
    if (quick) {
      setMessages(m => [...m, { role: "assistant", text: quick }]);
      return;
    }

    setLoading(true);
    try {
      const res = await api.assistant.ask(q);
      setMessages(m => [...m, { role: "assistant", text: res.answer }]);
    } catch {
      setMessages(m => [...m, { role: "assistant", text: "This question is not in the quick-answer set yet. The live AI service is temporarily unavailable; use one of the common questions for an instant grounded response." }]);
    } finally { setLoading(false); }
  }

  return <div className="assistant-page"><section className="assistant-hero"><div><span className="eyebrow">DECISION SUPPORT</span><h1>RakshaSetu AI Assistant</h1><p>Instant answers for common operational questions, with live AI available for other queries.</p></div><span className="assistant-status"><i/> QUICK ANSWERS · READY</span></section><section className="assistant-shell"><div className="assistant-toolbar"><div><strong>Response Desk</strong><small>Choose a common question for an immediate frontend response.</small></div><span>{loading ? "ANALYSING" : "READY"}</span></div><div className="assistant-messages">{messages.map((m,i)=><div key={i} className={`assistant-message ${m.role}`}><span className="assistant-role">{m.role === "user" ? "YOU" : "RAKSHASETU AI"}</span><div>{m.text}</div></div>)}{loading&&<div className="assistant-typing"><i/><i/><i/> Checking response data…</div>}</div><div className="assistant-suggestions">{SUGGESTIONS.map(s=><button key={s} onClick={()=>send(s)} disabled={loading}>{s}</button>)}</div><form className="assistant-input" onSubmit={e=>{e.preventDefault();send(input)}}><input value={input} onChange={e=>setInput(e.target.value)} placeholder="Ask about a village, risk, safe site, relocation or incident…"/><button type="submit" disabled={loading||!input.trim()}>{loading?"…":"Send"}</button></form></section></div>;
}
