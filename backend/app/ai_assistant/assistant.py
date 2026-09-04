"""Grounded RakshaSetu AI assistant."""
from app.core.config import get_settings
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.optimization.relocation import build_relocation_plan

SYSTEM_PROMPT = """You are RakshaSetu AI, a disaster-response decision assistant. Use ONLY the supplied system context. Never invent numbers, locations, capacities or events. If data is missing, say so. Be concise and operational: identify the situation, evidence, and recommended next step. Treat all prototype values as synthetic unless verified feeds are connected."""


def _build_context() -> str:
    lines = ["MONITORED LOCATIONS:"]
    for village in synthetic.get_villages():
        ind = compute_risk(village)
        level = classify(ind["risk_score"])["level"]
        history = synthetic.get_history(village["id"])
        lines.append(f"- {village['name']} | region={village.get('region', village.get('state'))} | district={village['district']} | risk={ind['risk_score']} [{level}] | population={village['population']} | hazard={ind['hazard']} | exposure={ind['exposure']} | vulnerability={ind['vulnerability']} | history_events={len(history)}")
    lines.append("SAFE SITES:")
    for site in synthetic.get_safe_sites():
        lines.append(f"- {site['name']} | region={site.get('region', site.get('state'))} | capacity={site['capacity']} | available={site['capacity'] - site['current_occupancy']} | hazard_risk={site['hazard_risk']} | facilities={', '.join(site.get('facilities', []))}")
    lines.append("HISTORICAL PATTERNS:")
    for village in synthetic.get_villages():
        events = synthetic.get_history(village["id"])
        if events:
            lines.append(f"- {village['name']}: " + "; ".join(f"{e.get('year')}: {e.get('hazard')} ({e.get('severity')})" for e in events))
    return "\n".join(lines)


def _best_village():
    rows = []
    for v in synthetic.get_villages():
        ind = compute_risk(v); rows.append((v, ind, classify(ind["risk_score"])))
    return max(rows, key=lambda x: x[1]["risk_score"]) if rows else None


def _template_answer(question: str) -> str:
    q = question.lower()
    rows = []
    for v in synthetic.get_villages():
        ind = compute_risk(v); rows.append((v, ind, classify(ind["risk_score"])))
    if not rows:
        return "No monitored location data is available."
    if any(k in q for k in ["highest risk", "highest-risk", "most risk"]):
        v, ind, cls = max(rows, key=lambda x: x[1]["risk_score"])
        return f"Highest current risk: {v['name']} ({v['district']}, {v.get('region', v.get('state'))}) — {ind['risk_score']}/100, {cls['level']}. Hazard {ind['hazard']}, exposure {ind['exposure']}, vulnerability {ind['vulnerability']}."
    if "alert" in q or "critical" in q:
        critical = [r for r in rows if r[2]["level"] == "CRITICAL"]
        high = [r for r in rows if r[2]["level"] == "HIGH"]
        return f"Current risk situation: {len(critical)} critical and {len(high)} high-risk monitored locations. Review the Alerts and Dashboard views before issuing response orders."
    if "safe site" in q or "relocat" in q:
        name = next((v["name"] for v, _, _ in rows if v["name"].lower() in q), rows[0][0]["name"])
        v = next(v for v, _, _ in rows if v["name"] == name)
        plan = build_relocation_plan(v, synthetic.get_safe_sites())
        best = plan.get("best_site")
        if best:
            return f"Recommended relocation for {v['name']}: {best['name']} with suitability {best.get('suitability', 'N/A')} and available capacity {best.get('available_capacity', 'N/A')}. Coverage status: {'fully covered' if plan.get('fully_covered') else 'capacity gap — split allocation required'}."
    top = max(rows, key=lambda x: x[1]["risk_score"])
    return f"The system currently monitors {len(rows)} locations. Highest risk is {top[0]['name']} at {top[1]['risk_score']}/100 ({top[2]['level']}). For a specific village, safe site, region or historical event, ask by name."


async def ask(question: str) -> dict:
    settings = get_settings()
    context = _build_context()
    if not settings.ANTHROPIC_API_KEY:
        return {"answer": _template_answer(question), "grounded": True, "used_llm": False}
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(model="claude-sonnet-4-6", max_tokens=500, system=SYSTEM_PROMPT, messages=[{"role": "user", "content": f"CONTEXT DATA:\n{context}\n\nQUESTION: {question}"}])
        text = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
        return {"answer": text, "grounded": True, "used_llm": True}
    except Exception:
        return {"answer": _template_answer(question), "grounded": True, "used_llm": False}
