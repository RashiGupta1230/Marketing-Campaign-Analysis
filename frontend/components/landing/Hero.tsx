import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Zap, CheckCircle2, ShieldCheck, BarChart3, TrendingUp, Sparkles } from "lucide-react";

const stats = [
  { label: "MTA Models", value: "5 Models" },
  { label: "Budget Solver", value: "SciPy SLSQP" },
  { label: "Revenue Invariant", value: "100% Conserved" },
  { label: "Industry Benchmarks", value: "B2C · SaaS · EdTech" },
];

const trustedCompanies = [
  "HYPERSCALE", "SCALEFLOW", "NEXUSAIR", "SYNTHETIX", "DATACORE", "ALTIMA"
];

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-28 pb-16 lg:pt-36 lg:pb-24 bg-gradient-to-b from-slate-50 via-white to-slate-50">
      {/* Background Subtle Mesh */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-blue-100/40 rounded-full blur-3xl -z-10 pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-4xl mx-auto">
          {/* Pill Badge */}
          <div className="inline-flex items-center gap-2 bg-white border border-slate-200/90 shadow-sm rounded-full px-3.5 py-1 text-xs text-slate-800 font-semibold mb-6 hover:border-blue-300 transition-colors">
            <span className="flex h-2 w-2 rounded-full bg-blue-600 animate-pulse" />
            <span>Multi-Touch Attribution & Budget Optimization Platform</span>
            <span className="text-slate-300">|</span>
            <span className="text-blue-600 inline-flex items-center gap-1 font-medium">
              2026 Engine <ArrowRight className="w-3 h-3" />
            </span>
          </div>

          {/* Heading */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.08] mb-6">
            Stop guessing spend.{" "}
            <span className="gradient-text-blue">
              Mathematically prove
            </span>{" "}
            every conversion.
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl text-slate-600 leading-relaxed mb-10 max-w-2xl mx-auto">
            Replace flawed last-click attribution with <strong className="text-slate-900 font-semibold">Markov Chain absorption</strong> and <strong className="text-slate-900 font-semibold">Shapley game theory</strong>. Optimize channel spend with SciPy SLSQP.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 mb-14">
            <Button size="xl" asChild>
              <Link href="/auth/register" className="gap-2">
                Launch Workspace <ArrowRight className="w-4 h-4" />
              </Link>
            </Button>
            <Button size="xl" variant="outline" asChild>
              <Link href="/auth/login?demo=true">
                Explore Live Demo →
              </Link>
            </Button>
          </div>

          {/* Micro Value Props */}
          <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-slate-500 font-medium mb-16">
            <span className="inline-flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-blue-600" /> Zero tracking black-box
            </span>
            <span className="inline-flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-blue-600" /> SHA-256 Governance ledger
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-blue-600" /> Real-time SLSQP simulation
            </span>
          </div>
        </div>

        {/* Dashboard Preview Mockup (Deel/Toptal 2026 Style) */}
        <div className="relative mx-auto max-w-5xl rounded-2xl border border-slate-200/90 bg-white shadow-2xl p-3 sm:p-4 mb-20 hover:border-blue-200 transition-all duration-300">
          <div className="rounded-xl bg-slate-900 text-white overflow-hidden border border-slate-800">
            {/* Mock Top bar */}
            <div className="h-10 bg-slate-950 px-4 flex items-center justify-between border-b border-slate-800 text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
                <span className="ml-2 font-mono text-[11px] text-slate-400">attributeiq.com/dashboard/enterprise-b2c</span>
              </div>
              <span className="font-semibold text-emerald-400 bg-emerald-950/80 border border-emerald-800/80 px-2 py-0.5 rounded text-[10px]">
                ● Markov Engine Active
              </span>
            </div>

            {/* Mock Content */}
            <div className="p-6 bg-slate-900 grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700/60">
                <p className="text-xs text-slate-400 mb-1">Total Media Spend</p>
                <p className="text-xl font-bold text-white">₹8,00,000</p>
                <p className="text-[11px] text-slate-400 mt-1">Across 5 channels</p>
              </div>
              <div className="bg-slate-800/80 p-4 rounded-xl border border-blue-500/60 ring-1 ring-blue-500/30">
                <p className="text-xs text-blue-400 font-semibold mb-1">Attributed Revenue</p>
                <p className="text-xl font-bold text-white">₹21,40,000</p>
                <p className="text-[11px] text-emerald-400 mt-1">✓ 100% Invariant Conserved</p>
              </div>
              <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700/60">
                <p className="text-xs text-slate-400 mb-1">Blended ROAS</p>
                <p className="text-xl font-bold text-white">2.68x</p>
                <p className="text-[11px] text-emerald-400 mt-1">▲ +0.24x vs Baseline</p>
              </div>
              <div className="bg-slate-800/80 p-4 rounded-xl border border-slate-700/60">
                <p className="text-xs text-slate-400 mb-1">SLSQP Recommendation</p>
                <p className="text-xs font-semibold text-blue-300 mt-1">Shift ₹80k Display → Email</p>
                <p className="text-[11px] text-emerald-400 mt-1">+₹1.2L projected lift</p>
              </div>
            </div>
          </div>
        </div>

        {/* Trusted By Companies Marquee Banner */}
        <div className="pt-4 border-t border-slate-200/80">
          <p className="text-center text-xs font-semibold uppercase tracking-wider text-slate-400 mb-6">
            Trusted by growth marketing teams & performance agencies
          </p>
          <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-14 opacity-60 grayscale hover:grayscale-0 transition-all duration-300">
            {trustedCompanies.map((c) => (
              <span key={c} className="text-sm font-extrabold tracking-widest text-slate-600 hover:text-blue-600 transition-colors">
                {c}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
