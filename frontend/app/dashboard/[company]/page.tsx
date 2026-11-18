import { TopNav } from "@/components/dashboard/TopNav";
import { KPICard } from "@/components/dashboard/KPICard";
import { Button } from "@/components/ui/button";
import { DollarSign, TrendingUp, Users, BarChart3, Download, RefreshCw, ArrowRight, Zap } from "lucide-react";

interface PageProps { params: { company: string } }

const kpis = [
  { label: "Total Media Spend", value: "₹8,00,000", delta: "+4.1% vs baseline", deltaType: "neutral" as const, caption: "Across 5 channels · All Regions", icon: <DollarSign className="w-4 h-4" /> },
  { label: "Attributed Revenue", value: "₹21,40,000", delta: "+8.2% vs baseline", deltaType: "positive" as const, caption: "Markov Chain model · Conserved", icon: <TrendingUp className="w-4 h-4" />, accent: true },
  { label: "Conversions & CPA", value: "3,420", delta: "+6.3% vs baseline", deltaType: "positive" as const, caption: "CPA: ₹2,339 · CAC: ₹3,124 (2.8m payback)", icon: <Users className="w-4 h-4" /> },
  { label: "ROAS / LTV:CAC", value: "2.67x (+167%)", delta: "+0.18x vs baseline", deltaType: "positive" as const, caption: "LTV:CAC: 4.2x · 🟢 Healthy", icon: <BarChart3 className="w-4 h-4" /> },
];

const channelRows = [
  { channel: "Email",   spend: "₹1,10,000", roas: "3.8x", conv: "712",   trend: "+12%", up: true  },
  { channel: "Search",  spend: "₹2,80,000", roas: "3.1x", conv: "1,089", trend: "+5%",  up: true  },
  { channel: "Social",  spend: "₹2,40,000", roas: "2.5x", conv: "890",   trend: "+9%",  up: true  },
  { channel: "Website", spend: "₹70,000",   roas: "2.1x", conv: "421",   trend: "+3%",  up: true  },
  { channel: "Display", spend: "₹1,00,000", roas: "1.4x", conv: "308",   trend: "-2%",  up: false },
];

const quickLinks = [
  { label: "Attribution Models", href: "attribution", icon: "🔀" },
  { label: "Run SLSQP Optimizer", href: "optimizer", icon: "⚡" },
  { label: "Manage Reports", href: "reports", icon: "📄" },
  { label: "Invite Team", href: "team", icon: "👥" },
];

export default function DashboardOverviewPage({ params }: PageProps) {
  const companyName = params.company.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  return (
    <>
      <TopNav
        title={`${companyName} — Campaign Overview`}
        subtitle="E-Commerce (B2C) · Oct 1 – Nov 3, 2026 · Markov Chain"
        actions={
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="gap-1.5"><RefreshCw className="w-3.5 h-3.5" />Refresh</Button>
            <Button size="sm" className="gap-1.5"><Download className="w-3.5 h-3.5" />Export Brief</Button>
          </div>
        }
      />
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* KPIs */}
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">📈 Historical Performance Actuals (Evaluated Period)</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            {kpis.map((k) => <KPICard key={k.label} {...k} />)}
          </div>
        </div>

        {/* Table + AI rec */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
          <div className="xl:col-span-2 bg-white rounded-xl border border-slate-200 overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
              <h2 className="text-sm font-semibold text-slate-900">Channel Performance</h2>
              <Button variant="ghost" size="sm" className="text-xs gap-1">View attribution <ArrowRight className="w-3 h-3" /></Button>
            </div>
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-100">
                  {["Channel", "Spend", "ROAS", "Conversions", "MoM"].map((h) => (
                    <th key={h} className="text-left text-xs font-semibold text-slate-500 px-5 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {channelRows.map((row, i) => (
                  <tr key={row.channel} className={`border-b border-slate-50 hover:bg-slate-50 transition-colors ${i === channelRows.length - 1 ? "border-0" : ""}`}>
                    <td className="px-5 py-3 font-medium text-slate-800">{row.channel}</td>
                    <td className="px-5 py-3 text-slate-600">{row.spend}</td>
                    <td className="px-5 py-3 font-semibold text-primary-700">{row.roas}</td>
                    <td className="px-5 py-3 text-slate-600">{row.conv}</td>
                    <td className="px-5 py-3">
                      <span className={`text-xs font-semibold ${row.up ? "text-emerald-600" : "text-red-500"}`}>{row.trend}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* AI Rec */}
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden flex flex-col">
            <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-500" />
              <h2 className="text-sm font-semibold text-slate-900">AI Recommendation</h2>
            </div>
            <div className="flex-1 p-5">
              <div className="bg-gradient-to-br from-primary-50 to-teal-50 border border-primary-100 rounded-xl p-4 mb-4">
                <div className="text-sm font-bold text-slate-900 mb-1">🎯 Reallocate ₹80K from Display → Email</div>
                <div className="text-xs font-semibold text-primary-700 mb-2">Projected: +₹1,20,000 incremental revenue</div>
                <div className="text-xs text-slate-600 leading-relaxed">Email is at 62% of Hill saturation. Display has crossed the diminishing-returns knee. Shapley model confirms Email&apos;s assist value is underweighted by 31% under Last-click.</div>
              </div>
              <Button className="w-full gap-2" variant="outline" size="sm"><Zap className="w-3.5 h-3.5" />Run SLSQP Optimizer →</Button>
            </div>
            <div className="px-5 py-3 bg-slate-50 border-t border-slate-100">
              <p className="text-xs text-slate-400">Advisory only. Human approval required before budget execution.</p>
            </div>
          </div>
        </div>

        {/* Quick links */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {quickLinks.map((card) => (
            <a key={card.label} href={card.href}
              className="bg-white rounded-xl border border-slate-200 p-4 hover:border-primary-300 hover:shadow-sm transition-all group">
              <div className="text-2xl mb-2">{card.icon}</div>
              <div className="text-xs font-medium text-slate-700 group-hover:text-primary-700 transition-colors">{card.label}</div>
            </a>
          ))}
        </div>
      </div>
    </>
  );
}

