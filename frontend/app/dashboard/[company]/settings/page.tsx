import { TopNav } from "@/components/dashboard/TopNav";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

interface PageProps { params: { company: string } }

export default function SettingsPage({ params }: PageProps) {
  const companyName = params.company.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  return (
    <>
      <TopNav title="Settings" subtitle="Workspace configuration" />
      <div className="flex-1 overflow-y-auto p-6 space-y-5 max-w-2xl">
        {/* Company info */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100">
            <h2 className="text-sm font-semibold text-slate-900">Company Information</h2>
          </div>
          <div className="p-5 space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Company Name</label>
              <Input defaultValue={companyName} />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Workspace URL</label>
              <div className="flex rounded-lg border border-slate-200 overflow-hidden focus-within:ring-2 focus-within:ring-primary-600">
                <span className="bg-slate-50 border-r border-slate-200 px-3 flex items-center text-xs text-slate-400 shrink-0">app.attributeiq.com/</span>
                <input className="flex-1 px-3 py-2 text-sm text-slate-900 bg-white outline-none" defaultValue={params.company} />
              </div>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Industry</label>
              <select className="flex h-10 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-600">
                <option>E-Commerce (B2C)</option>
                <option>B2B Enterprise SaaS</option>
                <option>EdTech & Professional Courses</option>
              </select>
            </div>
            <Button size="sm">Save Changes</Button>
          </div>
        </div>

        {/* Plan & billing */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-900">Plan & Billing</h2>
            <Badge variant="default">Pro</Badge>
          </div>
          <div className="p-5">
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-sm font-medium text-slate-900">Pro Plan</div>
                <div className="text-xs text-slate-500">₹14,999/month · Renews Dec 3, 2026</div>
              </div>
              <Button variant="outline" size="sm">Manage Billing</Button>
            </div>
            <div className="grid grid-cols-3 gap-3">
              {[
                { label: "Team Members", value: "4 / Unlimited" },
                { label: "Reports", value: "12 / Unlimited" },
                { label: "API Calls (MTD)", value: "8,241" },
              ].map((item) => (
                <div key={item.label} className="bg-slate-50 rounded-lg p-3">
                  <div className="text-xs text-slate-500 mb-1">{item.label}</div>
                  <div className="text-sm font-semibold text-slate-800">{item.value}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Danger zone */}
        <div className="bg-white rounded-xl border border-red-200 overflow-hidden">
          <div className="px-5 py-4 border-b border-red-100">
            <h2 className="text-sm font-semibold text-red-700">Danger Zone</h2>
          </div>
          <div className="p-5 flex items-center justify-between">
            <div>
              <div className="text-sm font-medium text-slate-800">Delete workspace</div>
              <div className="text-xs text-slate-500">Permanently deletes all data. This cannot be undone.</div>
            </div>
            <Button variant="destructive" size="sm">Delete Workspace</Button>
          </div>
        </div>
      </div>
    </>
  );
}

