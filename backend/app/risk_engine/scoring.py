"""Combines Hazard Intensity + Population Vulnerability + Disaster History
into the evidence-based habitation Risk Score shown throughout the dashboard (0-100),
strictly adhering to National Disaster Management Guidelines."""
from __future__ import annotations
from .hazard import hazard_score
from .exposure import exposure_score
from .vulnerability import vulnerability_score

# National Multi-Hazard Risk Formulation: Hazard Intensity (40%) + Population Vulnerability (35%) + Disaster History (25%)
RISK_WEIGHTS = {"hazard": 0.40, "vulnerability": 0.35, "history": 0.25}


def compute_risk(
    village: dict,
    weather: dict | None = None,
    earthquake: dict | None = None,
    history: list | None = None,
) -> dict:
    hazard = hazard_score(village, weather=weather, earthquake=earthquake)
    exposure = exposure_score(village)
    vulnerability = vulnerability_score(village)

    # 1. Population Vulnerability combines demographic susceptibility and access isolation
    pop_vulnerability = vulnerability * 0.6 + exposure * 0.4

    # 2. Disaster History Recurrence Factor (Historical Risk Pillar)
    hist_events = history if history is not None else village.get("history", [])
    if isinstance(hist_events, list) and len(hist_events) > 0:
        hist_score = min(100.0, len(hist_events) * 22.0)
    else:
        hist_score = min(100.0, float(village.get("history_recurrence_score") or 25.0))

    risk = (
        hazard * RISK_WEIGHTS["hazard"]
        + pop_vulnerability * RISK_WEIGHTS["vulnerability"]
        + hist_score * RISK_WEIGHTS["history"]
    )
    risk = round(min(100.0, max(0.0, risk)), 1)

    return {
        "risk_score": risk,
        "hazard": hazard,
        "exposure": exposure,
        "vulnerability": round(pop_vulnerability, 1),
        "disaster_history": round(hist_score, 1),
    }
