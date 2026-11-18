import Link from "next/link";
import { TrendingUp } from "lucide-react";

const footerLinks = {
  Product: ["Features", "Pricing", "Changelog", "Roadmap"],
  Docs: ["Getting Started", "API Reference", "Attribution Models", "Optimizer Guide"],
  Company: ["About", "Blog", "Careers", "Contact"],
  Legal: ["Privacy Policy", "Terms of Service"],
};

export function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400 py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-7 h-7 rounded-lg bg-primary-600 flex items-center justify-center">
                <TrendingUp className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="font-bold text-white">Attribute<span className="text-primary-500">IQ</span></span>
            </div>
            <p className="text-sm text-slate-500 leading-relaxed">Multi-touch attribution for modern marketing teams.</p>
          </div>
          {Object.entries(footerLinks).map(([section, links]) => (
            <div key={section}>
              <h4 className="text-sm font-semibold text-slate-300 mb-3">{section}</h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link}>
                    <Link href="#" className="text-sm text-slate-500 hover:text-slate-300 transition-colors">{link}</Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-600">© 2026 AttributeIQ. All rights reserved.</p>
          <div className="flex items-center gap-1 text-sm text-slate-600">
            <span>Built with</span><span className="text-primary-500">♥</span><span>for performance marketers</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

