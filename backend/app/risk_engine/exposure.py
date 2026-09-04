"""Exposure indicator: how physically exposed a settlement is, derived
from elevation, distance to the nearest river/coast, and embankment
condition (a weak embankment raises exposure even at moderate hazard)."""


def exposure_score(village: dict) -> float:
    elevation_component = max(0.0, 1 - village["elevation_m"] / 12) * 100
    proximity_component = max(0.0, 1 - village["distance_river_km"] / 5) * 100
    embankment_component = (1 - village["embankment_condition"]) * 100

    score = (
        elevation_component * 0.4
        + proximity_component * 0.35
        + embankment_component * 0.25
    )
    return round(min(100.0, max(0.0, score)), 1)
