"""
AI Assistant: answers authority questions using ONLY verified system
data (villages, risk scores, safe sites, relocation plans, history) -
never free-floating claims.

If ANTHROPIC_API_KEY is set, the grounded context is handed to Claude
to produce a natural-language answer. If no key is set, a deterministic
templated summary is returned instead so the assistant still works
out of the box.
"""
from app.core.config import get_settings
from app.data import synthetic
from app.risk_engine.scoring import compute_risk
from app.risk_engine.classification import classify
from app.risk_engine.explainability import explain, recommended_action
from app.optimization.relocation import build_relocation_plan

SYSTEM_PROMPT = """You are the RakshaSetu AI Assistant, embedded in a disaster
relocation planning dashboard used by government authorities. Answer the
authority's question using ONLY the CONTEXT DATA provided below - it comes
directly from the system's risk engine and relocation optimizer. Do not
invent figures. If the context does not contain the answer, say so plainly
and suggest which dashboard section would have it. Keep answers concise,
factual, and decision-oriented."""


def _build_context() -> str:
    lines = []
    for village in synthetic.get_villages():
        indicators = compute_risk(village)
        classification = classify(indicators["risk_score"])
        history = synthetic.get_history(village["id"])
        lines.append(
            f"- {village['name']} ({village['id']}, {village['district']}): "
            f"risk={indicators['risk_score']} [{classification['level']}], "
            f"population={village['population']}, "
            f"hazard={indicators['hazard']}, exposure={indicators['exposure']}, "
            f"vulnerability={indicators['vulnerability']}, "
            f"historical events={len(history)}"
        )
    lines.append("\nSafe sites:")
    for site in synthetic.get_safe_sites():
        available = site["capacity"] - site["current_occupancy"]
        lines.append(
            f"- {site['name']} ({site['id']}): capacity={site['capacity']}, "
            f"available={available}, hazard_risk={site['hazard_risk']}"
        )
    return "\n".join(lines)


def _template_answer(question: str) -> str:
    context = _build_context()
    villages = synthetic.get_villages()
    scored = []
    for v in villages:
        ind = compute_risk(v)
        cls = classify(ind["risk_score"])
        scored.append((v, ind, cls))
    scored.sort(key=lambda t: t[1]["risk_score"], reverse=True)
    top = scored[0]

    return (
        f"Based on current system data, {top[0]['name']} has the highest "
        f"risk score at {top[1]['risk_score']} ({top[2]['level']}), driven by "
        f"hazard={top[1]['hazard']}, exposure={top[1]['exposure']}, "
        f"vulnerability={top[1]['vulnerability']}.\n\n"
        f"Set ANTHROPIC_API_KEY in backend/.env to enable full natural-language "
        f"question answering over this data. For now, here is the underlying "
        f"context this question would be answered from:\n\n{context}"
    )


async def ask(question: str) -> dict:
    settings = get_settings()
    context = _build_context()

    if not settings.ANTHROPIC_API_KEY:
        return {"answer": _template_answer(question), "grounded": True, "used_llm": False}

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"CONTEXT DATA:\n{context}\n\nQUESTION: {question}",
                }
            ],
        )
        text = "".join(
            block.text for block in message.content if getattr(block, "type", "") == "text"
        )
        return {"answer": text, "grounded": True, "used_llm": True}
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {
            "answer": _template_answer(question)
            + f"\n\n(Note: LLM call failed, showing fallback. Error: {exc})",
            "grounded": True,
            "used_llm": False,
        }
