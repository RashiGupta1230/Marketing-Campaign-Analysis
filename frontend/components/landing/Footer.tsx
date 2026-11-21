import Link from "next/link";
import { TrendingUp } from "lucide-react";

const footerLinks = {
  Platform: ["Attribution Models", "SLSQP Optimizer", "Scenarios", "Changelog"],
  Developers: ["FastAPI Docs", "API Reference", "Python SDK", "Audit Ledger"],
  Company: ["Methodology", "Privacy Policy", "Terms of Service", "Security"],
};

export function Footer() {
  return (
    <footer className="bg-slate-950 text-slate-400 py-16 border-t border-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
          <div className="col-span-2">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-sm">
                <TrendingUp className="w-4 h-4 text-white" />
              </div>
              <span className="font-extrabold text-white text-lg tracking-tight">
                Attribute<span className="text-blue-500">IQ</span>
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed max-w-sm mb-4">
              Multi-touch attribution decision-support engine powered by Markov Chain absorption matrices, Shapley value coalitions, and SciPy optimization.
            </p>
            <div className="text-[11px] text-slate-500">
              Palette: #0F172A Dark Navy · #2563EB Accent Blue · #F8FAFC Light Gray
            </div>
          </div>

          {Object.entries(footerLinks).map(([section, links]) => (
            <div key={section}>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 mb-3">{section}</h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link}>
                    <Link href="#" className="text-xs text-slate-400 hover:text-white transition-colors">
                      {link}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-slate-900 pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>© 2026 AttributeIQ. All rights reserved.</p>
          <p>Built for modern growth marketing & performance analytics.</p>
        </div>
      </div>
    </footer>
  );
}
