import { TopNav } from "@/components/dashboard/TopNav";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { GitBranch, Info } from "lucide-react";

interface PageProps { params: { company: string } }

const models = [
  { name: "Markov Chain", tag: "Recommended", description: "First-order Markov absorption with channel removal effects. Computes conversion probability drop when each channel is removed from the journey graph.", strengths: ["Full journey awareness", "Handles position bias", "Mathematically grounded"], use: "Default — most balanced for multi-channel journeys", style: "border-primary-300 bg-primary-50", badge: "default" as const },
  { name: "Shapley Value", tag: "Game Theory", description: "Cooperative game-theoretic fairness across all channel coalitions. Guarantees fair marginal contribution regardless of touchpoint ordering.", strengths: ["Fairness guarantee", "Coalition-aware", "Order-independent"], use: "When channels have high co-occurrence and ordering is noisy", style: "border-purple-200 bg-purple-50", badge: "secondary" as const },
  { name: "Linear", tag: "Heuristic", description: "Equal credit distributed across all touchpoints in the path. Simple, transparent, and easy to explain to stakeholders.", strengths: ["Fully transparent", "No data requirements", "Easy to audit"], use: "Baseline comparison or stakeholder presentations", style: "border-slate-200 bg-white", badge: "outline" as const },
  { name: "First-click", tag: "Heuristic", description: "100% credit to the first touchpoint. Overweights awareness and discovery channels (Social, Display).", strengths: ["Simple to compute", "Good for brand awareness"], use: "Evaluating top-of-funnel channel effectiveness", style: "border-slate-200 bg-white", badge: "outline" as const },
  { name: "Last-click", tag: "Heuristic", description: "100% credit to the last touchpoint before conversion. Systematically undervalues assist channels.", strengths: ["Industry standard comparison", "Easy to implement"], use: "Comparison baseline — not recommended for optimization", style: "border-slate-200 bg-white", badge: "outline" as const },
];

export default function AttributionPage({ params }: PageProps) {
  return (
    <>
      <TopNav title="Attribution Models" subtitle="Compare how each model distributes revenue credit across channels"
        actions={<Button size="sm">Run Comparison →</Button>} />
      <div className="flex-1 overflow-y-auto p-6">
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 flex items-start gap-3">
          <Info className="w-4 h-4 text-blue-600 mt-0.5 shrink-0" />
          <p className="text-sm text-blue-800">
            <strong>Revenue Conservation Invariant:</strong> All 5 models ensure{" "}
            <code className="bg-blue-100 px-1 rounded text-xs">sum(attributed_revenue) == total_revenue</code>.
            Switching models changes credit distribution — not the total.
          </p>
        </div>
        <div className="space-y-3">
          {models.map((m) => (
            <div key={m.name} className={`rounded-xl border p-5 ${m.style}`}>
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-white border border-slate-200 flex items-center justify-center">
                    <GitBranch className="w-4 h-4 text-slate-600" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-slate-900 text-sm">{m.name}</h3>
                      <Badge variant={m.badge} className="text-xs">{m.tag}</Badge>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">{m.use}</p>
                  </div>
                </div>
                <Button variant="outline" size="sm" className="shrink-0 bg-white">Select Model</Button>
              </div>
              <p className="text-sm text-slate-600 mb-3">{m.description}</p>
              <div className="flex flex-wrap gap-2">
                {m.strengths.map((s) => (
                  <span key={s} className="text-xs bg-white border border-slate-200 text-slate-600 px-2.5 py-1 rounded-full">✓ {s}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

