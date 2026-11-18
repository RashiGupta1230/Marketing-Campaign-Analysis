import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Zap, TrendingUp } from "lucide-react";

const stats = [
  { label: "Attribution Models", value: "5" },
  { label: "Budget Optimizer", value: "SLSQP" },
  { label: "Industry Scenarios", value: "3+" },
  { label: "Revenue Conserved", value: "100%" },
];

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-28 pb-20 lg:pt-36 lg:pb-28">
      {/* Backgrounds */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-teal-50/30 -z-10" />
      <div className="absolute -top-32 left-1/2 -translate-x-1/2 w-[900px] h-[600px] rounded-full bg-primary-100/30 blur-3xl -z-10" />
      <div
        className="absolute inset-0 -z-10 opacity-[0.025]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%230F172A'%3E%3Ccircle cx='1' cy='1' r='1'/%3E%3C/g%3E%3C/svg%3E")`,
          backgroundSize: "30px 30px",
        }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-4xl mx-auto">
          {/* Pill badge */}
          <div className="flex justify-center mb-6">
            <span className="inline-flex items-center gap-2 bg-primary-50 border border-primary-200 rounded-full px-4 py-1.5 text-sm text-primary-700 font-medium">
              <Zap className="w-3.5 h-3.5" />
              Markov Chain + Shapley Value MTA · Now live
              <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </div>

          {/* Headline */}
          <h1 className="text-5xl lg:text-6xl xl:text-7xl font-bold text-slate-900 tracking-tight leading-[1.08] mb-6">
            Attribution that{" "}
            <span className="gradient-text-teal">actually</span>{" "}
            understands your funnel
          </h1>

          <p className="text-xl text-slate-500 leading-relaxed mb-10 max-w-2xl mx-auto">
            Multi-touch attribution powered by{" "}
            <strong className="text-slate-700">Markov Chain absorption</strong> and{" "}
            <strong className="text-slate-700">Shapley game theory</strong>. SciPy SLSQP
            budget optimizer. Built for performance-obsessed marketing teams.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Button size="xl" asChild>
              <Link href="/auth/register" className="gap-2">
                Start free trial <ArrowRight className="w-4 h-4" />
              </Link>
            </Button>
            <Button size="xl" variant="outline" asChild>
              <Link href="/auth/login?demo=true">View live demo →</Link>
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 max-w-3xl mx-auto mb-16">
            {stats.map((s) => (
              <div key={s.label} className="bg-white rounded-xl border border-slate-200 px-5 py-4 shadow-sm">
                <div className="text-2xl font-bold text-slate-900 mb-0.5">{s.value}</div>
                <div className="text-xs text-slate-500 font-medium">{s.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Dashboard mock-up */}
        <div className="relative max-w-5xl mx-auto">
          <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent z-10 pointer-events-none" />
          <div className="bg-slate-900 rounded-2xl shadow-2xl ring-1 ring-slate-700/50 overflow-hidden">
            {/* Browser chrome */}
            <div className="flex items-center gap-2 px-4 py-3 bg-slate-800 border-b border-slate-700/60">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-400/70" />
                <div className="w-3 h-3 rounded-full bg-yellow-400/70" />
                <div className="w-3 h-3 rounded-full bg-green-400/70" />
              </div>
              <div className="flex-1 mx-4">
                <div className="bg-slate-700 rounded-md px-3 py-1 text-xs text-slate-400 max-w-xs">
                  app.attributeiq.com/dashboard/acme-corp
                </div>
              </div>
            </div>

            {/* App shell */}
            <div className="flex h-[340px]">
              {/* Sidebar */}
              <div className="w-44 bg-slate-900 border-r border-slate-800 p-3 flex flex-col gap-1 shrink-0">
                <div className="flex items-center gap-2 px-2 py-3 mb-1">
                  <div className="w-6 h-6 rounded-md bg-primary-600 flex items-center justify-center">
                    <TrendingUp className="w-3 h-3 text-white" />
                  </div>
                  <span className="text-white font-bold text-sm">AttributeIQ</span>
                </div>
                {["Overview", "Reports", "Attribution", "Optimizer", "Team", "Settings"].map((item, i) => (
                  <div key={item}
                    className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                      i === 0 ? "bg-primary-600 text-white" : "text-slate-400"
                    }`}>
                    {item}
                  </div>
                ))}
              </div>

              {/* Main */}
              <div className="flex-1 bg-slate-50 p-4 overflow-hidden">
                <div className="text-xs font-semibold text-slate-500 mb-3 uppercase tracking-wider">
                  📈 Performance Actuals — Nov 2026
                </div>
                {/* KPI cards */}
                <div className="grid grid-cols-4 gap-2 mb-3">
                  {[
                    { l: "Media Spend", v: "₹8.0L", d: "+4.1%", g: false },
                    { l: "Revenue", v: "₹21.4L", d: "+8.2%", g: true },
                    { l: "Conversions", v: "3,420", d: "+6.3%", g: true },
                    { l: "ROAS", v: "2.67x", d: "+0.18x", g: true },
                  ].map((k) => (
                    <div key={k.l} className="bg-white rounded-lg p-2.5 border border-slate-200 shadow-sm">
                      <div className="text-[9px] text-slate-400 font-medium mb-1 uppercase">{k.l}</div>
                      <div className="text-sm font-bold text-slate-900">{k.v}</div>
                      <div className={`text-[9px] font-semibold mt-0.5 ${k.g ? "text-emerald-600" : "text-slate-500"}`}>{k.d}</div>
                    </div>
                  ))}
                </div>
                {/* Charts row */}
                <div className="grid grid-cols-5 gap-2 h-[148px]">
                  {/* ROAS bar chart */}
                  <div className="col-span-2 bg-white rounded-lg border border-slate-200 p-3">
                    <div className="text-[9px] font-semibold text-slate-500 mb-2 uppercase">ROAS by Channel</div>
                    <div className="space-y-1.5">
                      {[
                        { ch: "Email", w: "88%", v: "3.8x" },
                        { ch: "Search", w: "72%", v: "3.1x" },
                        { ch: "Social", w: "58%", v: "2.5x" },
                        { ch: "Display", w: "33%", v: "1.4x" },
                      ].map((b) => (
                        <div key={b.ch} className="flex items-center gap-2">
                          <div className="text-[8px] text-slate-500 w-9 text-right shrink-0">{b.ch}</div>
                          <div className="flex-1 bg-slate-100 rounded-full h-1.5">
                            <div className="bg-primary-500 h-1.5 rounded-full" style={{ width: b.w }} />
                          </div>
                          <div className="text-[8px] text-slate-700 font-bold w-5 shrink-0">{b.v}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                  {/* Attribution comparison */}
                  <div className="col-span-2 bg-white rounded-lg border border-slate-200 p-3">
                    <div className="text-[9px] font-semibold text-slate-500 mb-2 uppercase">Attribution Models</div>
                    <div className="flex items-end gap-1 h-20">
                      {[
                        { h: 60, c: "#38BDF8", l: "FC" },
                        { h: 40, c: "#34D399", l: "LC" },
                        { h: 52, c: "#FBBF24", l: "Lin" },
                        { h: 78, c: "#0D9488", l: "Mrk" },
                        { h: 68, c: "#A78BFA", l: "Shp" },
                      ].map((b) => (
                        <div key={b.l} className="flex-1 flex flex-col items-center gap-1">
                          <div className="w-full rounded-sm" style={{ height: `${b.h}%`, background: b.c }} />
                          <div className="text-[7px] text-slate-400">{b.l}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                  {/* AI rec */}
                  <div className="col-span-1 bg-gradient-to-b from-primary-50 to-teal-50 rounded-lg border border-primary-100 p-2.5 flex flex-col justify-center">
                    <div className="text-[8px] font-bold text-slate-800 mb-1">🎯 AI Rec</div>
                    <div className="text-[8px] text-primary-700 font-semibold mb-1">+₹1.2L rev</div>
                    <div className="text-[7px] text-slate-500 leading-snug">
                      Shift ₹80K Display → Email (Hill curve)
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

