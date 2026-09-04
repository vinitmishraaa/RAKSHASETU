export type RiskLevel = "CRITICAL" | "HIGH" | "MODERATE" | "LOW";

export interface Village {
  id: string;
  name: string;
  district: string;
  state: string;
  lat: number;
  lng: number;
  population: number;
  risk_score: number;
  hazard: number;
  exposure: number;
  vulnerability: number;
  accessibility: number;
  level: RiskLevel;
  color: string;
}

export interface VillageDetail extends Village {
  households: number;
  children: number;
  elderly: number;
  other_vulnerable: number;
  flood_hazard: number;
  landslide_hazard: number;
  cyclone_hazard: number;
  rainfall_mm_month: number;
  reasons: string[];
  recommended_action: string;
  history: { year: number; hazard: string; severity: string }[];
  rainfall_trend: number[];
}

export interface SafeSite {
  id: string;
  name: string;
  lat: number;
  lng: number;
  capacity: number;
  current_occupancy: number;
  available_capacity: number;
  hazard_risk: number;
  infrastructure_score: number;
  facilities: string[];
}

export interface SiteSuitability {
  site_id: string;
  site_name: string;
  suitability: number;
  distance_km: number;
  available_capacity: number;
  road_access: "GOOD" | "MODERATE" | "POOR";
  hazard_risk: number;
}

export interface RelocationAllocation {
  site_id: string;
  site_name: string;
  people: number;
}

export interface RelocationPlan {
  village_id: string;
  village_name: string;
  population: number;
  best_site: SiteSuitability | null;
  ranked_sites: SiteSuitability[];
  allocations: RelocationAllocation[];
  fully_covered: boolean;
  reason: string | null;
}

export interface Alert {
  village_id: string;
  village_name: string;
  level: "CRITICAL" | "HIGH" | "WARNING";
  risk_score: number;
  message: string;
}

export interface RiskSummary {
  total_villages: number;
  counts: Record<RiskLevel, number>;
  population_at_risk: number;
}
