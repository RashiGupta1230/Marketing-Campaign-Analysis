import { GitBranch, Zap, BarChart3, Users, Shield, Download, TrendingUp, Layers } from "lucide-react";

const features = [
  {
    icon: GitBranch,
    title: "Markov Chain Attribution",
    description: "First-order absorption matrices with removal effects. Captures true channel assists without guesswork.",
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
  {
    icon: TrendingUp,
    title: "Shapley Value Game Theory",
    description: "Fair coalition calculations across permutations. Evaluates cooperative contribution across every touchpoint.",
    color: "text-indigo-600",
    bg: "bg-indigo-50",
  },
  {
    icon: Zap,
    title: "SciPy SLSQP Optimizer",
    description: "Constrained quadratic budgeting over Hill saturation curves. Solves for maximum revenue or profit under budget limits.",
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
  {
    icon: Layers,
    title: "5 Comparative Models",
    description: "Compare First-click, Last-click, Linear, Markov, and Shapley side-by-side with strict Revenue Conservation.",
    color: "text-slate-700",
    bg: "bg-slate-100",
  },
  {
    icon: Users,
    title: "Multi-Company Workspace",
    description: "Tenant isolation with Admin, Analyst, and Viewer roles. Team collaboration with role-based permissions.",
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
  {
    icon: Shield,
    title: "SHA-256 Audit Ledger",
    description: "Cryptographic sign-offs for budget allocations. Complete change audit trail before committing ad spend.",
    color: "text-slate-800",
    bg: "bg-slate-100",
  },
  {
    icon: BarChart3,
    title: "Cohort Retention & Payback",
    description: "Analyze retention decay heatmaps, CAC recovery curves, and 3-month cumulative LTV per channel.",
    color: "text-indigo-600",
    bg: "bg-indigo-50",
  },
  {
    icon: Download,
    title: "C-Suite Executive Briefs",
    description: "One-click generation of board-ready briefs containing KPI impact, model variance, and AI advice.",
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
];

export function Features() {
  return (
    <section id="features" className="py-24 bg-slate-50 border-y border-slate-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200/80 rounded-full px-3.5 py-1 text-xs text-blue-700 font-semibold mb-4">
            <BarChart3 className="w-3.5 h-3.5" /> 2026 Core Capabilities
          </div>
          <h2 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
            Built for rigorous performance teams
          </h2>
          <p className="text-lg text-slate-600 leading-relaxed">
            Eliminate heuristic bias with verified mathematical models. Clear visual hierarchy, auditable logic, zero black boxes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {features.map((f) => (
            <div
              key={f.title}
              className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:border-blue-300 hover:shadow-card-hover hover:-translate-y-1 transition-all duration-200 ease-out group"
            >
              <div className={`w-11 h-11 rounded-xl ${f.bg} flex items-center justify-center mb-4 group-hover:scale-105 transition-transform`}>
                <f.icon className={`w-5 h-5 ${f.color}`} />
              </div>
              <h3 className="font-bold text-slate-900 mb-2 text-base tracking-tight">{f.title}</h3>
              <p className="text-xs text-slate-500 leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
