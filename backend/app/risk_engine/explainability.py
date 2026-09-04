"""Produces the human-readable 'WHY CRITICAL?' reasons shown when an
authority user clicks into a village, grounded only in the computed
indicators - never invented commentary."""


def explain(village: dict, indicators: dict, history: list) -> list[str]:
    reasons = []

    if village["flood_hazard"] >= 70:
        reasons.append("High flood exposure")
    if village["cyclone_hazard"] >= 70:
        reasons.append("High cyclone exposure")
    if indicators["vulnerability"] >= 60:
        reasons.append("High share of vulnerable population (children/elderly)")
    if village["distance_road_km"] >= 8:
        reasons.append("Poor road accessibility")
    if village["embankment_condition"] <= 0.4:
        reasons.append("Weak or degraded embankment")
    if len(history) >= 3:
        reasons.append("Recurring historical disaster events")

    if not reasons:
        reasons.append("Indicators currently within acceptable range")

    return reasons


def recommended_action(level: str) -> str:
    return {
        "CRITICAL": "Immediate relocation assessment",
        "HIGH": "Priority monitoring and relocation planning",
        "MODERATE": "Scheduled monitoring and embankment/infrastructure review",
        "LOW": "Routine monitoring",
    }.get(level, "Routine monitoring")
