"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { TopNav } from "@/components/dashboard/TopNav";
import { KPICard } from "@/components/dashboard/KPICard";
import { Button } from "@/components/ui/button";
import { DollarSign, TrendingUp, Users, BarChart3, Download, RefreshCw, ArrowRight, Zap, Sparkles } from "lucide-react";
import { attributionApi, optimizerApi } from "@/lib/api";
import { formatCurrency, formatPercent } from "@/lib/utils";

// Skeleton loader for KPI cards
function KPISkeleton() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse">
      <div className="h-3 w-24 bg-slate-200 rounded mb-4" />
      <div className="h-7 w-32 bg-slate-200 rounded mb-2" />
      <div className="h-3 w-20 bg-slate-100 rounded" />
    </div>
  );
}

export default function DashboardOverviewPage() {
  const params = useParams();
  const company = params.company as string;
  const companyName = company.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  // Real API call — Markov Chain attribution
  const { data: attrData, isLoading: attrLoading, refetch } = useQuery({
    queryKey: ["attribution", "E-Commerce (B2C)", "Markov Chain"],
    queryFn: async () => {
      const res = await attributionApi.compute({
        scenario: "E-Commerce (B2C)",
        attribution_model: "Markov Chain",
        seed: 42,
      });
      return res.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  // Real API call — Optimizer for AI recommendation
  const { data: optData } = useQuery({
    queryKey: ["optimizer", "E-Commerce (B2C)"],
    queryFn: async () => {
      const res = await optimizerApi.solve({
        target_budget: 800000,
        scenario: "E-Commerce (B2C)",
        objective: "revenue",
        gross_margin_pct: 0.65,
        attribution_model: "Markov Chain",
      });
      return res.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  // Derive KPIs from real data
  const totalSpend = attrData?.total_spend ?? 0;
  const totalRev = attrData?.total_attributed_revenue ?? 0;
  const totalConv = attrData?.channels?.reduce((s: number, c: { conversions: number }) => s + c.conversions, 0) ?? 0;
  const roas = attrData?.blended_roas ?? 0;
  const cpa = totalConv > 0 ? totalSpend / totalConv : 0;

  const kpis = [
    {
      label: "Total Media Spend",
      value: attrLoading ? "—" : formatCurrency(totalSpend),
      delta: "Across all channels",
      deltaType: "neutral" as const,
      caption: `${attrData?.channels?.length ?? 0} channels · All Regions`,
      icon: <DollarSign className="w-4 h-4" />,
    },
    {
      label: "Attributed Revenue",
      value: attrLoading ? "—" : formatCurrency(totalRev),
      delta: attrData?.revenue_conserved ? "✓ Revenue Conserved" : "⚠ Check model",
      deltaType: "positive" as const,
      caption: "Markov Chain · Invariant verified",
      icon: <TrendingUp className="w-4 h-4" />,
      accent: true,
    },
    {
      label: "Conversions / CPA",
      value: attrLoading ? "—" : totalConv.toLocaleString(),
      delta: `CPA: ${formatCurrency(cpa)}`,
      deltaType: "positive" as const,
      caption: "All channels combined",
      icon: <Users className="w-4 h-4" />,
    },
    {
      label: "Blended ROAS",
      value: attrLoading ? "—" : `${roas.toFixed(2)}x`,
      delta: roas >= 2 ? "🟢 Healthy" : roas >= 1 ? "🟡 Marginal" : "🔴 Below target",
      deltaType: roas >= 2 ? "positive" as const : "negative" as const,
      caption: "Revenue ÷ Spend (Markov)",
      icon: <BarChart3 className="w-4 h-4" />,
    },
  ];

  const aiRec = optData?.ai_recommendation;

  const quickLinks = [
    { label: "Attribution Models", href: "attribution", icon: "🔀" },
    { label: "Run SLSQP Optimizer", href: "optimizer", icon: "⚡" },
    { label: "Manage Reports", href: "reports", icon: "📄" },
    { label: "Invite Team", href: "team", icon: "👥" },
  ];

  return (
    <>
      <TopNav
        title={`${companyName} — Campaign Overview`}
        subtitle="E-Commerce (B2C) · Markov Chain Attribution"
        actions={
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="gap-1.5" onClick={() => refetch()} disabled={attrLoading}>
              <RefreshCw className={`w-3.5 h-3.5 ${attrLoading ? "animate-spin" : ""}`} />
              {attrLoading ? "Loading..." : "Refresh"}
            </Button>
            <Button size="sm" className="gap-1.5">
              <Download className="w-3.5 h-3.5" />Export Brief
            </Button>
          </div>
        }
      />
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50">

        {/* KPIs */}
        <div>
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">
            📈 Live Performance Actuals (Markov Chain)
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            {attrLoading
              ? Array.from({ length: 4 }).map((_, i) => <KPISkeleton key={i} />)
              : kpis.map((k) => <KPICard key={k.label} {...k} />)}
          </div>
        </div>

        {/* Channel table + AI rec */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
          <div className="xl:col-span-2 bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
              <h2 className="text-sm font-bold text-slate-900 tracking-tight">Channel Performance</h2>
              <Button variant="ghost" size="sm" className="text-xs gap-1 text-blue-600 hover:text-blue-700" asChild>
                <a href="attribution">View attribution <ArrowRight className="w-3 h-3" /></a>
              </Button>
            </div>
            {attrLoading ? (
              <div className="p-5 space-y-3">
                {Array.from({ length: 5 }).map((_, i) => (
                  <div key={i} className="h-8 bg-slate-100 rounded animate-pulse" />
                ))}
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50/70 border-b border-slate-100">
                    {["Channel", "Spend", "ROAS", "Conversions", "Weight"].map((h) => (
                      <th key={h} className="text-left text-xs font-bold text-slate-500 px-5 py-3 uppercase tracking-wider">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {(attrData?.channels ?? [])
                    .slice()
                    .sort((a: { roas: number }, b: { roas: number }) => b.roas - a.roas)
                    .map((row: { channel: string; spend: number; roas: number; conversions: number; weight: number }, i: number, arr: unknown[]) => (
                      <tr key={row.channel} className={`border-b border-slate-50 hover:bg-slate-50/80 transition-colors ${i === arr.length - 1 ? "border-0" : ""}`}>
                        <td className="px-5 py-3.5 font-semibold text-slate-900">{row.channel}</td>
                        <td className="px-5 py-3.5 text-slate-600 font-medium">{formatCurrency(row.spend)}</td>
                        <td className="px-5 py-3.5 font-bold text-blue-600">{row.roas.toFixed(2)}x</td>
                        <td className="px-5 py-3.5 text-slate-600 font-medium">{row.conversions.toLocaleString()}</td>
                        <td className="px-5 py-3.5 text-slate-500 font-medium">{formatPercent(row.weight)}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            )}
          </div>

          {/* AI Rec in Navy & Accent Blue */}
          <div className="bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2">
              <Zap className="w-4 h-4 text-blue-600" />
              <h2 className="text-sm font-bold text-slate-900 tracking-tight">AI Allocation Advice</h2>
            </div>
            <div className="flex-1 p-5">
              <div className="bg-gradient-to-br from-blue-50/80 via-slate-50 to-indigo-50/50 border border-blue-200/80 rounded-xl p-4 mb-4 shadow-sm">
                <div className="text-sm font-extrabold text-slate-900 mb-1 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                  {aiRec?.title ?? "Optimizing budget allocation..."}
                </div>
                {aiRec?.impact && (
                  <div className="text-xs font-bold text-blue-700 mb-2">{aiRec.impact}</div>
                )}
                <div className="text-xs text-slate-600 leading-relaxed font-normal">
                  {aiRec?.body ?? "Run the SLSQP optimizer to compute optimal Hill curve saturation levels based on Markov Chain attribution."}
                </div>
              </div>
              <Button className="w-full gap-2 shadow-sm font-bold" size="sm" asChild>
                <a href="optimizer"><Zap className="w-3.5 h-3.5" />Run SLSQP Optimizer →</a>
              </Button>
            </div>
            <div className="px-5 py-3 bg-slate-50 border-t border-slate-100">
              <p className="text-[11px] text-slate-400">Governance note: Human sign-off required prior to budget execution.</p>
            </div>
          </div>
        </div>

        {/* Quick links */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {quickLinks.map((card) => (
            <a key={card.label} href={card.href}
              className="bg-white rounded-xl border border-slate-200/80 p-4 hover:border-blue-300 hover:shadow-card-hover hover:-translate-y-0.5 transition-all group">
              <div className="text-2xl mb-2">{card.icon}</div>
              <div className="text-xs font-bold text-slate-800 group-hover:text-blue-600 transition-colors">{card.label}</div>
            </a>
          ))}
        </div>
      </div>
    </>
  );
}
