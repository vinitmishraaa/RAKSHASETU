export type RiskLevel = "CRITICAL" | "HIGH" | "MODERATE" | "LOW";
export type RelocationTier = "IMMEDIATE" | "SHORT_TERM" | "MEDIUM_TERM";

export interface Village {
  id: string;
  name: string;
  district?: string | null;
  state?: string | null;
  region?: string;
  city?: string | null;
  lat: number;
  lng: number;
  population: number | null;
  population_source?: string | null;
  risk_score: number;
  risk_components?: Record<string, number>;
  hazard?: number | null;
  exposure?: number | null;
  vulnerability?: number | null;
  accessibility?: number | null;
  level: RiskLevel;
  color?: string;
  source?: string;
  source_url?: string;
  weather?: {
    temperature_c?: number | null;
    precipitation_mm?: number | null;
    wind_speed_kmh?: number | null;
  };
  nearest_earthquake_km?: number | null;
  nearest_earthquake?: {
    magnitude?: number | null;
    place?: string;
    time?: number | null;
  } | null;
  risk_model?: string;
  observed_at?: string;
  data_status?: string;
  households?: number | null;
  children?: number | null;
  elderly?: number | null;
  other_vulnerable?: number | null;
  flood_hazard?: number | null;
  landslide_hazard?: number | null;
  cyclone_hazard?: number | null;
  coastal_erosion_hazard?: number | null;
  cloudburst_hazard?: number | null;
  rainfall_mm_month?: number | null;
  reasons?: string[];
  recommended_action?: string;
  history?: { year: number; hazard: string; severity: string }[];
  rainfall_trend?: number[];
  is_red_zone?: boolean;
  red_zone_declaration?: string;
  relocation_tier?: RelocationTier;
  relocation_horizon?: string;
  primary_hazard_trigger?: string;
}

export interface VillageDetail extends Village {
  reasons: string[];
  recommended_action: string;
  history: { year: number; hazard: string; severity: string }[];
  rainfall_trend: number[];
}

export interface SafeSite {
  id: string;
  name: string;
  region?: string;
  state?: string | null;
  district?: string | null;
  city?: string | null;
  lat: number;
  lng: number;
  capacity: number | null;
  current_occupancy: number | null;
  available_capacity: number | null;
  hazard_risk: number | null;
  infrastructure_score: number | null;
  facilities: string[];
  verified?: boolean;
  source?: string;
  source_url?: string;
  note?: string;
}

export interface SiteSuitability {
  site_id: string;
  site_name: string;
  suitability?: number;
  distance_km: number;
  available_capacity?: number | null;
  road_access?: "GOOD" | "MODERATE" | "POOR" | "UNVERIFIED";
  hazard_risk?: number | null;
  facilities?: string[];
}

export interface RelocationAllocation {
  site_id: string;
  site_name: string;
  people: number;
  site_capacity?: number;
  post_occupancy?: number;
  utilization_pct?: number;
}

export interface CarryingCapacityAssessment {
  primary_site_id: string;
  primary_site_name: string;
  total_capacity: number;
  pre_occupancy: number;
  available_headroom: number;
  evacuee_demand: number;
  post_intake_occupancy: number;
  stress_level_pct: number;
  carrying_capacity_status: "SAFE_WITHIN_HEADROOM" | "ELEVATED_HEADROOM_STRESS" | "OVERLOAD_PREVENTED_SPLIT_ROUTED" | string;
  overcrowding_mitigation: string;
  total_regional_capacity?: number;
  total_regional_available?: number;
}

export interface RelocationPlan {
  village_id: string;
  village_name: string;
  population: number | null;
  best_site: any | null;
  ranked_sites: any[];
  allocations: RelocationAllocation[];
  fully_covered: boolean;
  reason: string | null;
  carrying_capacity_assessment?: CarryingCapacityAssessment | null;
  relocation_tier?: RelocationTier;
  relocation_horizon?: string;
  is_red_zone?: boolean;
  red_zone_declaration?: string;
  primary_hazard_trigger?: string;
  guided_flow?: any[];
  advisory_note?: string;
  scope?: { state?: string | null; region?: string | null; district?: string | null; city?: string | null };
}

export interface Alert {
  village_id: string;
  village_name: string;
  district?: string;
  state?: string;
  lat?: number | null;
  lng?: number | null;
  population?: number | null;
  level: "CRITICAL" | "HIGH" | "WARNING" | "MODERATE" | "LOW";
  risk_score: number;
  message: string;
  action?: string;
  source?: string;
  time?: string | number | null;
  url?: string;
}

export interface LiveHazard {
  id: string;
  type: "Earthquake" | "Fire Hotspot" | string;
  title?: string;
  lat?: number | null;
  lng?: number | null;
  magnitude?: number | null;
  confidence?: string | number;
  frp?: number | null;
  time?: number | string | null;
  severity: "CRITICAL" | "HIGH" | "MODERATE" | "LOW";
  source: string;
  url?: string;
  detail?: string;
}

export interface LiveHazardFeed {
  updated_at: string;
  items: LiveHazard[];
  sources: { name: string; status: string; count?: number }[];
  note?: string;
}

export interface RiskSummary {
  total_villages: number;
  counts: Record<RiskLevel, number>;
  red_zones_count?: number;
  relocation_tiers?: Record<string, number>;
  population_by_tier?: Record<string, number>;
  population_at_risk: number | null;
  known_population_records?: number;
  average_risk_score?: number;
  hazard_breakdown_avg?: Record<string, number>;
  data_status?: string;
  note?: string;
}
