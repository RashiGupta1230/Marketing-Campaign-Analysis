import { GitBranch, Zap, BarChart3, Users, Shield, Download, TrendingUp, Layers } from "lucide-react";

const features = [
  { icon: GitBranch, title: "Markov Chain Attribution", description: "First-order Markov absorption with channel removal effects. Mathematically grounded, not a black box.", color: "text-blue-600", bg: "bg-blue-50" },
  { icon: TrendingUp, title: "Shapley Value MTA", description: "Cooperative game-theoretic fairness across channel coalitions. Every touchpoint gets its true credit.", color: "text-purple-600", bg: "bg-purple-50" },
  { icon: Zap, title: "SLSQP Budget Optimizer", description: "SciPy-powered Hill saturation curves. Maximize revenue or net profit contribution with one click.", color: "text-amber-600", bg: "bg-amber-50" },
  { icon: Layers, title: "5 Attribution Models", description: "First-click, Last-click, Linear, Markov, Shapley. Switch lens instantly. Revenue invariant guaranteed.", color: "text-teal-600", bg: "bg-teal-50" },
  { icon: Users, title: "Multi-company + Roles", description: "Admin, Analyst, Viewer roles. Every company's data isolated at the database layer via Row Level Security.", color: "text-green-600", bg: "bg-green-50" },
  { icon: Shield, title: "Governance & Audit Ledger", description: "SHA-256 sign-off hashes, persistent audit trail. Budget mutations require human approval.", color: "text-slate-600", bg: "bg-slate-100" },
  { icon: BarChart3, title: "Cohort LTV Analysis", description: "Retention decay heatmaps, CAC payback periods, and 3-month cumulative LTV per acquisition cohort.", color: "text-rose-600", bg: "bg-rose-50" },
  { icon: Download, title: "Executive Brief Export", description: "Print-ready HTML/PDF C-suite briefing with KPI grid, AI recommendation, and budget scenario table.", color: "text-indigo-600", bg: "bg-indigo-50" },
];

export function Features() {
  return (
    <section id="features" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-slate-100 rounded-full px-4 py-1.5 text-sm text-slate-600 font-medium mb-4">
            <BarChart3 className="w-3.5 h-3.5" /> Platform Capabilities
          </div>
          <h2 className="text-4xl font-bold text-slate-900 mb-4 tracking-tight">
            Everything your performance team needs
          </h2>
          <p className="text-xl text-slate-500 max-w-2xl mx-auto">
            Built by engineers who understand both the math and the marketing. No black boxes. Full auditability.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {features.map((f) => (
            <div key={f.title} className="group p-5 rounded-xl border border-slate-200 bg-white hover:border-slate-300 hover:shadow-md transition-all duration-200">
              <div className={`w-10 h-10 rounded-lg ${f.bg} flex items-center justify-center mb-4`}>
                <f.icon className={`w-5 h-5 ${f.color}`} />
              </div>
              <h3 className="font-semibold text-slate-900 mb-2 text-sm">{f.title}</h3>
              <p className="text-sm text-slate-500 leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

