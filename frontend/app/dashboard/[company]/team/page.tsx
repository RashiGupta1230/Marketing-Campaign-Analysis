import { TopNav } from "@/components/dashboard/TopNav";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Mail, MoreHorizontal, Shield, BarChart3, Eye } from "lucide-react";

interface PageProps { params: { company: string } }

const members = [
  { name: "Priya Sharma", email: "priya@acme.com", role: "admin", status: "active", lastActive: "Now", initials: "PS", color: "from-primary-400 to-teal-600" },
  { name: "Rahul Verma", email: "rahul@acme.com", role: "analyst", status: "active", lastActive: "2 hours ago", initials: "RV", color: "from-blue-400 to-indigo-600" },
  { name: "Ananya Singh", email: "ananya@acme.com", role: "analyst", status: "active", lastActive: "Yesterday", initials: "AS", color: "from-purple-400 to-pink-600" },
  { name: "Karthik Nair", email: "karthik@acme.com", role: "viewer", status: "pending", lastActive: "Invite sent", initials: "KN", color: "from-slate-400 to-slate-600" },
];

const roles = [
  { name: "Admin", icon: Shield, description: "Full access: data, reports, team management, billing, and settings.", color: "text-primary-700", bg: "bg-primary-50", border: "border-primary-200" },
  { name: "Analyst", icon: BarChart3, description: "Access to all reports, attribution models, and budget optimizer. Cannot manage team.", color: "text-blue-700", bg: "bg-blue-50", border: "border-blue-200" },
  { name: "Viewer", icon: Eye, description: "Read-only access to reports and exports. Cannot run simulations or edit data.", color: "text-slate-700", bg: "bg-slate-50", border: "border-slate-200" },
];

export default function TeamPage({ params }: PageProps) {
  return (
    <>
      <TopNav title="Team" subtitle="Manage members and roles"
        actions={<Button size="sm" className="gap-1.5"><Plus className="w-3.5 h-3.5" />Invite Member</Button>} />
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Members table */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
            <h2 className="text-sm font-semibold text-slate-900">Members <span className="text-slate-400 font-normal ml-1">({members.length})</span></h2>
            <Button variant="ghost" size="sm" className="gap-1.5 text-xs"><Mail className="w-3.5 h-3.5" />Bulk invite</Button>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-100">
                {["Member", "Role", "Status", "Last Active", ""].map((h) => (
                  <th key={h} className="text-left text-xs font-semibold text-slate-500 px-5 py-3">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {members.map((m) => (
                <tr key={m.email} className="border-b border-slate-50 last:border-0 hover:bg-slate-50 transition-colors">
                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-3">
                      <div className={`w-8 h-8 rounded-full bg-gradient-to-br ${m.color} flex items-center justify-center text-white text-xs font-bold shrink-0`}>{m.initials}</div>
                      <div>
                        <div className="font-medium text-slate-800 text-sm">{m.name}</div>
                        <div className="text-xs text-slate-400">{m.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-5 py-3.5">
                    <Badge variant={m.role === "admin" ? "default" : m.role === "analyst" ? "secondary" : "outline"} className="capitalize">{m.role}</Badge>
                  </td>
                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-1.5">
                      <div className={`w-1.5 h-1.5 rounded-full ${m.status === "active" ? "bg-emerald-500" : "bg-amber-400"}`} />
                      <span className={`text-xs font-medium capitalize ${m.status === "active" ? "text-emerald-700" : "text-amber-600"}`}>{m.status}</span>
                    </div>
                  </td>
                  <td className="px-5 py-3.5 text-xs text-slate-400">{m.lastActive}</td>
                  <td className="px-5 py-3.5"><Button variant="ghost" size="icon" className="h-7 w-7"><MoreHorizontal className="w-4 h-4" /></Button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Role definitions */}
        <div>
          <h2 className="text-sm font-semibold text-slate-900 mb-3">Role Permissions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {roles.map((role) => (
              <div key={role.name} className={`rounded-xl border p-4 ${role.bg} ${role.border}`}>
                <div className="flex items-center gap-2 mb-2">
                  <role.icon className={`w-4 h-4 ${role.color}`} />
                  <span className={`text-sm font-semibold ${role.color}`}>{role.name}</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">{role.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

