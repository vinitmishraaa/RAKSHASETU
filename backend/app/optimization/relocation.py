"""Relocation allocator with carrying capacity assessment and region-aware candidate selection."""
from __future__ import annotations
from typing import Any
from .site_scoring import rank_sites


def build_relocation_plan(village: dict[str, Any], sites: list[dict[str, Any]]) -> dict[str, Any]:
    region = village.get("region") or village.get("state")
    regional = [s for s in sites if (s.get("region") or s.get("state")) == region]
    candidates = regional or sites
    ranked = rank_sites(village, candidates)
    population = village.get("population") or 0

    if not ranked:
        return {
            "village_id": village["id"],
            "population": population,
            "best_site": None,
            "allocations": [],
            "fully_covered": False,
            "candidate_scope": "none",
            "reason": "No candidate safe sites available",
            "carrying_capacity_assessment": None,
        }

    best = ranked[0]
    total_reg_capacity = sum(s.get("capacity") or s.get("available_capacity") or 0 for s in candidates)
    total_reg_available = sum(s.get("available_capacity") or 0 for s in candidates)

    primary_cap = best.get("capacity") or (best.get("available_capacity", 0) + best.get("current_occupancy", 0)) or 5000
    primary_occ = best.get("current_occupancy") or 0
    primary_avail = best.get("available_capacity", primary_cap - primary_occ)

    if primary_avail >= population:
        post_occ = primary_occ + population
        stress_pct = round((post_occ / max(primary_cap, 1)) * 100, 1)
        status = "SAFE_WITHIN_HEADROOM" if stress_pct <= 75.0 else "ELEVATED_HEADROOM_STRESS"

        capacity_assessment = {
            "primary_site_id": best["site_id"],
            "primary_site_name": best["site_name"],
            "total_capacity": primary_cap,
            "pre_occupancy": primary_occ,
            "available_headroom": primary_avail,
            "evacuee_demand": population,
            "post_intake_occupancy": post_occ,
            "stress_level_pct": stress_pct,
            "carrying_capacity_status": status,
            "overcrowding_mitigation": "Single shelter possesses verified headroom; zero secondary displacement required.",
            "total_regional_capacity": total_reg_capacity,
            "total_regional_available": total_reg_available,
        }

        return {
            "village_id": village["id"],
            "population": population,
            "best_site": best,
            "allocations": [
                {
                    "site_id": best["site_id"],
                    "site_name": best["site_name"],
                    "people": population,
                    "site_capacity": primary_cap,
                    "post_occupancy": post_occ,
                    "utilization_pct": stress_pct,
                }
            ],
            "fully_covered": True,
            "candidate_scope": "same-region" if regional else "global-fallback",
            "reason": None,
            "carrying_capacity_assessment": capacity_assessment,
        }

    # Split allocation across multiple safe shelters to avoid exceeding carrying capacity
    remaining = population
    allocations = []
    for site in ranked:
        if remaining <= 0:
            break
        site_avail = site.get("available_capacity") or 0
        take = min(site_avail, remaining)
        if take > 0:
            s_cap = site.get("capacity") or (site_avail + (site.get("current_occupancy") or 0))
            s_pre = site.get("current_occupancy") or 0
            s_post = s_pre + take
            allocations.append({
                "site_id": site["site_id"],
                "site_name": site["site_name"],
                "people": take,
                "site_capacity": s_cap,
                "post_occupancy": s_post,
                "utilization_pct": round((s_post / max(s_cap, 1)) * 100, 1),
            })
            remaining -= take

    overflow_count = population - (allocations[0]["people"] if allocations else 0)
    capacity_assessment = {
        "primary_site_id": best["site_id"],
        "primary_site_name": best["site_name"],
        "total_capacity": primary_cap,
        "pre_occupancy": primary_occ,
        "available_headroom": primary_avail,
        "evacuee_demand": population,
        "post_intake_occupancy": primary_cap,
        "stress_level_pct": 100.0,
        "carrying_capacity_status": "OVERLOAD_PREVENTED_SPLIT_ROUTED",
        "overcrowding_mitigation": f"Carrying capacity ceiling enforced. Primary site capped at safe capacity; {overflow_count} evacuees load-balanced to secondary shelters to eliminate camp disease & congestion hazards.",
        "total_regional_capacity": total_reg_capacity,
        "total_regional_available": total_reg_available,
    }

    return {
        "village_id": village["id"],
        "population": population,
        "best_site": best,
        "allocations": allocations,
        "fully_covered": remaining <= 0,
        "candidate_scope": "same-region" if regional else "global-fallback",
        "reason": None if remaining <= 0 and len(allocations) == 1 else (
            f"Combined regional shelter capacity insufficient; {remaining} people still unallocated"
            if remaining > 0 else f"Primary site carrying capacity exceeded; {overflow_count} evacuees automatically split-allocated across {len(allocations)} shelters."
        ),
        "carrying_capacity_assessment": capacity_assessment,
    }
