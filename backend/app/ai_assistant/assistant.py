"""Grounded RakshaSetu AI assistant with selectable providers."""
from app.core.config import get_settings
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.optimization.relocation import build_relocation_plan
SYSTEM_PROMPT="""You are RakshaSetu AI, a disaster-response decision assistant. Use only supplied context. Never invent numbers, locations, capacities or events. Answer the user's exact question, vary the response according to the question, and state when information is unavailable. Be concise and operational: situation, evidence, next step. Prototype values are synthetic unless a live/verified source is explicitly labelled."""
def _build_context()->str:
 lines=["MONITORED LOCATIONS:"]
 for v in synthetic.get_villages():
  ind=compute_risk(v); level=classify(ind["risk_score"])["level"]; history=synthetic.get_history(v["id"])
  lines.append(f"- {v['name']} | region={v.get('region',v.get('state'))} | district={v['district']} | risk={ind['risk_score']} [{level}] | population={v['population']} | hazard={ind['hazard']} | exposure={ind['exposure']} | vulnerability={ind['vulnerability']} | history_events={len(history)}")
 lines.append("SAFE SITES:")
 for s in synthetic.get_safe_sites(): lines.append(f"- {s['name']} | region={s.get('region')} | capacity={s['capacity']} | available={s['capacity']-s['current_occupancy']} | hazard_risk={s['hazard_risk']} | facilities={', '.join(s.get('facilities',[]))}")
 lines.append("HISTORICAL PATTERNS:")
 for v in synthetic.get_villages():
  e=synthetic.get_history(v["id"])
  if e: lines.append(f"- {v['name']}: "+"; ".join(f"{x.get('year')}: {x.get('hazard')} ({x.get('severity')})" for x in e))
 return "\n".join(lines)
def _template_answer(q:str)->str:
 q=q.lower(); rows=[]
 for v in synthetic.get_villages():
  ind=compute_risk(v);rows.append((v,ind,classify(ind["risk_score"])))
 if not rows:return "No monitored location data is available."
 if any(k in q for k in ["highest risk","highest-risk","most risk"]):
  v,i,c=max(rows,key=lambda x:x[1]["risk_score"]);return f"Highest current risk: {v['name']} ({v['district']}, {v.get('region',v.get('state'))}) — {i['risk_score']}/100, {c['level']}."
 if "alert" in q or "critical" in q:
  c=sum(r[2]["level"]=="CRITICAL" for r in rows);h=sum(r[2]["level"]=="HIGH" for r in rows);return f"Current monitored situation: {c} critical and {h} high-risk locations."
 if "safe site" in q or "relocat" in q:
  v,_,_=max(rows,key=lambda x:x[1]["risk_score"]);p=build_relocation_plan(v,synthetic.get_safe_sites());b=p.get("best_site");return f"Best relocation option for {v['name']}: {b['name']} with suitability {b.get('suitability','N/A')} and available capacity {b.get('available_capacity','N/A')}." if b else "No suitable relocation site is currently available."
 top=max(rows,key=lambda x:x[1]["risk_score"]);return f"I can answer using the monitored response data. Current highest risk is {top[0]['name']} at {top[1]['risk_score']}/100. Ask about a specific district, village, incident, safe site, or relocation plan."
async def ask(question:str)->dict:
 settings=get_settings(); provider=(settings.AI_PROVIDER or "openai").lower(); context=_build_context(); error=None
 try:
  if provider=="openai" and settings.OPENAI_API_KEY:
   from openai import OpenAI
   client=OpenAI(api_key=settings.OPENAI_API_KEY);r=client.responses.create(model=settings.OPENAI_MODEL,instructions=SYSTEM_PROMPT,input=f"CONTEXT DATA:\n{context}\n\nQUESTION:\n{question}",max_output_tokens=500);return {"answer":r.output_text,"grounded":True,"used_llm":True}
  if provider=="google" and settings.GOOGLE_API_KEY:
   from google import genai
   client=genai.Client(api_key=settings.GOOGLE_API_KEY);r=client.models.generate_content(model=settings.GOOGLE_MODEL,contents=f"{SYSTEM_PROMPT}\n\nCONTEXT DATA:\n{context}\n\nQUESTION:\n{question}");return {"answer":r.text or _template_answer(question),"grounded":True,"used_llm":True}
  if provider=="anthropic" and settings.ANTHROPIC_API_KEY:
   import anthropic
   client=anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY);m=client.messages.create(model=settings.ANTHROPIC_MODEL,max_tokens=500,system=SYSTEM_PROMPT,messages=[{"role":"user","content":f"CONTEXT DATA:\n{context}\n\nQUESTION:\n{question}"}]);text="".join(b.text for b in m.content if getattr(b,"type","")=="text");return {"answer":text,"grounded":True,"used_llm":True}
  error=f"AI provider '{provider}' is not configured with a valid API key."
 except Exception as exc:
  error=f"{type(exc).__name__}: {str(exc)[:220]}"
 fallback=_template_answer(question)
 if error: fallback=f"AI connection unavailable ({error})\n\nData fallback: {fallback}"
 return {"answer":fallback,"grounded":True,"used_llm":False}
