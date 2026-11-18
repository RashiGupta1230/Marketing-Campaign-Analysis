import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number, symbol = "₹", compact = false): string {
  if (compact) {
    if (value >= 1_00_000) return `${symbol}${(value / 1_00_000).toFixed(1)}L`;
    if (value >= 1_000) return `${symbol}${(value / 1_000).toFixed(0)}K`;
  }
  return `${symbol}${value.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
}

export function formatPercent(value: number, decimals = 1): string {
  return `${value >= 0 ? "+" : ""}${value.toFixed(decimals)}%`;
}

export function slugify(text: string): string {
  return text.toLowerCase().replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, "");
}

