"""Operational Data Layer for RakshaSetu.

Connects to the authoritative Indian geographic catalog, providing settlements,
safe sites, historical events, and rainfall trends for all 36 States/UTs.
"""
from __future__ import annotations
from typing import Any
from app.data.geo_catalog import (
    get_villages_for_scope,
    get_village_by_id,
    get_safesites_for_scope,
    get_safesite_by_id,
    get_history_for_village,
    get_rainfall_for_village,
    DETAILED_VILLAGES,
    DETAILED_SAFE_SITES,
)

VILLAGES = DETAILED_VILLAGES
SAFE_SITES = DETAILED_SAFE_SITES


def get_villages(state: str | None = None, district: str | None = None, city: str | None = None) -> list[dict[str, Any]]:
    return get_villages_for_scope(state, district, city)


def get_village(village_id: str) -> dict[str, Any] | None:
    return get_village_by_id(village_id)


def get_safe_sites(state: str | None = None, district: str | None = None, city: str | None = None) -> list[dict[str, Any]]:
    return get_safesites_for_scope(state, district, city)


def get_safe_site(site_id: str) -> dict[str, Any] | None:
    return get_safesite_by_id(site_id)


def get_history(village_id: str) -> list[dict[str, Any]]:
    return get_history_for_village(village_id)


def get_rainfall_trend(village_id: str, base_rainfall: int = 250) -> list[int]:
    return get_rainfall_for_village(village_id, base_rainfall)
