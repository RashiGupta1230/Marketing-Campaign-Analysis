import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { cn } from "@/lib/utils";

interface KPICardProps {
  label: string;
  value: string;
  delta?: string;
  deltaType?: "positive" | "negative" | "neutral";
  caption?: string;
  icon?: React.ReactNode;
  accent?: boolean;
}

export function KPICard({ label, value, delta, deltaType = "neutral", caption, icon, accent = false }: KPICardProps) {
  const DeltaIcon = deltaType === "positive" ? TrendingUp : deltaType === "negative" ? TrendingDown : Minus;
  return (
    <div className={cn(
      "bg-white rounded-xl border p-5 transition-all duration-200 ease-out hover:shadow-card-hover hover:-translate-y-0.5 group",
      accent ? "border-blue-300 ring-1 ring-blue-100 shadow-sm" : "border-slate-200/90 shadow-card"
    )}>
      <div className="flex items-start justify-between mb-3">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">{label}</span>
        {icon && (
          <div className="w-7 h-7 rounded-lg bg-slate-100 group-hover:bg-blue-50 transition-colors flex items-center justify-center text-slate-500 group-hover:text-blue-600">
            {icon}
          </div>
        )}
      </div>
      <div className="text-2xl font-extrabold text-slate-900 mb-1.5 tracking-tight">{value}</div>
      {delta && (
        <div className={cn("flex items-center gap-1 text-xs font-semibold",
          deltaType === "positive" ? "text-emerald-600" : deltaType === "negative" ? "text-red-500" : "text-slate-500"
        )}>
          <DeltaIcon className="w-3.5 h-3.5" />{delta}
        </div>
      )}
      {caption && <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{caption}</p>}
    </div>
  );
}
