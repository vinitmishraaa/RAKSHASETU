"""Combines hazard + exposure + vulnerability into the single habitation
level Risk Score shown throughout the dashboard (0-100)."""
from __future__ import annotations
from .hazard import hazard_score
from .exposure import exposure_score
from .vulnerability import vulnerability_score

RISK_WEIGHTS = {"hazard": 0.40, "exposure": 0.30, "vulnerability": 0.30}


def compute_risk(village: dict, weather: dict | None = None, earthquake: dict | None = None) -> dict:
    hazard = hazard_score(village, weather=weather, earthquake=earthquake)
    exposure = exposure_score(village)
    vulnerability = vulnerability_score(village)

    risk = (
        hazard * RISK_WEIGHTS["hazard"]
        + exposure * RISK_WEIGHTS["exposure"]
        + vulnerability * RISK_WEIGHTS["vulnerability"]
    )
    risk = round(min(100.0, max(0.0, risk)), 1)

    return {
        "risk_score": risk,
        "hazard": hazard,
        "exposure": exposure,
        "vulnerability": vulnerability,
    }
