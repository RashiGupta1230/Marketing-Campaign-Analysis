"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { TrendingUp, Menu, X, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

const navLinks = [
  { label: "Platform", href: "#features" },
  { label: "Methodology", href: "#methodology" },
  { label: "Pricing", href: "#pricing" },
];

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 16);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }, []);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        scrolled
          ? "bg-white/90 backdrop-blur-md border-b border-slate-200/80 shadow-sm"
          : "bg-transparent"
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-slate-900 flex items-center justify-center shadow-sm group-hover:bg-blue-600 transition-colors">
            <TrendingUp className="w-4 h-4 text-white" />
          </div>
          <span className="font-extrabold text-slate-900 text-lg tracking-tight">
            Attribute<span className="text-blue-600">IQ</span>
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-1 bg-slate-100/70 p-1 rounded-full border border-slate-200/60">
          {navLinks.map((l) => (
            <Link
              key={l.label}
              href={l.href}
              className="px-4 py-1.5 text-xs text-slate-600 hover:text-slate-900 hover:bg-white rounded-full transition-all font-medium"
            >
              {l.label}
            </Link>
          ))}
        </nav>

        <div className="hidden md:flex items-center gap-2.5">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/auth/login">Log in</Link>
          </Button>
          <Button size="sm" asChild>
            <Link href="/auth/register" className="gap-1.5">
              Get started <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </Button>
        </div>

        <button
          className="md:hidden p-2 rounded-lg text-slate-700 hover:bg-slate-100"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {mobileOpen && (
        <div className="md:hidden bg-white border-b border-slate-200 px-4 pb-5 pt-3 space-y-2">
          {navLinks.map((l) => (
            <Link
              key={l.label}
              href={l.href}
              className="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg font-medium"
              onClick={() => setMobileOpen(false)}
            >
              {l.label}
            </Link>
          ))}
          <div className="mt-3 flex flex-col gap-2 pt-2 border-t border-slate-100">
            <Button variant="outline" className="w-full" asChild>
              <Link href="/auth/login">Log in</Link>
            </Button>
            <Button className="w-full" asChild>
              <Link href="/auth/register">Get started free</Link>
            </Button>
          </div>
        </div>
      )}
    </header>
  );
}
