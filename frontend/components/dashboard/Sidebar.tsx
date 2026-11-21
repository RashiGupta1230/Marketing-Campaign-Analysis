"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  GitBranch,
  Zap,
  Users,
  Settings,
  TrendingUp,
  ChevronLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { label: "Overview", href: "", icon: LayoutDashboard },
  { label: "Reports", href: "/reports", icon: FileText },
  { label: "Attribution", href: "/attribution", icon: GitBranch },
  { label: "Optimizer", href: "/optimizer", icon: Zap },
  { label: "Team", href: "/team", icon: Users },
  { label: "Settings", href: "/settings", icon: Settings },
];

interface SidebarProps {
  company: string;
  companyName?: string;
}

export function Sidebar({ company, companyName = "Acme Corp" }: SidebarProps) {
  const pathname = usePathname();
  const base = `/dashboard/${company}`;
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "flex flex-col bg-slate-900 text-white transition-all duration-300 relative border-r border-slate-800 shrink-0",
        collapsed ? "w-16" : "w-60"
      )}
    >
      {/* Logo + Company */}
      <div className={cn("flex items-center gap-3 px-4 py-4 border-b border-slate-800", collapsed && "justify-center px-2")}>
        <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shrink-0 shadow-md">
          <TrendingUp className="w-4 h-4 text-white" />
        </div>
        {!collapsed && (
          <div className="overflow-hidden">
            <span className="font-extrabold text-sm tracking-tight text-white block truncate">
              Attribute<span className="text-blue-500">IQ</span>
            </span>
            <span className="text-[11px] text-slate-400 block truncate">{companyName}</span>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 p-2 space-y-1">
        {navItems.map((item) => {
          const href = `${base}${item.href}`;
          const active = pathname === href;
          return (
            <Link
              key={item.label}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-xs transition-colors",
                active
                  ? "bg-blue-600 text-white font-semibold shadow-sm"
                  : "text-slate-400 hover:bg-slate-800/80 hover:text-white",
                collapsed && "justify-center px-2"
              )}
            >
              <item.icon className="w-4 h-4 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Collapse Toggle */}
      <div className="p-3 border-t border-slate-800 flex justify-end">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          <ChevronLeft className={cn("w-4 h-4 transition-transform", collapsed && "rotate-180")} />
        </button>
      </div>
    </aside>
  );
}
