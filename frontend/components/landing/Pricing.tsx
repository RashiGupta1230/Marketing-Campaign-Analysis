import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Starter",
    price: "₹4,999",
    period: "/month",
    description: "For scaling growth brands moving beyond last-click heuristic attribution.",
    features: [
      "Up to 3 team members",
      "All 5 MTA attribution models",
      "3 vertical benchmark simulations",
      "SLSQP budget optimization",
      "CSV & touchpoint dataset upload",
      "Executive Brief PDF export",
      "Email support",
    ],
    cta: "Start Free Trial",
    href: "/auth/register?plan=starter",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "₹14,999",
    period: "/month",
    description: "For performance-focused marketing teams demanding full budget governance.",
    features: [
      "Unlimited team workspaces",
      "Everything in Starter",
      "Markov & Shapley curve scaling",
      "FastAPI programmatic integration",
      "SHA-256 sign-off audit ledger",
      "Role-based RBAC (Admin, Analyst, Viewer)",
      "Priority SLA support",
      "Custom scenario configurations",
    ],
    cta: "Start Pro Trial",
    href: "/auth/register?plan=pro",
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "For large agencies and multi-brand enterprises managing cross-client budgets.",
    features: [
      "Unlimited client workspaces",
      "Everything in Pro",
      "SAML / Okta Single Sign-On",
      "Dedicated Python engine instance",
      "Custom ERP & warehouse connectors",
      "Onboarding & mathematical advisory",
      "99.9% uptime SLA",
    ],
    cta: "Contact Enterprise",
    href: "/auth/register?plan=enterprise",
    highlighted: false,
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 max-w-2xl mx-auto">
          <h2 className="text-4xl sm:text-5xl font-extrabold text-slate-900 mb-4 tracking-tight">
            Transparent, performance pricing
          </h2>
          <p className="text-lg text-slate-600">
            14-day free trial across all tiers. No credit card required to start.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto items-stretch">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl p-8 flex flex-col transition-all duration-200 ${
                plan.highlighted
                  ? "bg-slate-900 text-white shadow-2xl scale-[1.03] border-2 border-blue-500"
                  : "bg-white border border-slate-200 shadow-sm hover:border-slate-300"
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
                  <div className="bg-blue-600 text-white text-xs font-bold uppercase tracking-wider px-3.5 py-1 rounded-full shadow-sm">
                    Recommended
                  </div>
                </div>
              )}

              <div className="mb-6">
                <div className={`text-sm font-bold uppercase tracking-wider mb-2 ${plan.highlighted ? "text-blue-400" : "text-blue-600"}`}>
                  {plan.name}
                </div>
                <div className="flex items-baseline gap-1 mb-3">
                  <span className={`text-4xl font-extrabold tracking-tight ${plan.highlighted ? "text-white" : "text-slate-900"}`}>
                    {plan.price}
                  </span>
                  <span className={`text-sm font-medium ${plan.highlighted ? "text-slate-400" : "text-slate-500"}`}>
                    {plan.period}
                  </span>
                </div>
                <p className={`text-xs leading-relaxed ${plan.highlighted ? "text-slate-300" : "text-slate-500"}`}>
                  {plan.description}
                </p>
              </div>

              <div className="space-y-3 mb-8 flex-1">
                {plan.features.map((feat) => (
                  <div key={feat} className="flex items-start gap-2.5 text-xs">
                    <Check className={`w-4 h-4 shrink-0 mt-0.5 ${plan.highlighted ? "text-blue-400" : "text-blue-600"}`} />
                    <span className={plan.highlighted ? "text-slate-200" : "text-slate-600"}>
                      {feat}
                    </span>
                  </div>
                ))}
              </div>

              <Button
                variant={plan.highlighted ? "default" : "outline"}
                className={`w-full font-bold ${plan.highlighted ? "bg-blue-600 hover:bg-blue-500 text-white shadow-glow" : ""}`}
                size="lg"
                asChild
              >
                <Link href={plan.href}>{plan.cta} →</Link>
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
