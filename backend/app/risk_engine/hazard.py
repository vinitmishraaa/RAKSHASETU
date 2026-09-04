"""Hazard indicator: combines flood, cyclone and landslide hazard signals
for a location into a single 0-100 hazard intensity score."""

WEIGHTS = {"flood": 0.5, "cyclone": 0.35, "landslide": 0.15}


def hazard_score(village: dict) -> float:
    score = (
        village["flood_hazard"] * WEIGHTS["flood"]
        + village["cyclone_hazard"] * WEIGHTS["cyclone"]
        + village["landslide_hazard"] * WEIGHTS["landslide"]
    )
    return round(min(100.0, max(0.0, score)), 1)
