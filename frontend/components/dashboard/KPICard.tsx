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
      "bg-white rounded-xl border p-5 transition-all duration-200 hover:shadow-md group",
      accent ? "border-primary-200 ring-1 ring-primary-100" : "border-slate-200"
    )}>
      <div className="flex items-start justify-between mb-3">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{label}</span>
        {icon && (
          <div className="w-7 h-7 rounded-lg bg-slate-100 group-hover:bg-primary-50 transition-colors flex items-center justify-center text-slate-400 group-hover:text-primary-600">
            {icon}
          </div>
        )}
      </div>
      <div className="text-2xl font-bold text-slate-900 mb-1.5 tracking-tight">{value}</div>
      {delta && (
        <div className={cn("flex items-center gap-1 text-xs font-medium",
          deltaType === "positive" ? "text-emerald-600" : deltaType === "negative" ? "text-red-500" : "text-slate-500"
        )}>
          <DeltaIcon className="w-3 h-3" />{delta}
        </div>
      )}
      {caption && <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{caption}</p>}
    </div>
  );
}

