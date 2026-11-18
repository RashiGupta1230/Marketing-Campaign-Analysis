"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { TopNav } from "@/components/dashboard/TopNav";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { optimizerApi } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { Zap, TrendingUp, TrendingDown, Loader2 } from "lucide-react";

export default function OptimizerPage() {
  const params = useParams();
  const [budget, setBudget] = useState(800000);
  const [inputBudget, setInputBudget] = useState("800000");

  const { data, isLoading, refetch, isFetching } = useQuery({
    queryKey: ["optimizer-solve", budget],
    queryFn: async () => {
      const res = await optimizerApi.solve({
        target_budget: budget,
        scenario: "E-Commerce (B2C)",
        objective: "revenue",
        gross_margin_pct: 0.65,
        attribution_model: "Markov Chain",
      });
      return res.data;
    },
    staleTime: 2 * 60 * 1000,
  });

  const handleRunOptimizer = () => {
    const val = parseInt(inputBudget.replace(/,/g, ""), 10);
    if (!isNaN(val) && val > 0) {
      setBudget(val);
      setTimeout(() => refetch(), 0);
    }
  };

  const channels = data?.channels ?? [];
  const aiRec = data?.ai_recommendation;

  return (
    <>
      <TopNav
        title="SLSQP Budget Optimizer"
        subtitle="SciPy constrained optimisation · Hill saturation curves"
        actions={
          <div className="flex items-center gap-2">
            <input
              type="number"
              value={inputBudget}
              onChange={(e) => setInputBudget(e.target.value)}
              className="w-36 px-3 py-1.5 text-sm border border-slate-200 rounded-lg focus:ring-1 focus:ring-primary-500 focus:outline-none"
              placeholder="Budget (₹)"
            />
            <Button size="sm" className="gap-1.5" onClick={handleRunOptimizer} disabled={isFetching}>
              {isFetching ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Zap className="w-3.5 h-3.5" />}
              {isFetching ? "Solving..." : "Run SLSQP"}
            </Button>
          </div>
        }
      />
      <div className="flex-1 overflow-y-auto p-6 space-y-6">

        {/* KPI summary */}
        {data && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Target Budget", value: formatCurrency(data.target_budget) },
              { label: "Projected Revenue", value: formatCurrency(data.projected_total_revenue) },
              { label: "Blended ROAS", value: `${data.projected_blended_roas.toFixed(2)}x` },
              { label: "Revenue Uplift", value: formatCurrency(data.projected_total_revenue - data.target_budget) },
            ].map((k) => (
              <div key={k.label} className="bg-white border border-slate-200 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">{k.label}</p>
                <p className="text-lg font-bold text-slate-900">{k.value}</p>
              </div>
            ))}
          </div>
        )}

        {/* Channel allocation table */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100">
            <h2 className="text-sm font-semibold text-slate-900">Channel Allocation — Baseline vs Optimised</h2>
            <p className="text-xs text-slate-400 mt-0.5">SLSQP minimises negative profit subject to budget and channel constraints</p>
          </div>

          {isLoading ? (
            <div className="p-6 space-y-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="h-16 bg-slate-100 rounded-lg animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="divide-y divide-slate-50">
              {channels.map((ch: {
                channel: string; base_spend: number; optimized_spend: number;
                delta: number; delta_pct: number; projected_roas: number; revenue_impact: number;
              }) => {
                const pct = Math.max(ch.base_spend, ch.optimized_spend) > 0
                  ? ch.optimized_spend / Math.max(ch.base_spend, ch.optimized_spend)
                  : 0;
                const basePct = Math.max(ch.base_spend, ch.optimized_spend) > 0
                  ? ch.base_spend / Math.max(ch.base_spend, ch.optimized_spend)
                  : 0;
                const up = ch.delta >= 0;
                return (
                  <div key={ch.channel} className="px-5 py-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <span className="text-sm font-semibold text-slate-900 w-20">{ch.channel}</span>
                        <Badge variant={up ? "success" : "destructive"} className="text-xs">
                          {up ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                          {ch.delta_pct > 0 ? "+" : ""}{ch.delta_pct.toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="text-right text-xs text-slate-500">
                        <span className="font-medium text-slate-900">{formatCurrency(ch.optimized_spend)}</span>
                        <span className="text-slate-400"> vs {formatCurrency(ch.base_spend)}</span>
                      </div>
                    </div>
                    {/* Dual progress bars */}
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-400 w-16">Baseline</span>
                        <div className="flex-1 bg-slate-100 rounded-full h-1.5">
                          <div className="bg-slate-400 h-1.5 rounded-full" style={{ width: `${basePct * 100}%` }} />
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-primary-600 w-16 font-medium">Optimised</span>
                        <div className="flex-1 bg-primary-100 rounded-full h-1.5">
                          <div className="bg-primary-600 h-1.5 rounded-full" style={{ width: `${pct * 100}%` }} />
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-4 mt-1.5 text-xs text-slate-400">
                      <span>ROAS: <span className="font-medium text-slate-700">{ch.projected_roas.toFixed(2)}x</span></span>
                      <span>Rev impact: <span className={`font-medium ${ch.revenue_impact >= 0 ? "text-emerald-600" : "text-red-500"}`}>{ch.revenue_impact >= 0 ? "+" : ""}{formatCurrency(ch.revenue_impact)}</span></span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* AI Recommendation */}
        {aiRec && (
          <div className="bg-gradient-to-br from-primary-50 to-teal-50 border border-primary-200 rounded-xl p-5">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-4 h-4 text-amber-500" />
              <span className="text-sm font-bold text-slate-900">{aiRec.title}</span>
              {aiRec.impact && <Badge variant="success">{aiRec.impact}</Badge>}
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">{aiRec.body}</p>
            <p className="text-xs text-slate-400 mt-3">Advisory only. Human approval required before budget execution.</p>
          </div>
        )}
      </div>
    </>
  );
}
