/**
 * Auth helpers — token + session stored in localStorage.
 * Phase 3 upgrade: move to httpOnly cookie via route handler.
 */

const TOKEN_KEY = "aiq_token";
const COMPANY_KEY = "aiq_company_slug";
const COMPANY_ID_KEY = "aiq_company_id";
const ROLE_KEY = "aiq_role";
const NAME_KEY = "aiq_name";

export const auth = {
  setSession(data: {
    access_token: string;
    company_slug: string;
    company_id: string;
    role: string;
    user_name: string;
  }) {
    localStorage.setItem(TOKEN_KEY, data.access_token);
    localStorage.setItem(COMPANY_KEY, data.company_slug);
    localStorage.setItem(COMPANY_ID_KEY, data.company_id);
    localStorage.setItem(ROLE_KEY, data.role);
    localStorage.setItem(NAME_KEY, data.user_name);
  },

  getToken: () => (typeof window !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null),
  getSlug: () => (typeof window !== "undefined" ? localStorage.getItem(COMPANY_KEY) : null),
  getCompanyId: () => (typeof window !== "undefined" ? localStorage.getItem(COMPANY_ID_KEY) : null),
  getRole: () => (typeof window !== "undefined" ? localStorage.getItem(ROLE_KEY) : null),
  getName: () => (typeof window !== "undefined" ? localStorage.getItem(NAME_KEY) : null),

  isLoggedIn: () => !!(typeof window !== "undefined" && localStorage.getItem(TOKEN_KEY)),

  clear() {
    [TOKEN_KEY, COMPANY_KEY, COMPANY_ID_KEY, ROLE_KEY, NAME_KEY].forEach((k) =>
      localStorage.removeItem(k)
    );
  },
};
