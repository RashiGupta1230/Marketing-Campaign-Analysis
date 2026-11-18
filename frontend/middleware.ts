import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Edge middleware — redirect unauthenticated users away from /dashboard/*.
 * Token is read from localStorage via a client cookie set at login.
 * Phase 3 upgrade: use httpOnly cookie here instead.
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Protect dashboard routes
  if (pathname.startsWith("/dashboard")) {
    const token = request.cookies.get("aiq_token")?.value;
    if (!token) {
      const loginUrl = new URL("/auth/login", request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  // Redirect logged-in users away from auth pages
  if (pathname.startsWith("/auth")) {
    const token = request.cookies.get("aiq_token")?.value;
    const slug = request.cookies.get("aiq_company_slug")?.value;
    if (token && slug && !pathname.includes("logout")) {
      return NextResponse.redirect(new URL(`/dashboard/${slug}`, request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/auth/:path*"],
};
