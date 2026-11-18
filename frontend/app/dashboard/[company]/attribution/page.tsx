"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { TopNav } from "@/components/dashboard/TopNav";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { RefreshCw, Info } from "lucide-react";
import { attributionApi } from "@/lib/api";
import { formatCurrency, formatPercent } from "@/lib/utils";

const MODEL_META: Record<string, { description: string; strength: string; tag: string; tagColor: "default" | "secondary" | "success" | "warning" }> = {
  "First-click":   { description: "100% credit to the first touchpoint. Good for brand awareness measurement.", strength: "Simple, clear, favours top-of-funnel channels.", tag: "Top-of-funnel", tagColor: "secondary" },
  "Last-click":    { description: "100% credit to the final touchpoint before conversion. Default in most ad platforms.", strength: "Simple, conversion-focused. Undervalues assist channels.", tag: "Conversion focus", tagColor: "default" },
  "Linear":        { description: "Equal credit distributed across all touchpoints in the journey.", strength: "Fair baseline. Ignores actual channel contribution weight.", tag: "Balanced", tagColor: "secondary" },
  "Markov Chain":  { description: "Removal-effect matrix: each channel's credit = drop in conversion rate if removed.", strength: "Mathematically rigorous. Captures sequence & interaction effects.", tag: "Recommended", tagColor: "success" },
  "Shapley Value": { description: "Game-theoretic coalition values: credit = average marginal contribution across all channel orderings.", strength: "Theoretically optimal. Computationally intensive at scale.", tag: "Gold standard", tagColor: "success" },
};

function ModelSkeleton() {
  return <div className="bg-white rounded-xl border border-slate-200 p-5 animate-pulse h-48" />;
}

export default function AttributionPage() {
  const params = useParams();
  const company = params.company as string;

  const { data: compareData, isLoading, refetch } = useQuery({
    queryKey: ["attribution-compare", "E-Commerce (B2C)"],
    queryFn: async () => {
      const res = await attributionApi.compare("E-Commerce (B2C)", 42);
      return res.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  const models = ["First-click", "Last-click", "Linear", "Markov Chain", "Shapley Value"];
  const totalRev = compareData?.total_revenue ?? 0;

  // Build per-model totals
  const modelTotals = models.map((m) => {
    const key = m.toLowerCase().replace(/ /g, "_").replace(/-/g, "_").replace("chain", "chain");
    const colMap: Record<string, string> = {
      "First-click": "first_click", "Last-click": "last_click",
      "Linear": "linear", "Markov Chain": "markov_chain", "Shapley Value": "shapley_value",
    };
    const col = colMap[m];
    const total = (compareData?.channels ?? []).reduce(
      (s: number, c: Record<string, number>) => s + (c[col] ?? 0), 0
    );
    return { model: m, total };
  });

  return (
    <>
      <TopNav
        title="Attribution Models"
        subtitle="Compare 5 multi-touch models on the same dataset"
        actions={
          <Button variant="outline" size="sm" className="gap-1.5" onClick={() => refetch()} disabled={isLoading}>
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
            {isLoading ? "Computing..." : "Recompute"}
          </Button>
        }
      />
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Revenue conservation notice */}
        <div className="flex items-start gap-3 p-4 bg-teal-50 border border-teal-200 rounded-xl text-sm text-teal-800">
          <Info className="w-4 h-4 mt-0.5 shrink-0" />
          <div>
            <span className="font-semibold">Revenue Conservation Invariant enforced.</span>{" "}
            Across all models, total attributed revenue = total actual revenue (±0.1%).
            {totalRev > 0 && <span className="ml-1 font-medium">Total: {formatCurrency(totalRev)}</span>}
          </div>
        </div>

        {/* Model cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {isLoading
            ? Array.from({ length: 5 }).map((_, i) => <ModelSkeleton key={i} />)
            : models.map((m) => {
                const meta = MODEL_META[m];
                const total = modelTotals.find((t) => t.model === m)?.total ?? 0;
                return (
                  <div key={m} className={`bg-white rounded-xl border p-5 flex flex-col gap-3 ${m === "Markov Chain" ? "border-primary-300 ring-1 ring-primary-100" : "border-slate-200"}`}>
                    <div className="flex items-start justify-between">
                      <h3 className="text-sm font-bold text-slate-900">{m}</h3>
                      <Badge variant={meta.tagColor}>{meta.tag}</Badge>
                    </div>
                    <p className="text-xs text-slate-500 leading-relaxed">{meta.description}</p>
                    <p className="text-xs text-slate-400 italic">{meta.strength}</p>
                    <div className="mt-auto pt-3 border-t border-slate-100">
                      <div className="text-xs text-slate-500 mb-1">Total attributed revenue</div>
                      <div className="text-lg font-bold text-slate-900">{formatCurrency(total)}</div>
                    </div>
                    {/* Per-channel mini table */}
                    {compareData && (
                      <div className="text-xs space-y-1">
                        {(compareData.channels as Record<string, number | string>[])
                          .slice()
                          .sort((a, b) => {
                            const colMap: Record<string, string> = {
                              "First-click": "first_click", "Last-click": "last_click",
                              "Linear": "linear", "Markov Chain": "markov_chain", "Shapley Value": "shapley_value",
                            };
                            const col = colMap[m];
                            return (b[col] as number) - (a[col] as number);
                          })
                          .map((ch) => {
                            const colMap: Record<string, string> = {
                              "First-click": "first_click", "Last-click": "last_click",
                              "Linear": "linear", "Markov Chain": "markov_chain", "Shapley Value": "shapley_value",
                            };
                            const col = colMap[m];
                            const val = ch[col] as number;
                            const pct = total > 0 ? val / total : 0;
                            return (
                              <div key={ch.channel as string} className="flex items-center gap-2">
                                <span className="w-16 text-slate-500 truncate">{ch.channel}</span>
                                <div className="flex-1 bg-slate-100 rounded-full h-1.5">
                                  <div className="bg-primary-500 h-1.5 rounded-full" style={{ width: `${pct * 100}%` }} />
                                </div>
                                <span className="w-10 text-right text-slate-600">{formatPercent(pct)}</span>
                              </div>
                            );
                          })}
                      </div>
                    )}
                  </div>
                );
              })}
        </div>
      </div>
    </>
  );
}
