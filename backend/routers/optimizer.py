"""Optimizer router — wraps models/optimizer.py SLSQP engine"""
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from data.generator import generate_synthetic_data
from models.attribution import attach_multi_touch_attribution
from models.optimizer import (
    solve_optimal_budget,
    calculate_diminishing_returns,
    generate_dynamic_ai_recommendation,
    scale_curves_by_attribution,
)
from core.config import SCENARIO_CONFIGS
from views.charts import get_model_revenue_col
from dependencies.auth import TokenData, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


class OptimizerRequest(BaseModel):
    target_budget: float
    channels: Optional[List[str]] = None
    scenario: str = "E-Commerce (B2C)"
    objective: str = "revenue"
    gross_margin_pct: float = 0.65
    attribution_model: str = "Markov Chain"


@router.post("/solve")
async def solve_budget(
    req: OptimizerRequest,
    current_user: TokenData = Depends(get_current_user),
):
    if req.scenario not in SCENARIO_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unknown scenario '{req.scenario}'.")
    try:
        meta = SCENARIO_CONFIGS[req.scenario]
        hill_curves = meta["hill_curves"]

        df, _ = generate_synthetic_data(scenario=req.scenario, seed=42)
        df = attach_multi_touch_attribution(df)

        rev_col = get_model_revenue_col(req.attribution_model)
        tot_rev = float(df[rev_col].sum()) or 1.0
        channels = req.channels or list(hill_curves.keys())

        weights = {
            ch: float(df[df["channel"] == ch][rev_col].sum() / tot_rev)
            for ch in channels
        }
        scaled = scale_curves_by_attribution(hill_curves, weights, channels)

        baseline = {
            ch: meta["default_allocations"].get(ch, req.target_budget / len(channels))
            for ch in channels
        }

        # FIX O-01: Check solver success before using result
        opt = solve_optimal_budget(
            req.target_budget, scaled, channels,
            gross_margin_pct=req.gross_margin_pct,
            objective=req.objective,
        )
        if opt is None:
            raise HTTPException(
                status_code=422,
                detail="SLSQP solver did not converge. Try adjusting budget or channel constraints.",
            )

        base_res = calculate_diminishing_returns(baseline, scaled, gross_margin_pct=req.gross_margin_pct)
        opt_res  = calculate_diminishing_returns(opt, scaled, gross_margin_pct=req.gross_margin_pct)

        ai_rec = generate_dynamic_ai_recommendation(
            baseline, scaled,
            currency_formatter=lambda v: f"₹{v:,.0f}",
            gross_margin_pct=req.gross_margin_pct,
            attribution_model_name=req.attribution_model,
        )

        channel_results = []
        for ch in channels:
            b, o = base_res.get(ch, {}), opt_res.get(ch, {})
            bs, os_ = float(b.get("spend", 0)), float(o.get("spend", 0))
            channel_results.append({
                "channel": ch,
                "base_spend": bs,
                "optimized_spend": os_,
                "delta": os_ - bs,
                "delta_pct": (os_ - bs) / bs * 100 if bs > 0 else 0,
                "projected_roas": float(o.get("roas", 0)),
                "marginal_roas": float(o.get("m_roas", 0)),
                "revenue_impact": float(o.get("revenue", 0)) - float(b.get("revenue", 0)),
                "profit_impact":  float(o.get("net_profit", 0)) - float(b.get("net_profit", 0)),
            })

        tot_rev_opt   = sum(r.get("revenue", 0) for r in opt_res.values())
        tot_spend_opt = sum(r.get("spend", 0) for r in opt_res.values())

        return {
            "target_budget": req.target_budget,
            "objective": req.objective,
            "projected_total_revenue": float(tot_rev_opt),
            "projected_blended_roas": float(tot_rev_opt / tot_spend_opt) if tot_spend_opt > 0 else 0,
            "channels": channel_results,
            "ai_recommendation": {
                "title":  ai_rec.get("title", ""),
                "impact": ai_rec.get("impact", ""),
                "body":   ai_rec.get("body", ""),
            },
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Optimizer solve error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error during budget optimization.")


@router.get("/scenarios/{scenario}/hill-curves")
async def get_hill_curves(
    scenario: str,
    current_user: TokenData = Depends(get_current_user),
):
    meta = SCENARIO_CONFIGS.get(scenario)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario}' not found.")
    return {
        "scenario": scenario,
        "hill_curves": meta["hill_curves"],
        "default_allocations": meta["default_allocations"],
        "target_budget": meta["target_budget"],
    }
