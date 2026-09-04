"""Tracks and mutates safe-site occupancy for allocation planning."""


def available_capacity(site: dict) -> int:
    return max(0, site["capacity"] - site["current_occupancy"])


def can_absorb(site: dict, people: int) -> bool:
    return available_capacity(site) >= people
