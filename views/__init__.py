"""
Views package initialization.
"""

from .charts import (
    generate_executive_brief_html,
    get_model_revenue_col,
    render_attribution_comparison,
    render_campaign_drilldown,
    render_cohort_retention,
    render_funnel_pipeline,
    render_roas_by_channel,
    render_spend_vs_revenue,
)

__all__ = [
    "get_model_revenue_col",
    "render_roas_by_channel",
    "render_spend_vs_revenue",
    "render_funnel_pipeline",
    "render_cohort_retention",
    "render_attribution_comparison",
    "render_campaign_drilldown",
    "generate_executive_brief_html",
]
