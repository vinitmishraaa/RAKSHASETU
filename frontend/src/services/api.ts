import type { Village, VillageDetail, SafeSite, RelocationPlan, Alert, RiskSummary, LiveHazardFeed } from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { headers: { "Content-Type": "application/json" }, ...init });
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  return res.json();
}

export const api = {
  regions: {
    states: () => request<any[]>("/api/regions/states"),
    districts: (state: string) => request<any[]>(`/api/regions/districts?state=${encodeURIComponent(state)}`),
  },
  villages: {
    list: (params?: { state?: string; region?: string; district?: string; level?: string }) => {
      const q = new URLSearchParams();
      if (params?.state || params?.region) q.set("state", params.state || params.region || "");
      if (params?.district) q.set("district", params.district);
      if (params?.level) q.set("level", params.level);
      return request<Village[]>(`/api/villages${q.toString() ? `?${q.toString()}` : ""}`);
    },
    get: (id: string, params?: { state?: string; district?: string }) => request<VillageDetail>(`/api/villages/${id}?${new URLSearchParams(params as Record<string, string>).toString()}`),
  },
  safeSites: {
    list: (params?: { state?: string; region?: string; district?: string }) => {
      const q = new URLSearchParams();
      if (params?.state || params?.region) q.set("state", params.state || params.region || "");
      if (params?.district) q.set("district", params.district);
      return request<SafeSite[]>(`/api/safesites${q.toString() ? `?${q.toString()}` : ""}`);
    },
    rankFor: (villageId: string, params?: { state?: string; district?: string }) => request<any>(`/api/safesites/rank-for/${villageId}?${new URLSearchParams(params as Record<string, string>).toString()}`),
  },
  relocation: {
    plan: (villageId: string) => request<RelocationPlan>(`/api/relocation/plan/${villageId}`),
    allPlans: () => request<any[]>("/api/relocation/plans"),
    route: (villageId: string, siteId: string) => request<any>(`/api/relocation/route/${villageId}/${siteId}`),
  },
  alerts: {
    list: () => request<Alert[]>("/api/alerts"),
    summary: () => request<Record<string, number>>("/api/alerts/summary"),
  },
  risk: { summary: () => request<RiskSummary>("/api/risk/summary") },
  history: {
    get: (villageId: string) => request<any>(`/api/history/${villageId}`),
    region: (region: string, district?: string) => request<any>(`/api/history/region/${encodeURIComponent(region)}${district ? `?district=${encodeURIComponent(district)}` : ""}`),
  },
  reports: { overview: (region?: string) => request<any>(`/api/reports/overview${region ? `?region=${encodeURIComponent(region)}` : ""}`) },
  live: {
    hazards: (region?: string) => request<LiveHazardFeed>(`/api/live/hazards${region ? `?region=${encodeURIComponent(region)}` : ""}`),
    news: (region: string) => request<any>(`/api/live/news?region=${encodeURIComponent(region)}`),
  },
  assistant: {
    ask: (question: string) => request<{ answer: string; grounded: boolean; used_llm: boolean; provider?: string }>("/api/assistant", { method: "POST", body: JSON.stringify({ question }) }),
  },
};
