import Link from "next/link";
import { TrendingUp } from "lucide-react";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Left branding panel */}
      <div className="hidden lg:flex lg:w-[460px] xl:w-[520px] bg-slate-900 flex-col justify-between p-12 relative overflow-hidden shrink-0">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-primary-900/30" />
        <div className="absolute bottom-0 right-0 w-80 h-80 bg-primary-600/10 rounded-full blur-3xl" />
        <div className="absolute top-1/4 -left-10 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl" />

        {/* Logo */}
        <div className="relative flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-primary-600 flex items-center justify-center shadow-lg">
            <TrendingUp className="w-5 h-5 text-white" />
          </div>
          <span className="text-white font-bold text-xl">
            Attribute<span className="text-primary-400">IQ</span>
          </span>
        </div>

        {/* Testimonial */}
        <div className="relative">
          <div className="text-primary-400 text-4xl font-serif mb-4">"</div>
          <blockquote className="text-slate-300 text-lg leading-relaxed font-medium mb-6">
            Stop flying blind on attribution. Markov Chain models revealed we were over-investing
            in Last-Click channels by 40%.
          </blockquote>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-teal-600 flex items-center justify-center text-white font-bold text-sm">
              PS
            </div>
            <div>
              <div className="text-white font-semibold text-sm">Priya Sharma</div>
              <div className="text-slate-500 text-xs">Head of Performance Marketing, Acme Corp</div>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="relative grid grid-cols-3 gap-4">
          {[
            { value: "3.2x", label: "Avg ROAS lift" },
            { value: "40%", label: "Budget waste cut" },
            { value: "< 5s", label: "Attribution compute" },
          ].map((s) => (
            <div key={s.label} className="text-center">
              <div className="text-2xl font-bold text-primary-400 mb-1">{s.value}</div>
              <div className="text-xs text-slate-500">{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Right form panel */}
      <div className="flex-1 flex flex-col">
        <div className="flex items-center px-8 py-5 border-b border-slate-200 bg-white lg:hidden">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-primary-600 flex items-center justify-center">
              <TrendingUp className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="font-bold text-slate-900">Attribute<span className="text-primary-600">IQ</span></span>
          </Link>
        </div>
        <div className="flex-1 flex items-center justify-center p-8">{children}</div>
      </div>
    </div>
  );
}

