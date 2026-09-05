"""Grounded RakshaSetu AI assistant with selectable providers."""
from app.core.config import get_settings
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.optimization.relocation import build_relocation_plan

SYSTEM_PROMPT="""You are RakshaSetu AI, a disaster-response decision assistant. Use only supplied context. Never invent numbers, locations, capacities or events. Answer the user's exact question. Be concise and operational: situation, evidence, next step. Prototype values are synthetic unless a live/verified source is explicitly labelled."""

def _rows():
    rows=[]
    for v in synthetic.get_villages():
        ind=compute_risk(v); rows.append((v,ind,classify(ind["risk_score"])))
    return rows

def _template_answer(question:str)->str:
    q=question.lower().strip(); rows=_rows()
    if not rows:return "No monitored location data is available right now."
    if any(k in q for k in ["highest risk","highest-risk","most risk","riskiest"]):
        v,i,c=max(rows,key=lambda x:x[1]["risk_score"])
        return f"Highest current risk: {v['name']} — {v['district']}, {v.get('region',v.get('state'))}. Risk {i['risk_score']}/100 ({c['level']})."
    if any(k in q for k in ["critical","alert","alerts","emergency"]):
        c=sum(r[2]["level"]=="CRITICAL" for r in rows); h=sum(r[2]["level"]=="HIGH" for r in rows)
        top=sorted(rows,key=lambda x:x[1]["risk_score"],reverse=True)[:3]
        return f"Current monitored situation: {c} critical and {h} high-risk locations. Highest-priority locations: " + "; ".join(f"{v['name']} ({v['district']}, {v.get('region',v.get('state'))})" for v,_,_ in top) + "."
    matched=[r for r in rows if r[0]["name"].lower() in q or r[0]["district"].lower() in q or r[0].get("state","").lower() in q]
    if matched:
        v,i,c=sorted(matched,key=lambda x:x[1]["risk_score"],reverse=True)[0]
        if any(k in q for k in ["risk","safe","relocat","move","evacuat"]):
            p=build_relocation_plan(v,synthetic.get_safe_sites()); b=p.get("best_site")
            site=f" Best relocation option: {b['name']} (suitability {b.get('suitability','N/A')}, available {b.get('available_capacity','N/A')})." if b else " No suitable relocation site is currently available."
            return f"{v['name']} — {v['district']}, {v.get('region',v.get('state'))}. Risk {i['risk_score']}/100 ({c['level']}), population {v['population']}."+site
        if "history" in q or "incident" in q:
            events=synthetic.get_history(v["id"])
            return f"{v['name']} has {len(events)} recorded prototype history events: " + "; ".join(f"{e['year']} {e['hazard']} ({e['severity']})" for e in events) + "."
        return f"{v['name']} — {v['district']}, {v.get('region',v.get('state'))}. Risk {i['risk_score']}/100 ({c['level']}); population {v['population']}; hazard score {i['hazard']}; exposure {i['exposure']}."
    if "safe site" in q or "shelter" in q:
        sites=sorted(synthetic.get_safe_sites(),key=lambda s:s["capacity"]-s["current_occupancy"],reverse=True)[:3]
        return "Available safe-site options: " + "; ".join(f"{s['name']} ({s['capacity']-s['current_occupancy']:,} free)" for s in sites) + "."
    if "relocat" in q or "move" in q:
        v,_,_=max(rows,key=lambda x:x[1]["risk_score"]); p=build_relocation_plan(v,synthetic.get_safe_sites()); b=p.get("best_site")
        return f"For the highest-risk location, {v['name']}, the recommended safe site is {b['name']} with suitability {b.get('suitability','N/A')}." if b else "No suitable relocation site is currently available."
    top=max(rows,key=lambda x:x[1]["risk_score"])
    return f"RakshaSetu is monitoring {len(rows)} locations. Highest current risk is {top[0]['name']} at {top[1]['risk_score']}/100. Ask me about a village, district, risk, safe site, relocation or incident history."

def _build_context()->str:
    lines=["MONITORED LOCATIONS:"]
    for v,i,c in [(v,compute_risk(v),classify(compute_risk(v)["risk_score"])) for v in synthetic.get_villages()]:
        history=synthetic.get_history(v["id"])
        lines.append(f"- {v['name']} | region={v.get('region',v.get('state'))} | district={v['district']} | risk={i['risk_score']} [{c['level']}] | population={v['population']} | hazard={i['hazard']} | exposure={i['exposure']} | vulnerability={i['vulnerability']} | history_events={len(history)}")
    lines.append("SAFE SITES:")
    for s in synthetic.get_safe_sites(): lines.append(f"- {s['name']} | region={s.get('region')} | capacity={s['capacity']} | available={s['capacity']-s['current_occupancy']} | hazard_risk={s['hazard_risk']} | facilities={', '.join(s.get('facilities',[]))}")
    lines.append("HISTORICAL PATTERNS:")
    for v in synthetic.get_villages():
        e=synthetic.get_history(v["id"])
        if e: lines.append(f"- {v['name']}: "+"; ".join(f"{x.get('year')}: {x.get('hazard')} ({x.get('severity')})" for x in e))
    return "\n".join(lines)

async def ask(question:str)->dict:
    settings=get_settings(); provider=(settings.AI_PROVIDER or "openai").lower(); context=_build_context()
    try:
        if provider=="openai" and settings.OPENAI_API_KEY:
            from openai import OpenAI
            client=OpenAI(api_key=settings.OPENAI_API_KEY)
            r=client.responses.create(model=settings.OPENAI_MODEL,instructions=SYSTEM_PROMPT,input=f"CONTEXT DATA:\n{context}\n\nQUESTION:\n{question}",max_output_tokens=500)
            return {"answer":r.output_text,"grounded":True,"used_llm":True,"provider":"openai"}
        if provider=="google" and settings.GOOGLE_API_KEY:
            from google import genai
            client=genai.Client(api_key=settings.GOOGLE_API_KEY); r=client.models.generate_content(model=settings.GOOGLE_MODEL,contents=f"{SYSTEM_PROMPT}\n\nCONTEXT DATA:\n{context}\n\nQUESTION:\n{question}")
            return {"answer":r.text or _template_answer(question),"grounded":True,"used_llm":True,"provider":"google"}
        if provider=="anthropic" and settings.ANTHROPIC_API_KEY:
            import anthropic
            client=anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY); m=client.messages.create(model=settings.ANTHROPIC_MODEL,max_tokens=500,system=SYSTEM_PROMPT,messages=[{"role":"user","content":f"CONTEXT DATA:\n{context}\n\nQUESTION:\n{question}"}])
            text="".join(b.text for b in m.content if getattr(b,"type","")=="text")
            return {"answer":text or _template_answer(question),"grounded":True,"used_llm":True,"provider":"anthropic"}
    except Exception:
        # Keep the command centre usable when an external AI provider is out of
        # credits, rate-limited, offline, or temporarily unavailable.
        pass
    return {"answer":_template_answer(question),"grounded":True,"used_llm":False,"provider":"local-grounded"}
