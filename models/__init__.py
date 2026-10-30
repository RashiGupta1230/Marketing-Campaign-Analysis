"""
Models package initialization.
"""

from .attribution import (
    attach_multi_touch_attribution,
    compute_attribution_weights,
    compute_markov_removal_effects,
    compute_shapley_coalition_values,
)
from .optimizer import (
    calculate_diminishing_returns,
    generate_dynamic_ai_recommendation,
    get_channel_hill_curve,
    solve_optimal_budget,
)

__all__ = [
    "compute_attribution_weights",
    "compute_markov_removal_effects",
    "compute_shapley_coalition_values",
    "attach_multi_touch_attribution",
    "get_channel_hill_curve",
    "calculate_diminishing_returns",
    "solve_optimal_budget",
    "generate_dynamic_ai_recommendation",
]
