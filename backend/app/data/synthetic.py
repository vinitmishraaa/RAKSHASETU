"""
Synthetic data layer.

This module stands in for Step 1/2 of the methodology (Data Collection +
GIS Integration) so the rest of the system — risk engine, optimizer,
dashboard — is fully wired and demoable without needing a live PostGIS
instance or licensed datasets on day one.

Villages are placed in a low-lying deltaic belt (modelled loosely on the
Sundarbans / lower Ganges-Brahmaputra region of West Bengal) because that
geography is genuinely flood- and cyclone-prone, so the numbers behave
the way real hazard data would: risk correlates with elevation, distance
from rivers, and embankment quality.

Swap `VILLAGES`, `SAFE_SITES`, `HISTORICAL_EVENTS` for real repository
calls against PostGIS once verified datasets are available — the rest
of the codebase (risk_engine, optimization, api) only depends on the
shapes defined in app/schemas, not on this file being synthetic.
"""
from __future__ import annotations
import random

random.seed(42)

VILLAGES = [
    {
        "id": "V001",
        "name": "Gosaba Char",
        "district": "South 24 Parganas",
        "state": "West Bengal",
        "lat": 22.1667,
        "lng": 88.8000,
        "population": 2400,
        "households": 510,
        "children": 420,
        "elderly": 290,
        "other_vulnerable": 180,
        "elevation_m": 2.1,
        "distance_river_km": 0.3,
        "distance_road_km": 6.8,
        "embankment_condition": 0.35,  # 0 = failing, 1 = strong
        "rainfall_mm_month": 310,
        "flood_hazard": 87,
        "landslide_hazard": 12,
        "cyclone_hazard": 74,
    },
    {
        "id": "V002",
        "name": "Sandeshkhali Basti",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "lat": 22.3667,
        "lng": 88.8500,
        "population": 3100,
        "households": 640,
        "children": 510,
        "elderly": 340,
        "other_vulnerable": 210,
        "elevation_m": 3.4,
        "distance_river_km": 1.1,
        "distance_road_km": 4.2,
        "embankment_condition": 0.55,
        "rainfall_mm_month": 275,
        "flood_hazard": 68,
        "landslide_hazard": 8,
        "cyclone_hazard": 61,
    },
    {
        "id": "V003",
        "name": "Kultali Nagar",
        "district": "South 24 Parganas",
        "state": "West Bengal",
        "lat": 21.9833,
        "lng": 88.6667,
        "population": 1850,
        "households": 390,
        "children": 300,
        "elderly": 220,
        "other_vulnerable": 140,
        "elevation_m": 1.6,
        "distance_river_km": 0.15,
        "distance_road_km": 14.0,
        "embankment_condition": 0.22,
        "rainfall_mm_month": 330,
        "flood_hazard": 94,
        "landslide_hazard": 5,
        "cyclone_hazard": 90,
    },
    {
        "id": "V004",
        "name": "Baruipur Purba",
        "district": "South 24 Parganas",
        "state": "West Bengal",
        "lat": 22.3600,
        "lng": 88.4300,
        "population": 4200,
        "households": 890,
        "children": 680,
        "elderly": 450,
        "other_vulnerable": 260,
        "elevation_m": 6.8,
        "distance_river_km": 3.2,
        "distance_road_km": 1.1,
        "embankment_condition": 0.7,
        "rainfall_mm_month": 240,
        "flood_hazard": 34,
        "landslide_hazard": 4,
        "cyclone_hazard": 29,
    },
    {
        "id": "V005",
        "name": "Hingalganj Char",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "lat": 22.4333,
        "lng": 88.9333,
        "population": 2950,
        "households": 615,
        "children": 470,
        "elderly": 310,
        "other_vulnerable": 195,
        "elevation_m": 1.9,
        "distance_river_km": 0.2,
        "distance_road_km": 11.4,
        "embankment_condition": 0.28,
        "rainfall_mm_month": 320,
        "flood_hazard": 91,
        "landslide_hazard": 6,
        "cyclone_hazard": 79,
    },
    {
        "id": "V006",
        "name": "Canning Dakshin",
        "district": "South 24 Parganas",
        "state": "West Bengal",
        "lat": 22.3100,
        "lng": 88.6600,
        "population": 1600,
        "households": 340,
        "children": 250,
        "elderly": 190,
        "other_vulnerable": 110,
        "elevation_m": 4.5,
        "distance_river_km": 1.8,
        "distance_road_km": 2.6,
        "embankment_condition": 0.6,
        "rainfall_mm_month": 260,
        "flood_hazard": 47,
        "landslide_hazard": 3,
        "cyclone_hazard": 40,
    },
]

SAFE_SITES = [
    {
        "id": "S001",
        "name": "Baruipur Relief Campus",
        "lat": 22.3550,
        "lng": 88.4400,
        "capacity": 3200,
        "current_occupancy": 400,
        "elevation_m": 9.2,
        "distance_road_km": 0.4,
        "hazard_risk": 12,
        "infrastructure_score": 88,
        "facilities": ["Medical post", "Water supply", "School (shelter-ready)"],
    },
    {
        "id": "S002",
        "name": "Jaynagar Community Ground",
        "lat": 22.1750,
        "lng": 88.4260,
        "capacity": 1800,
        "current_occupancy": 150,
        "elevation_m": 7.5,
        "distance_road_km": 1.2,
        "hazard_risk": 18,
        "infrastructure_score": 71,
        "facilities": ["Water supply", "Community hall"],
    },
    {
        "id": "S003",
        "name": "Canning Upazila Shelter",
        "lat": 22.3170,
        "lng": 88.6650,
        "capacity": 2200,
        "current_occupancy": 300,
        "elevation_m": 6.1,
        "distance_road_km": 0.6,
        "hazard_risk": 24,
        "infrastructure_score": 75,
        "facilities": ["Medical post", "Water supply"],
    },
    {
        "id": "S004",
        "name": "Diamond Harbour Rehab Site",
        "lat": 22.1900,
        "lng": 88.1900,
        "capacity": 5000,
        "current_occupancy": 900,
        "elevation_m": 10.4,
        "distance_road_km": 0.2,
        "hazard_risk": 8,
        "infrastructure_score": 92,
        "facilities": ["Medical post", "Water supply", "School", "Grid power"],
    },
]

HISTORICAL_EVENTS = {
    "V001": [
        {"year": 2018, "hazard": "Flood", "severity": "High"},
        {"year": 2020, "hazard": "Cyclone", "severity": "Critical"},
        {"year": 2022, "hazard": "Flood", "severity": "Moderate"},
        {"year": 2024, "hazard": "Heavy Rainfall", "severity": "Moderate"},
    ],
    "V002": [
        {"year": 2019, "hazard": "Flood", "severity": "Moderate"},
        {"year": 2021, "hazard": "Cyclone", "severity": "High"},
        {"year": 2023, "hazard": "Flood", "severity": "Moderate"},
    ],
    "V003": [
        {"year": 2017, "hazard": "Cyclone", "severity": "Critical"},
        {"year": 2018, "hazard": "Flood", "severity": "Critical"},
        {"year": 2020, "hazard": "Cyclone", "severity": "Critical"},
        {"year": 2022, "hazard": "Flood", "severity": "High"},
        {"year": 2024, "hazard": "Flood", "severity": "High"},
    ],
    "V004": [
        {"year": 2021, "hazard": "Heavy Rainfall", "severity": "Low"},
    ],
    "V005": [
        {"year": 2018, "hazard": "Cyclone", "severity": "Critical"},
        {"year": 2020, "hazard": "Flood", "severity": "High"},
        {"year": 2023, "hazard": "Flood", "severity": "High"},
        {"year": 2024, "hazard": "Cyclone", "severity": "Moderate"},
    ],
    "V006": [
        {"year": 2020, "hazard": "Heavy Rainfall", "severity": "Low"},
        {"year": 2023, "hazard": "Flood", "severity": "Moderate"},
    ],
}

RAINFALL_TREND = {
    "V001": [210, 240, 260, 300, 310, 340, 355, 330, 300, 260, 220, 200],
    "V002": [180, 200, 220, 250, 275, 290, 300, 280, 250, 220, 190, 170],
    "V003": [230, 260, 290, 320, 330, 360, 375, 350, 320, 280, 240, 210],
    "V004": [150, 170, 190, 220, 240, 255, 260, 240, 210, 180, 160, 140],
    "V005": [220, 250, 280, 305, 320, 350, 365, 340, 305, 270, 230, 210],
    "V006": [160, 180, 200, 230, 260, 270, 280, 260, 230, 200, 175, 155],
}


def get_villages():
    return VILLAGES


def get_village(village_id: str):
    return next((v for v in VILLAGES if v["id"] == village_id), None)


def get_safe_sites():
    return SAFE_SITES


def get_safe_site(site_id: str):
    return next((s for s in SAFE_SITES if s["id"] == site_id), None)


def get_history(village_id: str):
    return HISTORICAL_EVENTS.get(village_id, [])


def get_rainfall_trend(village_id: str):
    return RAINFALL_TREND.get(village_id, [])
