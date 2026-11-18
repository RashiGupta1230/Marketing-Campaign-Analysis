import { Search, Bell, ChevronDown } from "lucide-react";

interface TopNavProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
}

export function TopNav({ title, subtitle, actions }: TopNavProps) {
  return (
    <header className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0">
      <div>
        <h1 className="text-sm font-semibold text-slate-900">{title}</h1>
        {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-3">
        <div className="hidden md:flex items-center gap-2 bg-slate-100 rounded-lg px-3 py-1.5 w-52 cursor-pointer hover:bg-slate-200 transition-colors">
          <Search className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs text-slate-400">Search... ⌘K</span>
        </div>
        <button className="relative w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center text-slate-500 transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-primary-600" />
        </button>
        {actions}
        <button className="flex items-center gap-2 hover:bg-slate-100 rounded-lg pl-2 pr-3 py-1.5 transition-colors">
          <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary-400 to-teal-600 flex items-center justify-center text-white text-xs font-bold">PS</div>
          <ChevronDown className="w-3 h-3 text-slate-400" />
        </button>
      </div>
    </header>
  );
}

