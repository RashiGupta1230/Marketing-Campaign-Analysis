import { TopNav } from "@/components/dashboard/TopNav";
import { Button } from "@/components/ui/button";
import { Zap, TrendingUp, Info } from "lucide-react";

interface PageProps { params: { company: string } }

const channels = [
  { name: "Search",  current: 280000, optimized: 310000, roas: 3.1, mRoas: 2.8 },
  { name: "Social",  current: 240000, optimized: 195000, roas: 2.5, mRoas: 1.9 },
  { name: "Email",   current: 110000, optimized: 190000, roas: 3.8, mRoas: 4.1 },
  { name: "Display", current: 100000, optimized: 55000,  roas: 1.4, mRoas: 0.9 },
  { name: "Website", current: 70000,  optimized: 50000,  roas: 2.1, mRoas: 1.7 },
];

export default function OptimizerPage({ params }: PageProps) {
  const maxBudget = 400000;
  return (
    <>
      <TopNav title="Budget Optimizer" subtitle="SciPy SLSQP Hill saturation curve optimization"
        actions={
          <div className="flex gap-2">
            <Button variant="outline" size="sm">Reset</Button>
            <Button size="sm" className="gap-1.5"><Zap className="w-3.5 h-3.5" />Run SLSQP</Button>
          </div>
        }
      />
      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start gap-3">
          <Info className="w-4 h-4 text-amber-600 mt-0.5 shrink-0" />
          <p className="text-sm text-amber-800">
            <strong>Advisory only.</strong> SLSQP optimizer suggests the efficient frontier allocation. All budget mutations require human sign-off before execution.
          </p>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Current Budget", value: "₹8.0L" },
            { label: "Optimized Budget", value: "₹8.0L" },
            { label: "Projected ROAS Lift", value: "+0.32x", green: true },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-xl border border-slate-200 p-4">
              <div className="text-xs text-slate-500 font-medium mb-1">{s.label}</div>
              <div className={`text-xl font-bold ${s.green ? "text-emerald-600" : "text-slate-900"}`}>{s.value}</div>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-900">Channel Allocation Comparison</h2>
            <div className="flex items-center gap-3 text-xs text-slate-500">
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-slate-200 inline-block" />Current</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-primary-500 inline-block" />Optimized</span>
            </div>
          </div>
          <div className="p-5 space-y-5">
            {channels.map((ch) => {
              const diff = ch.optimized - ch.current;
              const isUp = diff > 0;
              return (
                <div key={ch.name}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-slate-700">{ch.name}</span>
                    <div className="flex items-center gap-3 text-xs">
                      <span className="text-slate-400">₹{(ch.current/1000).toFixed(0)}K current</span>
                      <span className={`font-bold px-2 py-0.5 rounded-full ${isUp ? "bg-emerald-100 text-emerald-700" : "bg-red-100 text-red-600"}`}>
                        {isUp ? "+" : ""}{(diff/1000).toFixed(0)}K
                      </span>
                      <span className="text-slate-900 font-bold">₹{(ch.optimized/1000).toFixed(0)}K</span>
                    </div>
                  </div>
                  <div className="relative h-5 bg-slate-100 rounded-full overflow-hidden">
                    <div className="absolute left-0 top-0 h-full bg-slate-200 rounded-full" style={{ width: `${(ch.current / maxBudget) * 100}%` }} />
                    <div className="absolute left-0 top-0 h-full bg-primary-500 rounded-full opacity-80" style={{ width: `${(ch.optimized / maxBudget) * 100}%` }} />
                  </div>
                  <div className="flex justify-between mt-1 text-xs text-slate-400">
                    <span>ROAS: {ch.roas}x</span>
                    <span>Marginal ROAS: <strong className={ch.mRoas >= 2 ? "text-emerald-600" : "text-red-500"}>{ch.mRoas}x</strong></span>
                  </div>
                </div>
              );
            })}
          </div>
          <div className="px-5 py-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
            <Button variant="outline" size="sm">Export CSV</Button>
            <Button size="sm" className="gap-1.5"><TrendingUp className="w-3.5 h-3.5" />Approve & Sign Off</Button>
          </div>
        </div>
      </div>
    </>
  );
}

