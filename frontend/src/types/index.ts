export type RiskLevel = "CRITICAL" | "HIGH" | "MODERATE" | "LOW";

export interface Village {
  id: string; name: string; district?: string | null; state?: string | null; region?: string;
  lat: number; lng: number; population: number | null; population_source?: string | null;
  risk_score: number; hazard?: number | null; exposure?: number | null; vulnerability?: number | null; accessibility?: number | null;
  level: RiskLevel; color?: string; source?: string; source_url?: string; weather?: { temperature_c?: number | null; precipitation_mm?: number | null; wind_speed_kmh?: number | null };
  nearest_earthquake_km?: number | null; risk_model?: string; observed_at?: string; data_status?: string;
}

export interface VillageDetail extends Village {
  households?: number | null; children?: number | null; elderly?: number | null; other_vulnerable?: number | null;
  flood_hazard?: number | null; landslide_hazard?: number | null; cyclone_hazard?: number | null; rainfall_mm_month?: number | null;
  reasons: string[]; recommended_action: string; history: { year: number; hazard: string; severity: string }[]; rainfall_trend: number[];
}

export interface SafeSite {
  id: string; name: string; region?: string; lat: number; lng: number;
  capacity: number | null; current_occupancy: number | null; available_capacity: number | null;
  hazard_risk: number | null; infrastructure_score: number | null; facilities: string[];
  verified?: boolean; source?: string; source_url?: string; note?: string;
}

export interface SiteSuitability { site_id: string; site_name: string; suitability: number; distance_km: number; available_capacity: number; road_access: "GOOD" | "MODERATE" | "POOR"; hazard_risk: number; }
export interface RelocationAllocation { site_id: string; site_name: string; people: number; }
export interface RelocationPlan { village_id: string; village_name: string; population: number | null; best_site: SiteSuitability | null; ranked_sites: SiteSuitability[]; allocations: RelocationAllocation[]; fully_covered: boolean; reason: string | null; }
export interface Alert { village_id: string; village_name: string; district?: string; state?: string; lat?: number; lng?: number; population?: number; level: "CRITICAL" | "HIGH" | "WARNING"; risk_score: number; message: string; action?: string; source?: string; }
export interface LiveHazard { id: string; type: "Earthquake" | "Fire Hotspot" | string; title?: string; lat: number; lng: number; magnitude?: number | null; confidence?: string | number; frp?: number | null; time?: number | string | null; severity: "CRITICAL" | "HIGH" | "MODERATE" | "LOW"; source: string; url?: string; detail?: string; }
export interface LiveHazardFeed { updated_at: string; items: LiveHazard[]; sources: { name: string; status: string; count?: number }[]; note?: string; }
export interface RiskSummary { total_villages: number; counts: Record<RiskLevel, number>; population_at_risk: number | null; known_population_records?: number; data_status?: string; note?: string; }
