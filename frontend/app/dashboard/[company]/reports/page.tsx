import { TopNav } from "@/components/dashboard/TopNav";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Download, Share2, MoreHorizontal, FileText, CheckCircle2, Clock } from "lucide-react";

interface PageProps { params: { company: string } }

const reports = [
  { id: "r1", title: "Q4 E-Commerce Attribution Analysis", scenario: "E-Commerce (B2C)", model: "Markov Chain", dateRange: "Oct 1 – Nov 3, 2026", status: "signed_off", createdBy: "Priya Sharma", createdAt: "Nov 3, 2026", auditId: "AUD-20261103-001" },
  { id: "r2", title: "Diwali Campaign ROAS Review", scenario: "E-Commerce (B2C)", model: "Shapley Value", dateRange: "Sep 15 – Oct 15, 2026", status: "draft", createdBy: "Rahul Verma", createdAt: "Oct 16, 2026", auditId: null },
  { id: "r3", title: "B2B SaaS Attribution — Q3 Retrospective", scenario: "B2B Enterprise SaaS", model: "Shapley Value", dateRange: "Jul 1 – Sep 30, 2026", status: "signed_off", createdBy: "Priya Sharma", createdAt: "Oct 2, 2026", auditId: "AUD-20261002-001" },
];

export default function ReportsPage({ params }: PageProps) {
  return (
    <>
      <TopNav title="Reports" subtitle="Attribution analyses, what-if scenarios, and executive briefs"
        actions={<Button size="sm" className="gap-1.5"><Plus className="w-3.5 h-3.5" />New Report</Button>} />
      <div className="flex-1 overflow-y-auto p-6 space-y-3">
        {reports.map((r) => (
          <div key={r.id} className="bg-white rounded-xl border border-slate-200 p-5 hover:border-slate-300 hover:shadow-sm transition-all">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-4 min-w-0">
                <div className="w-9 h-9 rounded-lg bg-slate-100 flex items-center justify-center shrink-0 mt-0.5">
                  <FileText className="w-4 h-4 text-slate-500" />
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <h3 className="font-semibold text-slate-900 text-sm">{r.title}</h3>
                    {r.status === "signed_off"
                      ? <Badge variant="success" className="gap-1"><CheckCircle2 className="w-3 h-3" />Signed Off</Badge>
                      : <Badge variant="warning" className="gap-1"><Clock className="w-3 h-3" />Draft</Badge>}
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-400 flex-wrap">
                    <span>{r.scenario}</span><span>·</span>
                    <span>{r.model} MTA</span><span>·</span>
                    <span>{r.dateRange}</span><span>·</span>
                    <span>By {r.createdBy}</span>
                    {r.auditId && <><span>·</span><span className="font-mono text-primary-600">{r.auditId}</span></>}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <Button variant="outline" size="sm" className="gap-1.5"><Download className="w-3.5 h-3.5" />Export</Button>
                <Button variant="outline" size="sm" className="gap-1.5"><Share2 className="w-3.5 h-3.5" />Share</Button>
                <Button variant="ghost" size="sm"><MoreHorizontal className="w-4 h-4" /></Button>
              </div>
            </div>
          </div>
        ))}
        <div className="border-2 border-dashed border-slate-200 rounded-xl p-8 text-center mt-2">
          <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center mx-auto mb-3">
            <Plus className="w-5 h-5 text-slate-400" />
          </div>
          <h3 className="text-sm font-semibold text-slate-700 mb-1">Create a new report</h3>
          <p className="text-xs text-slate-400 mb-4">Run attribution analysis, what-if simulations, and generate executive briefs.</p>
          <Button size="sm">New Report</Button>
        </div>
      </div>
    </>
  );
}

