"""Relocation allocator: given a village's population and ranked safe
sites, produces either a single best-site recommendation or a split
allocation plan when no single site has enough capacity."""
from .site_scoring import rank_sites
from .capacity import available_capacity


def build_relocation_plan(village: dict, sites: list[dict]) -> dict:
    ranked = rank_sites(village, sites)
    population = village["population"]

    if not ranked:
        return {
            "village_id": village["id"],
            "population": population,
            "best_site": None,
            "allocations": [],
            "fully_covered": False,
            "reason": "No candidate safe sites available",
        }

    best = ranked[0]

    if best["available_capacity"] >= population:
        return {
            "village_id": village["id"],
            "population": population,
            "best_site": best,
            "allocations": [
                {
                    "site_id": best["site_id"],
                    "site_name": best["site_name"],
                    "people": population,
                }
            ],
            "fully_covered": True,
            "reason": None,
        }

    # Split allocation across ranked sites, highest suitability first.
    remaining = population
    allocations = []
    for site in ranked:
        if remaining <= 0:
            break
        take = min(site["available_capacity"], remaining)
        if take <= 0:
            continue
        allocations.append(
            {"site_id": site["site_id"], "site_name": site["site_name"], "people": take}
        )
        remaining -= take

    return {
        "village_id": village["id"],
        "population": population,
        "best_site": best,
        "allocations": allocations,
        "fully_covered": remaining <= 0,
        "reason": (
            f"{best['site_name']} capacity insufficient for entire population"
            if remaining <= 0 else
            f"Combined safe-site capacity insufficient; {remaining} people still unallocated"
        ) if len(allocations) > 1 or remaining > 0 else None,
    }
