from pydantic import BaseModel
from typing import Optional


class VillageOut(BaseModel):
    id: str
    name: str
    district: str
    state: str
    lat: float
    lng: float
    population: int
    risk_score: float
    hazard: float
    exposure: float
    vulnerability: float
    accessibility: float
    level: str
    color: str


class VillageDetailOut(VillageOut):
    households: int
    children: int
    elderly: int
    other_vulnerable: int
    flood_hazard: float
    landslide_hazard: float
    cyclone_hazard: float
    rainfall_mm_month: float
    reasons: list[str]
    recommended_action: str
    history: list[dict]
    rainfall_trend: list[int]


class SafeSiteOut(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    capacity: int
    current_occupancy: int
    available_capacity: int
    hazard_risk: float
    infrastructure_score: float
    facilities: list[str]


class SiteSuitabilityOut(BaseModel):
    site_id: str
    site_name: str
    suitability: float
    distance_km: float
    available_capacity: int
    road_access: str
    hazard_risk: float


class RelocationAllocation(BaseModel):
    site_id: str
    site_name: str
    people: int


class RelocationPlanOut(BaseModel):
    village_id: str
    village_name: str
    population: int
    best_site: Optional[SiteSuitabilityOut]
    ranked_sites: list[SiteSuitabilityOut]
    allocations: list[RelocationAllocation]
    fully_covered: bool
    reason: Optional[str]


class AlertOut(BaseModel):
    village_id: str
    village_name: str
    level: str
    risk_score: float
    message: str


class AssistantQuery(BaseModel):
    question: str


class AssistantAnswer(BaseModel):
    answer: str
    grounded: bool
    used_llm: bool
