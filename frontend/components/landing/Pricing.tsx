import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Starter", price: "₹4,999", period: "/month",
    description: "For growing teams that need real attribution, not just last-click.",
    features: ["Up to 3 team members", "All 5 attribution models", "3 industry verticals", "SLSQP budget optimizer", "CSV data upload", "Executive brief export", "Email support"],
    cta: "Start free trial", href: "/auth/register?plan=starter", highlighted: false,
  },
  {
    name: "Pro", price: "₹14,999", period: "/month",
    description: "For performance-driven teams that live in the data every day.",
    features: ["Unlimited team members", "Everything in Starter", "Custom industry scenarios", "API access (FastAPI)", "Audit ledger + sign-off", "Role-based access control", "Priority support", "White-label reports"],
    cta: "Start Pro trial", href: "/auth/register?plan=pro", highlighted: true,
  },
  {
    name: "Enterprise", price: "Custom", period: "",
    description: "For large marketing orgs and agencies managing multiple clients.",
    features: ["Unlimited companies", "Everything in Pro", "SSO / SAML", "Custom data connectors", "Dedicated instance", "SLA guarantee", "Onboarding & training"],
    cta: "Contact sales", href: "/contact", highlighted: false,
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-slate-900 mb-4 tracking-tight">Simple, transparent pricing</h2>
          <p className="text-xl text-slate-500">14-day free trial. No credit card required.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <div key={plan.name} className={`relative rounded-2xl p-7 flex flex-col ${
              plan.highlighted
                ? "bg-slate-900 text-white shadow-2xl scale-[1.02] border border-slate-700"
                : "bg-white border border-slate-200 shadow-sm"
            }`}>
              {plan.highlighted && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
                  <div className="bg-primary-600 text-white text-xs font-semibold px-3 py-1 rounded-full">Most popular</div>
                </div>
              )}
              <div className="mb-6">
                <div className={`text-sm font-semibold mb-3 ${plan.highlighted ? "text-primary-400" : "text-primary-600"}`}>{plan.name}</div>
                <div className="flex items-end gap-1 mb-3">
                  <span className={`text-3xl font-bold ${plan.highlighted ? "text-white" : "text-slate-900"}`}>{plan.price}</span>
                  <span className={`text-sm mb-1 ${plan.highlighted ? "text-slate-400" : "text-slate-500"}`}>{plan.period}</span>
                </div>
                <p className={`text-sm ${plan.highlighted ? "text-slate-400" : "text-slate-500"}`}>{plan.description}</p>
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2.5">
                    <Check className={`w-4 h-4 mt-0.5 shrink-0 ${plan.highlighted ? "text-primary-400" : "text-primary-600"}`} />
                    <span className={`text-sm ${plan.highlighted ? "text-slate-300" : "text-slate-600"}`}>{f}</span>
                  </li>
                ))}
              </ul>
              <Button variant={plan.highlighted ? "gradient" : "outline"} className="w-full" asChild>
                <Link href={plan.href}>{plan.cta}</Link>
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

