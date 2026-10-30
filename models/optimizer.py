"""
Diminishing Returns, Marginal ROAS, and Scipy SLSQP Budget Optimizer Engine.
"""

from typing import Any, Dict, List, Optional
import numpy as np
from scipy.optimize import minimize


def get_channel_hill_curve(
    ch: str,
    hill_curves: Dict[str, Dict[str, float]],
    target_budget: float = 800000.0,
    aov_estimate: float = 2400.0
) -> Dict[str, float]:
    """Retrieve or dynamically synthesize Hill parameters for any marketing channel with owned baseline demand."""
    if ch in hill_curves:
        curve = hill_curves[ch].copy()
    else:
        curve = {
            "max_scale": max(100.0, target_budget / (aov_estimate * 3.5)),
            "half_sat": max(50000.0, target_budget * 0.25),
            "alpha": 0.75,
            "aov": aov_estimate,
        }

    # Model owned media baseline demand (organic web traffic or existing email subscriber base)
    if "baseline_conversions" not in curve:
        ch_lower = ch.lower()
        if "website" in ch_lower or "organic" in ch_lower:
            curve["baseline_conversions"] = float(curve["max_scale"] * 0.12)
        elif "email" in ch_lower or "crm" in ch_lower:
            curve["baseline_conversions"] = float(curve["max_scale"] * 0.08)
        else:
            curve["baseline_conversions"] = 0.0

    return curve


def scale_curves_by_attribution(
    hill_curves: Dict[str, Dict[str, float]],
    attribution_weights: Optional[Dict[str, float]] = None,
    channels: Optional[List[str]] = None,
) -> Dict[str, Dict[str, float]]:
    """
    Scale channel saturation capacity (max_scale) proportionally to active attribution model weights.
    Ensures that switching attribution models (e.g., Last-Click vs. Markov) directly alters
    channel capacity, marginal returns, and optimal budget allocations.
    """
    if not attribution_weights:
        return hill_curves

    active_channels = channels or list(attribution_weights.keys())
    n = max(len(active_channels), 1)
    baseline_uniform = 1.0 / n

    scaled = {}
    for ch, curve in hill_curves.items():
        curve_copy = curve.copy()
        if ch in attribution_weights:
            w = attribution_weights[ch]
            scale_ratio = float(np.clip(w / baseline_uniform, 0.35, 2.50))
            curve_copy["max_scale"] = float(curve["max_scale"] * scale_ratio)
        scaled[ch] = curve_copy

    return scaled


def calculate_diminishing_returns(
    allocations: Dict[str, float],
    hill_curves: Dict[str, Dict[str, float]],
    gross_margin_pct: float = 1.0,
) -> Dict[str, Dict[str, float]]:
    """Compute projected conversions, revenue, net profit, and instantaneous marginal ROAS / profit."""
    results = {}
    for ch, spend in allocations.items():
        curve = get_channel_hill_curve(ch, hill_curves)
        k = curve["half_sat"]
        alpha = curve["alpha"]
        max_scale = curve["max_scale"]
        aov = curve["aov"]
        base_conv = float(curve.get("baseline_conversions", 0.0))

        if spend <= 0:
            b_rev = round(base_conv * aov, 2)
            b_prof = round(b_rev * gross_margin_pct, 2)
            results[ch] = {
                "spend": 0.0,
                "conversions": int(base_conv),
                "revenue": b_rev,
                "gross_profit": b_prof,
                "net_profit": b_prof,
                "roas": 0.0,
                "m_roas": 0.0,
                "m_profit": -1.0,
            }
            continue

        ratio = spend / (spend + k)
        conversions = int(base_conv + max_scale * (ratio ** alpha))
        revenue = round(conversions * aov, 2)
        gross_profit = round(revenue * gross_margin_pct, 2)
        net_profit = round(gross_profit - spend, 2)
        roas = (revenue / spend) if spend > 0 else 0.0

        # Instantaneous derivative d(conv)/d(spend)
        d_conv = max_scale * alpha * (ratio ** (alpha - 1.0)) * (k / ((spend + k) ** 2.0))
        m_roas = round(d_conv * aov, 2)
        m_profit = round((m_roas * gross_margin_pct) - 1.0, 2)

        results[ch] = {
            "spend": float(spend),
            "conversions": conversions,
            "revenue": revenue,
            "gross_profit": gross_profit,
            "net_profit": net_profit,
            "roas": roas,
            "m_roas": m_roas,
            "m_profit": m_profit,
        }

    return results


def solve_optimal_budget(
    target_budget: float,
    hill_curves: Dict[str, Dict[str, float]],
    channels: List[str],
    gross_margin_pct: float = 1.0,
    objective: str = "revenue",
) -> Dict[str, float]:
    """
    Solve for global revenue-maximizing or net-profit-maximizing budget allocation vector via Scipy SLSQP.
    Resilient to arbitrary custom channels with no KeyErrors.
    """
    if not channels:
        return {}

    # Pre-resolve curves for all channels
    resolved_curves = [get_channel_hill_curve(ch, hill_curves, target_budget=target_budget) for ch in channels]

    def neg_objective(x: np.ndarray) -> float:
        tot_metric = 0.0
        for i, curve in enumerate(resolved_curves):
            spend = x[i]
            k = curve["half_sat"]
            alpha = curve["alpha"]
            max_scale = curve["max_scale"]
            aov = curve["aov"]
            base_conv = float(curve.get("baseline_conversions", 0.0))

            ratio = spend / (spend + k)
            conv = base_conv + max_scale * (ratio ** alpha)
            ch_rev = conv * aov
            if objective == "profit":
                tot_metric += (ch_rev * gross_margin_pct) - spend
            else:
                tot_metric += ch_rev
        return -tot_metric

    cons = ({"type": "eq", "fun": lambda x: np.sum(x) - target_budget})
    min_bound = min(10000.0, target_budget / (len(channels) * 4))
    max_bound = target_budget * 0.70
    bounds = [(min_bound, max_bound) for _ in channels]
    x0 = [target_budget / len(channels)] * len(channels)

    res = minimize(neg_objective, x0, method="SLSQP", bounds=bounds, constraints=cons)
    if res.success:
        return {ch: float(int(round(res.x[i], -3))) for i, ch in enumerate(channels)}
    else:
        # Fallback to balanced split
        return {ch: float(int(round(target_budget / len(channels), -3))) for ch in channels}


def generate_dynamic_ai_recommendation(
    baseline_allocations: Dict[str, float],
    hill_curves: Dict[str, Dict[str, float]],
    currency_formatter=None,
    gross_margin_pct: float = 1.0,
    attribution_model_name: str = "Markov Chain",
) -> Dict[str, Any]:
    """Dynamically analyze marginal returns across channels to compute optimal budget shift."""
    def fmt(val: float) -> str:
        if currency_formatter:
            return currency_formatter(val)
        return f"₹{val:,.0f}"

    base_res = calculate_diminishing_returns(baseline_allocations, hill_curves, gross_margin_pct=gross_margin_pct)

    sorted_by_mroas = sorted(
        [(ch, res["m_roas"]) for ch, res in base_res.items() if res["spend"] > 0],
        key=lambda x: x[1]
    )

    if len(sorted_by_mroas) >= 2:
        from_ch, from_mroas = sorted_by_mroas[0]
        to_ch, to_mroas = sorted_by_mroas[-1]

        shift_amount = 50000.0
        base_from_spend = baseline_allocations.get(from_ch, 0)
        if base_from_spend < shift_amount:
            shift_amount = base_from_spend * 0.25

        test_alloc = baseline_allocations.copy()
        test_alloc[from_ch] -= shift_amount
        test_alloc[to_ch] += shift_amount

        test_res = calculate_diminishing_returns(test_alloc, hill_curves, gross_margin_pct=gross_margin_pct)

        base_conv = sum(r["conversions"] for r in base_res.values())
        test_conv = sum(r["conversions"] for r in test_res.values())
        conv_gain_pct = ((test_conv - base_conv) / base_conv * 100) if base_conv > 0 else 0

        base_rev = sum(r["revenue"] for r in base_res.values())
        test_rev = sum(r["revenue"] for r in test_res.values())
        rev_gain_pct = ((test_rev - base_rev) / base_rev * 100) if base_rev > 0 else 0

        return {
            "title": f"Recommended: Shift {fmt(shift_amount)} from {from_ch} to {to_ch}",
            "impact": f"Projected Impact: +{conv_gain_pct:.1f}% Conversions · +{rev_gain_pct:.1f}% Revenue",
            "body": (
                f"<strong>Analytical Rationale ({attribution_model_name} Lens):</strong> Empirical marginal return curves indicate "
                f"<strong>{from_ch}</strong> has reached diminishing efficiency with a marginal ROAS of "
                f"<strong>{from_mroas:.2f}x</strong>. Meanwhile, <strong>{to_ch}</strong> retains substantial "
                f"unlocked capacity with a marginal ROAS of <strong>{to_mroas:.2f}x</strong>. "
                f"Rebalancing {fmt(shift_amount)} shifts capital along the efficient frontier."
            ),
            "from_ch": from_ch,
            "to_ch": to_ch,
            "shift_amount": shift_amount,
        }

    return {
        "title": "Portfolio In Equilibrium",
        "impact": "Current channel allocations are balanced within marginal tolerance.",
        "body": "No significant marginal ROAS disparity detected across active channels.",
        "from_ch": "Social",
        "to_ch": "Email",
        "shift_amount": 50000.0,
    }
