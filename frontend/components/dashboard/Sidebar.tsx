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
  Building2,
  Bell,
  HelpCircle,
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
        "flex flex-col bg-slate-900 text-white transition-all duration-300 relative",
        collapsed ? "w-16" : "w-60"
      )}
    >
      {/* Logo + company */}
      <div className={cn("flex items-center gap-3 px-4 py-5 border-b border-slate-800", collapsed && "justify-center px-2")}>
        <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center shrink-0 shadow-md">
          <TrendingUp className="w-4 h-4 text-white" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <div className="text-white font-bold text-sm tracking-tight truncate">
              Attribute<span className="text-primary-400">IQ</span>
            </div>
            <div className="text-slate-500 text-xs truncate">{companyName}</div>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 p-2 space-y-0.5 mt-1">
        {navItems.map((item) => {
          const href = base + item.href;
          const isActive = item.href === ""
            ? pathname === base || pathname === base + "/"
            : pathname.startsWith(href);
          return (
            <Link
              key={item.label}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group",
                collapsed && "justify-center px-2",
                isActive
                  ? "bg-primary-600 text-white shadow-sm"
                  : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
              )}
              title={collapsed ? item.label : undefined}
            >
              <item.icon className={cn("shrink-0", collapsed ? "w-5 h-5" : "w-4 h-4")} />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Bottom actions */}
      <div className="p-2 border-t border-slate-800 space-y-0.5">
        {[
          { icon: Bell, label: "Notifications" },
          { icon: HelpCircle, label: "Help & Docs" },
        ].map((item) => (
          <button
            key={item.label}
            className={cn(
              "w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-500 hover:bg-slate-800 hover:text-slate-300 transition-colors",
              collapsed && "justify-center px-2"
            )}
            title={collapsed ? item.label : undefined}
          >
            <item.icon className={cn("shrink-0", collapsed ? "w-5 h-5" : "w-4 h-4")} />
            {!collapsed && item.label}
          </button>
        ))}

        {/* User avatar */}
        <div className={cn("flex items-center gap-3 px-3 py-2 mt-1", collapsed && "justify-center px-2")}>
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-primary-400 to-teal-600 flex items-center justify-center text-white text-xs font-bold shrink-0">
            PS
          </div>
          {!collapsed && (
            <div className="min-w-0">
              <div className="text-slate-300 text-xs font-medium truncate">Priya Sharma</div>
              <div className="text-slate-600 text-xs truncate">Admin</div>
            </div>
          )}
        </div>
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-[72px] w-6 h-6 rounded-full bg-slate-700 border border-slate-600 flex items-center justify-center text-slate-400 hover:text-white hover:bg-slate-600 transition-colors z-10"
      >
        <ChevronLeft className={cn("w-3 h-3 transition-transform", collapsed && "rotate-180")} />
      </button>
    </aside>
  );
}
