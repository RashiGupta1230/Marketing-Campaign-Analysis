"use client";

import { useState, useEffect, useCallback } from "react";
import { attributionApi, optimizerApi } from "@/lib/api";
import type { AttributionResult, OptimizerResult } from "@/types";

/** Fetch attribution data for a given scenario + model */
export function useAttribution(scenario: string, model: string, channels?: string[]) {
  const [data, setData] = useState<AttributionResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await attributionApi.compute({ scenario, attribution_model: model, channels });
      setData(res.data);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Failed to fetch attribution data";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, [scenario, model, channels]);

  useEffect(() => { fetch(); }, [fetch]);

  return { data, loading, error, refetch: fetch };
}

/** Solve budget allocation with SLSQP optimizer */
export function useOptimizer() {
  const [result, setResult] = useState<OptimizerResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const solve = useCallback(async (params: {
    target_budget: number;
    scenario: string;
    objective: string;
    gross_margin_pct: number;
    attribution_model: string;
    channels?: string[];
  }) => {
    setLoading(true);
    setError(null);
    try {
      const res = await optimizerApi.solve(params);
      setResult(res.data);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Optimizer failed";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { result, loading, error, solve };
}
