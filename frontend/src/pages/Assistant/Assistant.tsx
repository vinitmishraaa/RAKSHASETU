import { useState } from "react";
import { api } from "../../services/api";

interface Message {
  role: "user" | "assistant";
  text: string;
}

const SUGGESTIONS = [
  "Which village has the highest risk score right now?",
  "What safe site should Gosaba Char relocate to?",
  "Which villages have capacity warnings?",
  "Summarise the current alert situation.",
];

export default function Assistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text:
        "I'm the RakshaSetu assistant. I answer using only the system's live risk and relocation data — ask me about a village, a safe site, or the current alert situation.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(question: string) {
    if (!question.trim() || loading) return;
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);
    try {
      const res = await api.assistant.ask(question);
      setMessages((m) => [...m, { role: "assistant", text: res.answer }]);
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: "Sorry, I couldn't reach the backend. Is the FastAPI server running?" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0, padding: 24 }}>
      <h2 style={{ fontSize: 20, marginBottom: 4 }}>AI Assistant</h2>
      <p style={{ marginBottom: 16 }}>
        Evidence-grounded answers over risk scores, hazard indicators and relocation plans.
      </p>

      <div className="panel" style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0, padding: 20 }}>
        <div className="scrollable" style={{ flex: 1, display: "flex", flexDirection: "column", gap: 12, marginBottom: 16 }}>
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                maxWidth: "75%",
                background: m.role === "user" ? "var(--brand)" : "var(--bg-inset)",
                color: m.role === "user" ? "#1a1206" : "var(--text-primary)",
                padding: "10px 14px",
                borderRadius: 10,
                fontSize: 13.5,
                whiteSpace: "pre-wrap",
                lineHeight: 1.5,
              }}
            >
              {m.text}
            </div>
          ))}
          {loading && (
            <div style={{ alignSelf: "flex-start", color: "var(--text-muted)", fontSize: 13 }}>
              Thinking…
            </div>
          )}
        </div>

        {messages.length <= 1 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
            {SUGGESTIONS.map((s) => (
              <button key={s} className="btn" style={{ fontSize: 12 }} onClick={() => send(s)}>
                {s}
              </button>
            ))}
          </div>
        )}

        <form
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
          style={{ display: "flex", gap: 10 }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about risk, villages, safe sites, relocation plans…"
            style={{
              flex: 1,
              background: "var(--bg-inset)",
              color: "var(--text-primary)",
              border: "1px solid var(--border-subtle)",
              borderRadius: 8,
              padding: "11px 14px",
              fontSize: 14,
            }}
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
