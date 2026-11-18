import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("auth_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    const companyId = localStorage.getItem("company_id");
    if (companyId) config.headers["X-Company-ID"] = companyId;
  }
  return config;
});

export const attributionApi = {
  compute: (params: {
    scenario: string;
    attribution_model: string;
    channels?: string[];
    seed?: number;
  }) => api.post("/attribution/compute", params),

  compare: (scenario: string, seed = 42) =>
    api.post(`/attribution/compare?scenario=${encodeURIComponent(scenario)}&seed=${seed}`),

  scenarios: () => api.get("/attribution/scenarios"),
};

export const optimizerApi = {
  solve: (params: {
    target_budget: number;
    channels?: string[];
    scenario: string;
    objective: string;
    gross_margin_pct: number;
    attribution_model: string;
  }) => api.post("/optimizer/solve", params),

  hillCurves: (scenario: string) =>
    api.get(`/optimizer/scenarios/${encodeURIComponent(scenario)}/hill-curves`),
};

export const companyApi = {
  register: (data: {
    company_name: string;
    slug: string;
    industry: string;
    admin_name: string;
    email: string;
    password: string;
  }) => api.post("/companies/register", data),

  getTeam: (companyId: string) => api.get(`/companies/${companyId}/team`),

  inviteMember: (
    companyId: string,
    data: { email: string; role: string; name?: string }
  ) => api.post(`/companies/${companyId}/invite`, data),

  removeMember: (companyId: string, memberId: string) =>
    api.delete(`/companies/${companyId}/team/${memberId}`),
};

export const authApi = {
  login: (email: string, password: string) =>
    api.post("/auth/login", { email, password }),
  logout: () => api.post("/auth/logout"),
};
