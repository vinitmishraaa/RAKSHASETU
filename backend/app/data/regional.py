"""Deterministic synthetic coverage for RakshaSetu's target response region.

This expands the original detailed West Bengal demo into district-level
prototype records across West Bengal, Bihar, Odisha, Jharkhand, Sikkim and
Nepal. Values are demo data, not operational GIS intelligence.
"""
from __future__ import annotations

import hashlib
import random

from app.data import districts
from app.data import synthetic


def _rng(key: str) -> random.Random:
    seed = int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:8], 16)
    return random.Random(seed)


def _point(region: str, district: str):
    rng = _rng(f"point:{region}:{district}")
    south, north, west, east = districts.REGION_BOUNDS[region]
    return round(rng.uniform(south, north), 5), round(rng.uniform(west, east), 5)


def _risk_values(region: str, district: str):
    rng = _rng(f"risk:{region}:{district}")
    flood = rng.randint(28, 92)
    landslide = rng.randint(10, 88)
    cyclone = rng.randint(12, 92)
    if region in {"Bihar", "Nepal"}:
        flood = min(96, flood + 8)
    if region in {"Odisha", "West Bengal"}:
        cyclone = min(96, cyclone + 10)
    if region in {"Sikkim", "Jharkhand", "Nepal"}:
        landslide = min(96, landslide + 12)
    return flood, landslide, cyclone


def _village(region: str, district: str, index: int):
    rng = _rng(f"village:{region}:{district}")
    lat, lng = _point(region, district)
    flood, landslide, cyclone = _risk_values(region, district)
    population = rng.randint(900, 6800)
    return {
        "id": f"RG{index:03d}",
        "name": f"{district} Response Zone",
        "district": district,
        "state": region,
        "region": region,
        "lat": lat,
        "lng": lng,
        "population": population,
        "households": max(1, round(population / rng.uniform(3.7, 5.2))),
        "children": round(population * rng.uniform(0.16, 0.24)),
        "elderly": round(population * rng.uniform(0.07, 0.13)),
        "other_vulnerable": round(population * rng.uniform(0.04, 0.09)),
        "elevation_m": round(rng.uniform(2.0, 14.0), 1),
        "distance_river_km": round(rng.uniform(0.2, 7.0), 2),
        "distance_road_km": round(rng.uniform(0.4, 15.0), 2),
        "embankment_condition": round(rng.uniform(0.3, 0.9), 2),
        "rainfall_mm_month": rng.randint(120, 360),
        "flood_hazard": flood,
        "landslide_hazard": landslide,
        "cyclone_hazard": cyclone,
    }


def _safe_site(region: str, index: int):
    rng = _rng(f"site:{region}:{index}")
    lat, lng = _point(region, f"safe-site-{index}")
    capacity = rng.randint(1200, 6500)
    occupancy = rng.randint(100, min(1000, capacity // 2))
    facilities = ["Water supply", "Emergency power"]
    if rng.random() > 0.35:
        facilities.append("Medical post")
    if rng.random() > 0.45:
        facilities.append("Shelter-ready hall")
    return {
        "id": f"RS{index:03d}",
        "name": f"{region} Emergency Shelter {index}",
        "region": region,
        "lat": lat,
        "lng": lng,
        "capacity": capacity,
        "current_occupancy": occupancy,
        "elevation_m": round(rng.uniform(5, 25), 1),
        "distance_road_km": round(rng.uniform(0.1, 2.5), 2),
        "hazard_risk": rng.randint(5, 30),
        "infrastructure_score": rng.randint(68, 96),
        "facilities": facilities,
    }


def build_regional_data():
    existing_districts = {v["district"] for v in synthetic.VILLAGES}
    generated = []
    index = 100
    for region in districts.TARGET_REGIONS:
        for district in districts.get_districts(region):
            if district in existing_districts:
                continue
            generated.append(_village(region, district, index))
            index += 1

    sites = []
    site_index = 10
    for region in districts.TARGET_REGIONS:
        for _ in range(3):
            sites.append(_safe_site(region, site_index))
            site_index += 1

    # Add lightweight historical context and rainfall series for generated zones.
    for village in generated:
        rng = _rng(f"history:{village['id']}")
        hazards = ["Flood", "Heavy Rainfall", "Cyclone", "Landslide"]
        events = []
        for year in (2019, 2021, 2023, 2025):
            hazard = hazards[rng.randrange(len(hazards))]
            severity = rng.choice(["Low", "Moderate", "High"])
            events.append({"year": year, "hazard": hazard, "severity": severity})
        synthetic.HISTORICAL_EVENTS[village["id"]] = events
        base = village["rainfall_mm_month"]
        synthetic.RAINFALL_TREND[village["id"]] = [
            max(80, round(base * rng.uniform(0.55, 1.15))) for _ in range(12)
        ]

    return generated, sites
