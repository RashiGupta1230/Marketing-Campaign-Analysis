"""Attribution router — wraps models/attribution.py"""
import logging
import sys
import os

# sys.path already set by main.py; this insert is a no-op safety net
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from data.generator import generate_synthetic_data
from models.attribution import attach_multi_touch_attribution
from core.config import SCENARIO_CONFIGS
from dependencies.auth import TokenData, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

MODEL_COL = {
    "First-click":   "revenue_first_click",
    "Last-click":    "revenue_last_click",
    "Linear":        "revenue_linear",
    "Markov Chain":  "revenue_markov",
    "Shapley Value": "revenue_shapley",
}


class AttributionRequest(BaseModel):
    scenario: str = "E-Commerce (B2C)"
    attribution_model: str = "Markov Chain"
    channels: Optional[List[str]] = None
    seed: int = 42


@router.post("/compute")
async def compute_attribution(
    req: AttributionRequest,
    current_user: TokenData = Depends(get_current_user),
):
    if req.scenario not in SCENARIO_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unknown scenario '{req.scenario}'. Valid: {list(SCENARIO_CONFIGS.keys())}")
    try:
        df, _ = generate_synthetic_data(scenario=req.scenario, seed=req.seed)
        df = attach_multi_touch_attribution(df)
        if req.channels:
            df = df[df["channel"].isin(req.channels)]

        rev_col = MODEL_COL.get(req.attribution_model, "revenue_markov")
        total_spend = float(df["spend"].sum())
        total_rev = float(df["revenue"].sum())
        total_attr = float(df[rev_col].sum())

        channels = []
        for ch in sorted(df["channel"].unique()):
            ch_df = df[df["channel"] == ch]
            ch_spend = float(ch_df["spend"].sum())
            ch_attr = float(ch_df[rev_col].sum())
            channels.append({
                "channel": ch,
                "spend": ch_spend,
                "attributed_revenue": ch_attr,
                "roas": ch_attr / ch_spend if ch_spend > 0 else 0,
                "conversions": int(ch_df["conversions"].sum()),
                "weight": ch_attr / total_attr if total_attr > 0 else 0,
            })

        return {
            "model": req.attribution_model,
            "total_spend": total_spend,
            "total_revenue": total_rev,
            "total_attributed_revenue": total_attr,
            "blended_roas": total_attr / total_spend if total_spend > 0 else 0,
            "channels": channels,
            "revenue_conserved": abs(total_attr - total_rev) / max(total_rev, 1) < 0.001,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Attribution compute error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error during attribution computation.")


@router.post("/compare")
async def compare_models(
    scenario: str = Query("E-Commerce (B2C)"),
    seed: int = Query(42),
    current_user: TokenData = Depends(get_current_user),
):
    if scenario not in SCENARIO_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Unknown scenario '{scenario}'.")
    try:
        df, _ = generate_synthetic_data(scenario=scenario, seed=seed)
        df = attach_multi_touch_attribution(df)
        channels = sorted(df["channel"].unique().tolist())
        comparison = []
        for ch in channels:
            ch_df = df[df["channel"] == ch]
            comparison.append({
                "channel": ch,
                "first_click":   float(ch_df["revenue_first_click"].sum()),
                "last_click":    float(ch_df["revenue_last_click"].sum()),
                "linear":        float(ch_df["revenue_linear"].sum()),
                "markov_chain":  float(ch_df["revenue_markov"].sum()),
                "shapley_value": float(ch_df["revenue_shapley"].sum()),
            })
        return {"channels": comparison, "total_revenue": float(df["revenue"].sum())}
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Attribution compare error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error during model comparison.")


@router.get("/scenarios")
async def list_scenarios():
    """Public endpoint — no auth required (used for onboarding/landing page)."""
    return {"scenarios": [
        {
            "key": k,
            "description": v["description"],
            "target_budget": v["target_budget"],
            "channels": list(v["default_allocations"].keys()),
        }
        for k, v in SCENARIO_CONFIGS.items()
    ]}
