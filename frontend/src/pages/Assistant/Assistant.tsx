import { useState } from "react";
import { api } from "../../services/api";

interface Message { role:"user"|"assistant"; text:string; }
const SUGGESTIONS=["Highest risk right now?","Best safe site for Gosaba Char?","Which areas are critical?","Summarise current alerts."];

export default function Assistant(){
 const [messages,setMessages]=useState<Message[]>([{role:"assistant",text:"RakshaSetu AI is ready. Ask about current risk, villages, safe sites, relocation, alerts or incident history."}]);
 const [input,setInput]=useState(""); const [loading,setLoading]=useState(false);
 async function send(question:string){if(!question.trim()||loading)return;const q=question.trim();setMessages(m=>[...m,{role:"user",text:q}]);setInput("");setLoading(true);try{const res=await api.assistant.ask(q);setMessages(m=>[...m,{role:"assistant",text:res.answer}]);}catch{setMessages(m=>[...m,{role:"assistant",text:"I couldn't reach the RakshaSetu backend. Make sure FastAPI is running on port 8000."}]);}finally{setLoading(false)}}
 return <div className="assistant-page"><section className="assistant-hero"><div><span className="eyebrow">DECISION SUPPORT</span><h1>RakshaSetu AI Assistant</h1><p>Grounded answers from monitored risk, safe-site, relocation and incident data.</p></div><span className="assistant-status"><i/> GROUNDED · LIVE DATA</span></section><section className="assistant-shell"><div className="assistant-toolbar"><div><strong>Response Desk</strong><small>Ask naturally — the assistant uses RakshaSetu's monitored data.</small></div><span>{loading?"ANALYSING":"READY"}</span></div><div className="assistant-messages">{messages.map((m,i)=><div key={i} className={`assistant-message ${m.role}`}><span className="assistant-role">{m.role==="user"?"YOU":"RAKSHASETU AI"}</span><div>{m.text}</div></div>)}{loading&&<div className="assistant-typing"><i/><i/><i/> Checking response data…</div>}</div>{messages.length===1&&<div className="assistant-suggestions">{SUGGESTIONS.map(s=><button key={s} onClick={()=>send(s)}>{s}</button>)}</div>}<form className="assistant-input" onSubmit={e=>{e.preventDefault();send(input)}}><input value={input} onChange={e=>setInput(e.target.value)} placeholder="Ask about a village, risk, safe site, relocation or incident…"/><button type="submit" disabled={loading||!input.trim()}>{loading?"…":"Send"}</button></form></section></div>;
}
