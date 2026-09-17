import type { Village, VillageDetail, SafeSite, RelocationPlan, Alert, RiskSummary, LiveHazardFeed } from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const savedScope = () => localStorage.getItem("rakshasetu_region") || "";
const savedDistrict = () => localStorage.getItem("rakshasetu_district") || "";
const savedCity = () => localStorage.getItem("rakshasetu_city") || "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

export const api = {
  regions: {
    states: () => request<any[]>("/api/regions/states"),
    districts: (state: string) => request<any[]>(`/api/regions/districts?state=${encodeURIComponent(state)}`),
    cities: (state: string, district: string) => request<any[]>(`/api/regions/cities?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}`),
  },

  villages: {
    list: (p?: { state?: string; region?: string; district?: string; city?: string; level?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? (p?.region ?? savedScope());
      const d = p?.district !== undefined ? p.district : (p ? "" : savedDistrict());
      const c = p?.city !== undefined ? p.city : (p ? "" : savedCity());

      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      if (c) q.set("city", c);
      if (p?.level) q.set("level", p.level);

      return request<Village[]>(`/api/villages${q.toString() ? `?${q}` : ""}`);
    },
    get: (id: string, p?: { state?: string; district?: string; city?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      const c = p?.city !== undefined ? p.city : savedCity();

      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      if (c) q.set("city", c);

      return request<VillageDetail>(`/api/villages/${id}${q.toString() ? `?${q}` : ""}`);
    },
  },

  safeSites: {
    list: (p?: { state?: string; region?: string; district?: string; city?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? (p?.region ?? savedScope());
      const d = p?.district !== undefined ? p.district : (p ? "" : savedDistrict());
      const c = p?.city !== undefined ? p.city : (p ? "" : savedCity());

      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      if (c) q.set("city", c);

      return request<SafeSite[]>(`/api/safesites${q.toString() ? `?${q}` : ""}`);
    },
    rankFor: (id: string, p?: { state?: string; district?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      return request<any>(`/api/safesites/rank-for/${id}${q.toString() ? `?${q}` : ""}`);
    },
  },

  relocation: {
    plan: (id: string, p?: { state?: string; district?: string; city?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      const c = p?.city !== undefined ? p.city : savedCity();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      if (c) q.set("city", c);
      return request<RelocationPlan>(`/api/relocation/plan/${id}${q.toString() ? `?${q}` : ""}`);
    },
    allPlans: (p?: { state?: string; district?: string; city?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      const c = p?.city !== undefined ? p.city : savedCity();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      if (c) q.set("city", c);
      return request<any[]>(`/api/relocation/plans${q.toString() ? `?${q}` : ""}`);
    },
    route: (v: string, s: string, p?: { state?: string; district?: string; city?: string }) => {
      const q = new URLSearchParams();
      const st = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      const c = p?.city !== undefined ? p.city : savedCity();
      if (st && st !== "India") q.set("state", st);
      if (d) q.set("district", d);
      if (c) q.set("city", c);
      return request<any>(`/api/relocation/route/${v}/${s}${q.toString() ? `?${q}` : ""}`);
    },
  },

  alerts: {
    list: (p?: { state?: string; district?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      return request<Alert[]>(`/api/alerts${q.toString() ? `?${q}` : ""}`);
    },
    summary: (p?: { state?: string; district?: string }) => {
      const q = new URLSearchParams();
      const s = p?.state ?? savedScope();
      const d = p?.district !== undefined ? p.district : savedDistrict();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      return request<Record<string, number>>(`/api/alerts/summary${q.toString() ? `?${q}` : ""}`);
    },
  },

  risk: {
    summary: (state?: string, district?: string, city?: string) => {
      const q = new URLSearchParams();
      const s = state ?? savedScope();
      const d = district !== undefined ? district : savedDistrict();
      const c = city !== undefined ? city : savedCity();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      if (c) q.set("city", c);
      return request<RiskSummary>(`/api/risk/summary${q.toString() ? `?${q}` : ""}`);
    },
  },

  history: {
    get: (id: string) => request<any>(`/api/history/${id}`),
    region: (region: string, district?: string) =>
      request<any>(`/api/history/region/${encodeURIComponent(region)}${district ? `?district=${encodeURIComponent(district)}` : ""}`),
  },

  reports: {
    overview: (state?: string, district?: string) => {
      const q = new URLSearchParams();
      if (state && state !== "India") q.set("state", state);
      if (district) q.set("district", district);
      return request<any>(`/api/reports/overview${q.toString() ? `?${q}` : ""}`);
    },
  },

  live: {
    hazards: (state?: string, district?: string) => {
      const q = new URLSearchParams();
      const s = state ?? savedScope();
      const d = district !== undefined ? district : savedDistrict();
      if (s && s !== "India") q.set("state", s);
      if (d) q.set("district", d);
      return request<LiveHazardFeed>(`/api/live/hazards${q.toString() ? `?${q}` : ""}`);
    },
    news: (state?: string, district?: string) => {
      const q = new URLSearchParams();
      const s = state ?? savedScope();
      const d = district !== undefined ? district : savedDistrict();
      if (s) q.set("state", s);
      if (d) q.set("district", d);
      return request<any>(`/api/live/news${q.toString() ? `?${q}` : ""}`);
    },
  },

  assistant: {
    ask: (question: string) => request<any>("/api/assistant", { method: "POST", body: JSON.stringify({ question }) }),
  },
};

export { savedScope, savedDistrict, savedCity };
