"""Classifies a numeric risk score into the Low/Moderate/High/Critical
red-zone bands used across the dashboard. Thresholds are a starting
point only - the source doc is explicit that these should be recalibrated
in Phase 2 against real data distribution and field validation."""

THRESHOLDS = [
    (75, 100, "CRITICAL", "#e5484d"),
    (50, 75, "HIGH", "#f2994a"),
    (30, 50, "MODERATE", "#f5c94a"),
    (0, 30, "LOW", "#3fb27f"),
]


def classify(risk_score: float) -> dict:
    for low, high, label, color in THRESHOLDS:
        if low <= risk_score <= high or (label == "CRITICAL" and risk_score > high):
            return {"level": label, "color": color}
    return {"level": "LOW", "color": "#3fb27f"}
