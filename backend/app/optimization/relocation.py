"""Relocation allocator with region-aware candidate selection."""
from .site_scoring import rank_sites


def build_relocation_plan(village: dict, sites: list[dict]) -> dict:
    region = village.get("region") or village.get("state")
    regional = [s for s in sites if (s.get("region") or s.get("state")) == region]
    candidates = regional or sites
    ranked = rank_sites(village, candidates)
    population = village["population"]

    if not ranked:
        return {
            "village_id": village["id"], "population": population, "best_site": None,
            "allocations": [], "fully_covered": False, "candidate_scope": "none",
            "reason": "No candidate safe sites available",
        }

    best = ranked[0]
    if best["available_capacity"] >= population:
        return {
            "village_id": village["id"], "population": population, "best_site": best,
            "allocations": [{"site_id": best["site_id"], "site_name": best["site_name"], "people": population}],
            "fully_covered": True,
            "candidate_scope": "same-region" if regional else "global-fallback", "reason": None,
        }

    remaining = population
    allocations = []
    for site in ranked:
        if remaining <= 0:
            break
        take = min(site["available_capacity"], remaining)
        if take > 0:
            allocations.append({"site_id": site["site_id"], "site_name": site["site_name"], "people": take})
            remaining -= take

    return {
        "village_id": village["id"], "population": population, "best_site": best,
        "allocations": allocations, "fully_covered": remaining <= 0,
        "candidate_scope": "same-region" if regional else "global-fallback",
        "reason": None if remaining <= 0 and len(allocations) == 1 else (
            f"Combined safe-site capacity insufficient; {remaining} people still unallocated"
            if remaining > 0 else f"{best['site_name']} capacity insufficient; allocation split across sites"
        ),
    }
