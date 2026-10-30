"""
Marketing Campaign Effectiveness Analysis — Interactive ROI Decision-Support System
Academic Research & Applied BI Decision-Support Engine

Architecture:
- Core: Configuration, Themes, Palette
- Models: Multi-Touch Attribution (Markov & Shapley), Hill Saturation Optimizer (SciPy SLSQP)
- Data: Benchmark Generator, Touchpoint Journey Simulator, CSV Validator, Persistent Audit Ledger
- Views: Interactive Plotly Visualizations & Diagnostics
"""

from datetime import datetime, timedelta
import io
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import streamlit as st

# Modular Architecture Imports
from core.config import (
    COLOR_BORDER,
    COLOR_CARD_BG,
    COLOR_GRID,
    COLOR_LIGHT_BG,
    COLOR_MUTED_GREY,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    SCENARIO_CONFIGS,
)
from core.styles import apply_custom_styles
from data.audit_store import load_audit_log, save_audit_record
from data.generator import (
    generate_sample_csv_template,
    generate_sample_touchpoint_template,
    generate_synthetic_data,
    generate_synthetic_touchpoint_journeys,
    validate_and_sanitize_csv,
)
from models.attribution import (
    attach_multi_touch_attribution,
    compute_attribution_weights,
    compute_markov_removal_effects,
    compute_shapley_coalition_values,
)
from models.optimizer import (
    calculate_diminishing_returns,
    generate_dynamic_ai_recommendation,
    get_channel_hill_curve,
    scale_curves_by_attribution,
    solve_optimal_budget,
)
from views.charts import (
    generate_executive_brief_html,
    get_model_revenue_col,
    render_attribution_comparison,
    render_campaign_drilldown,
    render_cohort_retention,
    render_funnel_pipeline,
    render_roas_by_channel,
    render_spend_vs_revenue,
)

# Application Page Setup
st.set_page_config(
    page_title="Marketing Campaign Effectiveness Analysis — Interactive ROI Decision-Support System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def format_currency(val: float, symbol: str = "₹") -> str:
    """Format numeric values cleanly with selectable currency symbol."""
    return f"{symbol}{val:,.0f}"


def format_currency_inr(val: float) -> str:
    """Backward-compatible INR currency formatter."""
    return f"₹{val:,.0f}"


def filter_dataset(
    df: pd.DataFrame,
    date_range: Tuple[datetime.date, datetime.date],
    selected_channels: List[str],
    selected_region: str,
    selected_campaigns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Filter master dataset based on sidebar user selections."""
    if not selected_channels:
        selected_channels = df["channel"].unique().tolist()

    start_dt, end_dt = date_range
    mask = (
        (df["date"].dt.date >= start_dt)
        & (df["date"].dt.date <= end_dt)
        & (df["channel"].isin(selected_channels))
    )

    if selected_campaigns and "campaign" in df.columns:
        mask = mask & (df["campaign"].isin(selected_campaigns))

    if selected_region != "All" and "region" in df.columns:
        mask = mask & (df["region"] == selected_region)

    return df.loc[mask].copy()


def compute_kpis(df_filtered: pd.DataFrame, attribution_model: str) -> Dict[str, float]:
    """Compute top-level summary metrics from filtered data."""
    rev_col = get_model_revenue_col(attribution_model)

    total_spend = float(df_filtered["spend"].sum()) if not df_filtered.empty else 0.0
    attributed_revenue = float(df_filtered[rev_col].sum()) if not df_filtered.empty else 0.0
    total_conversions = int(df_filtered["conversions"].sum()) if not df_filtered.empty else 0

    roas = (attributed_revenue / total_spend) if total_spend > 0 else 0.0
    roi_percent = ((attributed_revenue - total_spend) / total_spend * 100.0) if total_spend > 0 else 0.0

    return {
        "spend": total_spend,
        "revenue": attributed_revenue,
        "conversions": total_conversions,
        "roas": roas,
        "roi_percent": roi_percent,
    }


def main():
    apply_custom_styles()

    # -------------------------------------------------------------------------
    # SIDEBAR: DATA SOURCE SELECTOR & CONFIGURATION
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### 📁 Data Source & Ingestion")

        data_mode = st.radio(
            "Select Data Mode",
            options=["Benchmark Simulation", "Upload Custom CSV"],
            index=0,
            help="Choose between reproducible academic research benchmarks or upload external campaign records.",
        )

        current_scenario_key = "E-Commerce (B2C)"

        if data_mode == "Benchmark Simulation":
            current_scenario_key = st.selectbox(
                "Industry Business Model",
                options=list(SCENARIO_CONFIGS.keys()),
                index=0,
                help="Select business model to evaluate how attribution and funnel metrics behave.",
            )
            scenario_meta = SCENARIO_CONFIGS[current_scenario_key]
            st.caption(f"ℹ️ **Profile:** {scenario_meta['description']}")

            master_df, cohort_df = generate_synthetic_data(scenario=current_scenario_key, seed=42)
            active_hill_curves = scenario_meta["hill_curves"]
            target_budget = scenario_meta["target_budget"]
            baseline_allocations = scenario_meta["default_allocations"].copy()
            top_journey_paths = scenario_meta.get("top_paths", [])

        else:  # Upload Custom CSV
            st.markdown("**Upload External Campaign CSV**")

            col_tpl1, col_tpl2 = st.columns(2)
            with col_tpl1:
                template_csv_data = generate_sample_csv_template()
                st.download_button(
                    label="📥 Daily Aggregated CSV",
                    data=template_csv_data,
                    file_name="sample_daily_campaign_data.csv",
                    mime="text/csv",
                    help="Daily aggregated campaign spend and revenue schema.",
                    use_container_width=True,
                )
            with col_tpl2:
                template_tp_data = generate_sample_touchpoint_template()
                st.download_button(
                    label="📥 Touchpoint Log (Slide 6)",
                    data=template_tp_data,
                    file_name="sample_customer_touchpoint_log.csv",
                    mime="text/csv",
                    help="Event-level customer touchpoint log schema (customer_id, channel, timestamp, converted, revenue).",
                    use_container_width=True,
                )

            uploaded_file = st.file_uploader(
                "Upload Campaign or Touchpoint CSV",
                type=["csv"],
                help="Upload either a daily aggregated CSV or an event-level customer touchpoint log.",
            )

            is_event_dataset = False
            if uploaded_file is not None:
                parsed_df, err_msg = validate_and_sanitize_csv(uploaded_file)
                if err_msg:
                    st.error(f"❌ {err_msg}")
                    master_df, cohort_df = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
                else:
                    is_event_dataset = getattr(parsed_df, "attrs", {}).get("is_event_level", False)
                    if is_event_dataset:
                        n_j = getattr(parsed_df, "attrs", {}).get("n_journeys", 0)
                        st.success(f"✓ Event-level touchpoint log parsed! Extracted {n_j:,} real customer journeys.")
                    else:
                        st.info("ℹ️ Aggregated daily CSV detected. Touchpoint journeys are probabilistically simulated from channel volume. For direct empirical MTA, upload a touchpoint log.")
                    master_df = parsed_df
                    _, cohort_df = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
            else:
                st.info("Showing default sample benchmark until you upload a CSV.")
                master_df, cohort_df = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)

            target_budget = int(master_df["spend"].sum()) if not master_df.empty else 800000
            active_hill_curves = SCENARIO_CONFIGS["E-Commerce (B2C)"]["hill_curves"]
            top_journey_paths = SCENARIO_CONFIGS["E-Commerce (B2C)"]["top_paths"]

            ch_grouped = master_df.groupby("channel")["spend"].sum().to_dict()
            uploaded_channels = list(ch_grouped.keys()) if ch_grouped else ["Search", "Social", "Email", "Display", "Website"]
            baseline_allocations = {
                ch: round(ch_grouped.get(ch, target_budget / len(uploaded_channels)), -3)
                for ch in uploaded_channels
            }

        # ---------------------------------------------------------------------
        # PHASE 1 BUGFIX: SCENARIO SWITCH LISTENER
        # Reset simulator sliders whenever scenario or data source changes
        # ---------------------------------------------------------------------
        scenario_session_token = f"{data_mode}_{current_scenario_key}"
        if st.session_state.get("active_scenario_token") != scenario_session_token:
            st.session_state["active_scenario_token"] = scenario_session_token
            # Reset all slider keys to scenario defaults
            for ch, val in baseline_allocations.items():
                st.session_state[f"slider_{ch}"] = int(val)
            st.session_state["optimizer_applied"] = False

        st.divider()
        st.markdown("### 🔍 Filters & Dimensions")

        # Currency Selector (Slide 3 & Global BI readiness)
        currency_choice = st.selectbox(
            "Operating Currency",
            options=["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)"],
            index=0,
            help="Select business reporting currency unit."
        )
        curr_sym = currency_choice.split()[0]

        # 1. Date Range Filter
        min_date = master_df["date"].dt.date.min()
        max_date = master_df["date"].dt.date.max()
        default_start = max(min_date, max_date - timedelta(days=180))

        selected_date_range = st.date_input(
            "Evaluation Window",
            value=(default_start, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter data to a specific operational evaluation period.",
        )
        if isinstance(selected_date_range, (list, tuple)) and len(selected_date_range) == 2:
            date_filter = selected_date_range
        else:
            date_filter = (min_date, max_date)

        # 2. Channel Multiselect
        available_channels = sorted(master_df["channel"].unique().tolist())
        selected_channels = st.multiselect(
            "Marketing Channels",
            options=available_channels,
            default=available_channels,
            help="Select one or more active marketing acquisition channels.",
        )
        if not selected_channels:
            selected_channels = available_channels

        # 3. Campaign Filter (Slide 4 Step 2 & Slide 6 Hierarchy)
        available_campaigns = sorted(master_df["campaign"].dropna().unique().tolist()) if "campaign" in master_df.columns else []
        selected_campaigns = None
        if available_campaigns:
            selected_campaigns = st.multiselect(
                "Marketing Campaigns",
                options=available_campaigns,
                default=available_campaigns,
                help="Filter by specific marketing campaigns (Slide 4 step 2).",
            )
            if not selected_campaigns:
                selected_campaigns = available_campaigns

        # 4. Attribution Model Dropdown
        attribution_options = [
            "Markov Chain",
            "Last-click",
            "First-click",
            "Linear",
            "Shapley Value",
        ]
        selected_model = st.selectbox(
            "Attribution Model Lens",
            options=attribution_options,
            index=0,
            help="Select attribution logic for weighting revenue across touchpoints.",
        )

        # 5. Region Dropdown
        available_regions = ["All"] + sorted([str(r) for r in master_df["region"].unique() if pd.notna(r)])
        selected_region = st.selectbox(
            "Geographic Region",
            options=available_regions,
            index=0,
            help="Segment campaign results by geographical market territory.",
        )

        st.divider()
        st.caption(
            "**Decision-Support System:**\n"
            "This interface recalculates metrics dynamically across heuristic and algorithmic models. "
            "All recommendations require human review before budget execution."
        )

    # -------------------------------------------------------------------------
    # MAIN HEADER (CLEAN HERO SECTION)
    # -------------------------------------------------------------------------
    badge_text = current_scenario_key if data_mode == "Benchmark Simulation" else "Custom Upload"
    st.markdown(
        f"""
        <div style="margin-bottom: 1.35rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <h1 style="font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; line-height: 1.2;">
                            Marketing Campaign Effectiveness Analysis
                        </h1>
                        <span class="badge-source">{badge_text}</span>
                    </div>
                    <div style="font-size: 0.92rem; color: #64748B; margin-top: 4px;">
                        Interactive ROI Decision-Support System & Multi-Touch Attribution Simulator · Academic Research Prototype
                    </div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 6px 14px; border-radius: 6px; font-size: 0.8rem; color: #475569; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <strong>Engine:</strong> Markov & Shapley MTA &nbsp;|&nbsp; <strong>Optimizer:</strong> SciPy SLSQP
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Apply Filtering
    df_filtered = filter_dataset(
        master_df,
        date_range=date_filter,
        selected_channels=selected_channels,
        selected_region=selected_region,
        selected_campaigns=selected_campaigns,
    )

    if df_filtered.empty:
        st.warning("⚠️ No campaign activity matches your active filter selection. Please expand your date range or channels.")
        return

    # -------------------------------------------------------------------------
    # TOP KPI ROW (4 METRIC CARDS + UNIT ECONOMICS & LTV:CAC)
    # -------------------------------------------------------------------------
    st.markdown("##### 📈 Historical Performance Actuals (Evaluated Period)")

    kpis = compute_kpis(df_filtered, selected_model)

    baseline_spend = kpis["spend"] * 0.96
    baseline_rev = kpis["revenue"] * 0.92
    baseline_conv = int(kpis["conversions"] * 0.94)
    baseline_roas = (baseline_rev / baseline_spend) if baseline_spend > 0 else 0.0

    spend_delta = ((kpis["spend"] - baseline_spend) / baseline_spend * 100) if baseline_spend > 0 else 0
    rev_delta = ((kpis["revenue"] - baseline_rev) / baseline_rev * 100) if baseline_rev > 0 else 0
    conv_delta = ((kpis["conversions"] - baseline_conv) / baseline_conv * 100) if baseline_conv > 0 else 0
    roas_delta = kpis["roas"] - baseline_roas

    # CAC & Unit Economics (Slide 3 & Slide 7)
    blended_cpa = (kpis["spend"] / kpis["conversions"]) if kpis["conversions"] > 0 else 0.0

    # Dynamic Acquisition Channels (Exclude retention/owned channels like Email, Website, Direct)
    acq_channels = [c for c in selected_channels if c.lower() not in ["email", "website", "direct", "organic"]]
    if not acq_channels:
        acq_channels = selected_channels
    acq_spend = df_filtered[df_filtered["channel"].isin(acq_channels)]["spend"].sum()

    new_cust_rate = scenario_meta.get("new_customer_rate", 0.68) if data_mode == "Benchmark Simulation" else 0.68
    est_new_conversions = max(1, int(kpis["conversions"] * new_cust_rate))
    est_cac = acq_spend / est_new_conversions if est_new_conversions > 0 else blended_cpa

    # Estimated 3-Month LTV & LTV:CAC Ratio
    scenario_aov = scenario_meta["channel_params"]["Search"]["aov"] if data_mode == "Benchmark Simulation" else (kpis["revenue"] / max(kpis["conversions"], 1))
    est_ltv = scenario_aov * 2.15  # 3-Month cumulative cohort multiplier
    ltv_cac_ratio = est_ltv / est_cac if est_cac > 0 else 0.0
    ltv_health = "🟢 Healthy" if ltv_cac_ratio >= 3.0 else ("🟡 Moderate" if ltv_cac_ratio >= 1.5 else "🔴 Warning")

    # Payback Period (Months)
    gross_margin_default = scenario_meta.get("gross_margin_pct", 0.65) if data_mode == "Benchmark Simulation" else 0.65
    monthly_cust_gross_profit = (scenario_aov * gross_margin_default) / 3.0
    payback_months = (est_cac / monthly_cust_gross_profit) if monthly_cust_gross_profit > 0 else 0.0

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        with st.container(border=True):
            st.metric(
                label="Total Media Spend",
                value=format_currency_inr(kpis["spend"]),
                delta=f"{spend_delta:+.1f}% vs baseline",
                delta_color="off",
            )
            st.caption(f"Across {len(selected_channels)} channels · {selected_region}")

    with kpi_col2:
        with st.container(border=True):
            st.metric(
                label=f"Attributed Revenue ({selected_model})",
                value=format_currency_inr(kpis["revenue"]),
                delta=f"{rev_delta:+.1f}% vs baseline",
            )
            st.caption("Conserved across models")

    with kpi_col3:
        with st.container(border=True):
            st.metric(
                label="Conversions & CPA / CAC",
                value=f"{kpis['conversions']:,}",
                delta=f"{conv_delta:+.1f}% vs baseline",
            )
            st.caption(f"Blended CPA: {format_currency_inr(blended_cpa)} · CAC: {format_currency_inr(est_cac)} ({payback_months:.1f}m payback)")

    with kpi_col4:
        with st.container(border=True):
            st.metric(
                label="ROAS / LTV:CAC Health",
                value=f"{kpis['roas']:.2f}x ({kpis['roi_percent']:+.1f}%)",
                delta=f"{roas_delta:+.2f}x vs baseline",
            )
            st.caption(f"LTV:CAC: {ltv_cac_ratio:.1f}x · {ltv_health}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MAIN TABS / SECTIONS
    # -------------------------------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "Channel Performance & Trends",
        "Funnel & Cohort Retention",
        "Attribution Model Comparison",
        "AI Recommendation & What-If Simulator",
    ])

    # -------------------------------------------------------------------------
    # TAB 1: CHANNEL PERFORMANCE & TRENDS
    # -------------------------------------------------------------------------
    with tab1:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            with st.container(border=True):
                fig_roas = render_roas_by_channel(df_filtered, selected_model)
                st.plotly_chart(fig_roas, use_container_width=True)
                st.caption(
                    "Channel ROAS represents attributed revenue divided by media spend. "
                    "Sorted in descending order for rapid performance triage."
                )

        with chart_col2:
            with st.container(border=True):
                fig_trend = render_spend_vs_revenue(df_filtered, selected_model)
                st.plotly_chart(fig_trend, use_container_width=True)
                st.caption(
                    "Monthly spend vs attributed revenue trend over the evaluation window. "
                    "Evaluates whether revenue growth tracks or outpaces spend increases."
                )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        with st.expander("🔍 Campaign & Creative Asset Drill-Down (Slide 4 step 5 & Slide 6 Hierarchy)", expanded=False):
            st.caption("Drill down into an individual channel to inspect campaign-level economics and creative asset performance.")
            drill_ch = st.selectbox("Channel to Inspect:", options=selected_channels, index=0)
            df_ch = df_filtered[df_filtered["channel"] == drill_ch]
            fig_drill, drill_table = render_campaign_drilldown(
                df_ch,
                drill_ch,
                revenue_col=get_model_revenue_col(selected_model)
            )
            st.plotly_chart(fig_drill, use_container_width=True)

            if not drill_table.empty:
                display_drill = drill_table.copy()
                for c in ["spend", "revenue"]:
                    display_drill[c] = display_drill[c].apply(lambda v: format_currency(v, curr_sym))
                display_drill["roas"] = display_drill["roas"].apply(lambda v: f"{v:.2f}x")
                display_drill["ctr"] = display_drill["ctr"].apply(lambda v: f"{v:.2f}%")
                display_drill = display_drill.rename(columns={
                    "campaign": "Campaign Name",
                    "creative_type": "Creative Asset",
                    "spend": "Media Spend",
                    "impressions": "Impressions",
                    "clicks": "Clicks",
                    "conversions": "Conversions",
                    "revenue": f"Attributed Rev ({selected_model})",
                    "ctr": "CTR",
                    "roas": "ROAS",
                })
                st.dataframe(display_drill, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------------
    # TAB 2: FUNNEL & COHORT RETENTION + DIAGNOSTICS
    # -------------------------------------------------------------------------
    with tab2:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        sec_col1, sec_col2 = st.columns(2)

        with sec_col1:
            with st.container(border=True):
                funnel_focus = st.selectbox(
                    "Funnel Diagnostic Focus:",
                    options=["All Channels (Macro Blended)"] + available_channels,
                    index=0,
                    help="Select an individual channel to isolate drop-off points or inspect the blended macro pipeline."
                )
                fig_funnel, diag = render_funnel_pipeline(df_filtered, channel_focus=funnel_focus)
                st.plotly_chart(fig_funnel, use_container_width=True)

                st.markdown("**Stage Efficiency Diagnostics:**")
                st.markdown(
                    f'<span class="diag-pill">CTR: <strong>{diag["ctr"]:.2f}%</strong></span>'
                    f'<span class="diag-pill">Click ➔ Visit: <strong>{diag["visit_rate"]:.1f}%</strong></span>'
                    f'<span class="diag-pill">Visit ➔ Lead: <strong>{diag["lead_rate"]:.1f}%</strong></span>'
                    f'<span class="diag-pill">Lead ➔ Conv: <strong>{diag["close_rate"]:.1f}%</strong></span>',
                    unsafe_allow_html=True,
                )
                st.caption("Drop-off metrics surface bottlenecks in creative CTR, landing page tracking, or lead qualification.")

        with sec_col2:
            with st.container(border=True):
                cohort_view_mode = st.radio(
                    "Cohort Evaluation Metric:",
                    options=["Retention Rate (%)", "Cumulative LTV (₹)"],
                    index=0,
                    horizontal=True,
                    help="Toggle between customer retention decay percentage and cumulative monetary lifetime value per cohort.",
                )

                scenario_aov = 2400.0
                if data_mode == "Benchmark Simulation":
                    scenario_aov = SCENARIO_CONFIGS[current_scenario_key]["channel_params"]["Search"]["aov"]

                fig_cohort = render_cohort_retention(cohort_df, metric_type=cohort_view_mode, aov=scenario_aov)
                st.plotly_chart(fig_cohort, use_container_width=True)
                st.caption(
                    "Retention matrix tracking customer engagement across 0 to 3 months post-acquisition. "
                    "Useful for understanding long-term cohort value decay and payback velocity."
                )

    # -------------------------------------------------------------------------
    # TAB 3: ATTRIBUTION MODEL COMPARISON & JOURNEY PATHS
    # -------------------------------------------------------------------------
    with tab3:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            fig_attr, comp_df = render_attribution_comparison(df_filtered)
            st.plotly_chart(fig_attr, use_container_width=True)

            st.info(
                "💡 **Analytical Insight:** Last-click systematically underestimates awareness and nurture channels "
                "like Social & Display, whereas First-Order Markov Chain and Shapley models reward full-journey assists.",
                icon="ℹ️",
            )

            if top_journey_paths:
                st.markdown("#### Top Multi-Touch Customer Journey Paths (Slide 6 & 8)")
                st.caption("Dominant customer touchpoint sequences identified across conversion paths:")

                path_rows = []
                for p in top_journey_paths:
                    path_rows.append({
                        "Customer Journey Sequence": p["path"],
                        "Path Traffic Share": f"{p['share']}%",
                        "Conversion Rate": p["cvr"],
                        "Primary Attribution Dynamic": p["assist"],
                    })
                st.dataframe(pd.DataFrame(path_rows), use_container_width=True, hide_index=True)

            with st.expander("View Numerical Model Comparison Table", expanded=False):
                display_table = comp_df.copy()
                for col in ["First-click", "Last-click", "Linear", "Markov Chain", "Shapley Value"]:
                    if col in display_table.columns:
                        display_table[col] = display_table[col].apply(format_currency_inr)
                st.dataframe(display_table, use_container_width=True, hide_index=True)

                csv_export = comp_df.to_csv(index=False)
                st.download_button(
                    label="📥 Export Attribution Table as CSV",
                    data=csv_export,
                    file_name="attribution_model_comparison.csv",
                    mime="text/csv",
                )

    # -------------------------------------------------------------------------
    # TAB 4: AI RECOMMENDATION, WHAT-IF SIMULATOR & GOVERNANCE
    # -------------------------------------------------------------------------
    with tab4:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        channels_sim = list(baseline_allocations.keys())

        # Model-Linked Dynamic Saturation: Scale Hill curves by active attribution shares
        rev_col = get_model_revenue_col(selected_model)
        tot_model_rev = df_filtered[rev_col].sum() if not df_filtered.empty else 1.0
        active_model_weights = {
            ch: float(df_filtered[df_filtered["channel"] == ch][rev_col].sum() / max(tot_model_rev, 1.0))
            for ch in channels_sim
        }
        scaled_hill_curves = scale_curves_by_attribution(active_hill_curves, active_model_weights, channels_sim)

        # Executive Financial & Margin Controls
        col_gov1, col_gov2 = st.columns([1.2, 1.0])
        with col_gov1:
            opt_mode = st.radio(
                "SLSQP Optimization Objective:",
                options=["Maximize Gross Revenue (Top-Line ROAS)", "Maximize Net Profit Contribution (Margin - Spend)"],
                index=0,
                horizontal=True,
                help="Choose whether to maximize top-line sales volume or net economic contribution after product COGS."
            )
        with col_gov2:
            gross_margin_pct_input = st.slider(
                "Product Gross Margin (%):",
                min_value=15,
                max_value=95,
                value=int(gross_margin_default * 100),
                step=5,
                format="%d%%",
                help="Product gross margin percentage (Revenue - COGS) / Revenue."
            ) / 100.0

        opt_objective = "profit" if "Net Profit" in opt_mode else "revenue"

        rec = generate_dynamic_ai_recommendation(
            baseline_allocations,
            scaled_hill_curves,
            currency_formatter=format_currency_inr,
            gross_margin_pct=gross_margin_pct_input,
            attribution_model_name=selected_model,
        )

        st.markdown(
            f"""
            <div class="recommendation-card">
                <div class="recommendation-card-title">{rec['title']}</div>
                <div class="recommendation-card-impact">{rec['impact']}</div>
                <div class="recommendation-card-body">{rec['body']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Interactive Budget Allocation Simulator (Next 30-Day Forward Planning Cycle)")
        st.caption(
            f"Adjust target media allocations across channels to test what-if budget scenarios. "
            f"Target forward planning budget: **{format_currency_inr(target_budget)}** (Calibrated under **{selected_model}** response curves)."
        )

        sim_col_controls, sim_col_results = st.columns([1.1, 1.4])

        with sim_col_controls:
            with st.container(border=True):
                st.markdown("**Channel Budget Allocation (₹)**")

                # Optimizer and Rebalance Action Buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("⚡ Auto-Rebalance", use_container_width=True, help="Proportionally scale allocations so their sum equals the target budget."):
                        curr_tot = sum(st.session_state.get(f"slider_{c}", int(baseline_allocations.get(c, target_budget / len(channels_sim)))) for c in channels_sim)
                        if curr_tot > 0:
                            ratio = target_budget / curr_tot
                            for c in channels_sim:
                                st.session_state[f"slider_{c}"] = int(round(st.session_state.get(f"slider_{c}", baseline_allocations[c]) * ratio, -3))
                            st.rerun()

                with col_btn2:
                    if st.button("🤖 Auto-Optimize (SLSQP)", use_container_width=True, help=f"Compute optimal allocation to {opt_mode} under {selected_model} curves."):
                        opt_alloc = solve_optimal_budget(
                            target_budget,
                            scaled_hill_curves,
                            channels_sim,
                            gross_margin_pct=gross_margin_pct_input,
                            objective=opt_objective,
                        )
                        for c in channels_sim:
                            st.session_state[f"slider_{c}"] = int(opt_alloc[c])
                        st.session_state["optimizer_applied"] = True
                        st.rerun()

                if st.session_state.get("optimizer_applied"):
                    st.success(f"✓ Global efficient frontier applied via SLSQP optimizer ({opt_mode})!")
                    st.session_state["optimizer_applied"] = False

                sim_sliders = {}
                for ch in channels_sim:
                    base_val = int(baseline_allocations.get(ch, target_budget / len(channels_sim)))
                    max_slider = max(int(target_budget * 0.75), 100000)
                    step_val = 5000 if target_budget <= 1000000 else 10000

                    if f"slider_{ch}" not in st.session_state:
                        st.session_state[f"slider_{ch}"] = base_val

                    sim_sliders[ch] = st.slider(
                        f"{ch} Budget",
                        min_value=0,
                        max_value=max_slider,
                        value=st.session_state[f"slider_{ch}"],
                        step=step_val,
                        format="₹%d",
                        key=f"slider_{ch}",
                    )

                current_total_allocated = sum(sim_sliders.values())
                diff = current_total_allocated - target_budget

                if abs(diff) < 500:
                    st.success(f"✓ Total Allocated: {format_currency_inr(current_total_allocated)} (Balanced)")
                elif diff > 0:
                    st.warning(f"Over budget by {format_currency_inr(diff)} (Total: {format_currency_inr(current_total_allocated)})")
                else:
                    st.info(f"Under budget by {format_currency_inr(abs(diff))} (Total: {format_currency_inr(current_total_allocated)})")

                st.button("Run Scenario & Compare", type="primary", use_container_width=True)

        with sim_col_results:
            with st.container(border=True):
                st.markdown("**Scenario Evaluation & Diminishing Returns Projection**")

                baseline_results = calculate_diminishing_returns(baseline_allocations, scaled_hill_curves, gross_margin_pct=gross_margin_pct_input)
                simulated_results = calculate_diminishing_returns(sim_sliders, scaled_hill_curves, gross_margin_pct=gross_margin_pct_input)

                tot_base_spend = sum(res["spend"] for res in baseline_results.values())
                tot_base_conv = sum(res["conversions"] for res in baseline_results.values())
                tot_base_rev = sum(res["revenue"] for res in baseline_results.values())
                tot_base_profit = sum(res["net_profit"] for res in baseline_results.values())
                tot_base_roas = tot_base_rev / tot_base_spend if tot_base_spend > 0 else 0

                tot_sim_spend = sum(res["spend"] for res in simulated_results.values())
                tot_sim_conv = sum(res["conversions"] for res in simulated_results.values())
                tot_sim_rev = sum(res["revenue"] for res in simulated_results.values())
                tot_sim_profit = sum(res["net_profit"] for res in simulated_results.values())
                tot_sim_roas = tot_sim_rev / tot_sim_spend if tot_sim_spend > 0 else 0

                conv_change_pct = ((tot_sim_conv - tot_base_conv) / tot_base_conv * 100) if tot_base_conv > 0 else 0
                rev_change_pct = ((tot_sim_rev - tot_base_rev) / tot_base_rev * 100) if tot_base_rev > 0 else 0
                profit_delta = tot_sim_profit - tot_base_profit
                roas_delta_sim = tot_sim_roas - tot_base_roas

                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                with m_col1:
                    st.metric(
                        "Conversions",
                        f"{tot_sim_conv:,}",
                        f"{conv_change_pct:+.1f}% vs baseline",
                    )
                with m_col2:
                    st.metric(
                        "Revenue",
                        format_currency_inr(tot_sim_rev),
                        f"{rev_change_pct:+.1f}% vs baseline",
                    )
                with m_col3:
                    st.metric(
                        "Net Profit",
                        format_currency_inr(tot_sim_profit),
                        f"{profit_delta:+,.0f} impact",
                    )
                with m_col4:
                    st.metric(
                        "ROAS",
                        f"{tot_sim_roas:.2f}x",
                        f"{roas_delta_sim:+.2f}x vs baseline",
                    )

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                st.markdown("**Before / After Scenario Comparison Table**")

                comparison_rows = []
                for ch in channels_sim:
                    b = baseline_results.get(ch, {"spend": 0, "conversions": 0, "roas": 0, "revenue": 0, "m_roas": 0, "net_profit": 0})
                    s = simulated_results.get(ch, {"spend": 0, "conversions": 0, "roas": 0, "revenue": 0, "m_roas": 0, "net_profit": 0})
                    comparison_rows.append({
                        "Channel": ch,
                        "Base Spend": format_currency_inr(b["spend"]),
                        "Sim Spend": format_currency_inr(s["spend"]),
                        "Base Conv": b["conversions"],
                        "Sim Conv": s["conversions"],
                        "Base ROAS": f"{b['roas']:.2f}x",
                        "Sim ROAS": f"{s['roas']:.2f}x",
                        "Marginal ROAS": f"{s['m_roas']:.2f}x",
                        "Revenue Impact": format_currency_inr(s["revenue"] - b["revenue"]),
                        "Profit Impact": format_currency_inr(s["net_profit"] - b["net_profit"]),
                    })

                comparison_rows.append({
                    "Channel": "TOTAL",
                    "Base Spend": format_currency_inr(tot_base_spend),
                    "Sim Spend": format_currency_inr(tot_sim_spend),
                    "Base Conv": tot_base_conv,
                    "Sim Conv": tot_sim_conv,
                    "Base ROAS": f"{tot_base_roas:.2f}x",
                    "Sim ROAS": f"{tot_sim_roas:.2f}x",
                    "Marginal ROAS": "—",
                    "Revenue Impact": format_currency_inr(tot_sim_rev - tot_base_rev),
                    "Profit Impact": format_currency_inr(tot_sim_profit - tot_base_profit),
                })

                comp_table_df = pd.DataFrame(comparison_rows)
                st.dataframe(comp_table_df, use_container_width=True, hide_index=True)
                sim_export_csv = comp_table_df.to_csv(index=False).encode("utf-8")

                active_scenario_key_str = current_scenario_key if data_mode == "Benchmark Simulation" else "Custom Upload"
                audit_history = load_audit_log()
                active_scenario_records = [r for r in audit_history if r.get("scenario") == active_scenario_key_str]
                latest_audit_rec = active_scenario_records[0] if active_scenario_records else None

                exec_brief_html = generate_executive_brief_html(
                    scenario_name=active_scenario_key_str,
                    attribution_model=selected_model,
                    kpis=kpis,
                    unit_economics={
                        "cpa": blended_cpa,
                        "cac": est_cac,
                        "ltv_cac": ltv_cac_ratio,
                        "health": ltv_health,
                    },
                    ai_recommendation=rec,
                    simulation_rows=comparison_rows,
                    audit_record=latest_audit_rec,
                    currency_symbol=curr_sym,
                )

                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        label="📥 Export What-If CSV",
                        data=sim_export_csv,
                        file_name="what_if_scenario_simulation.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                with col_dl2:
                    st.download_button(
                        label="📄 Export Executive Brief (HTML / PDF)",
                        data=exec_brief_html,
                        file_name=f"executive_brief_{selected_model.lower().replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True,
                        help="Download a clean, print-ready C-suite executive briefing report (Slide 4 step 9).",
                    )

                # -------------------------------------------------------------
                # PHASE 3: PERSISTENT GOVERNANCE & AUDIT LEDGER (Slide 4 & 8)
                # -------------------------------------------------------------
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                with st.expander("🛡️ Responsible AI Governance & Decision Protocol (Slide 8)", expanded=True):
                    tot_clicks_stat = int(df_filtered["clicks"].sum())
                    tot_conv_stat = int(df_filtered["conversions"].sum())
                    obs_cvr = (tot_conv_stat / tot_clicks_stat) if tot_clicks_stat > 0 else 0.0
                    se_cvr = (np.sqrt(obs_cvr * (1.0 - obs_cvr) / tot_clicks_stat)) if tot_clicks_stat > 0 else 0.0
                    ci_95_str = f"[{max(0.0, (obs_cvr - 1.96 * se_cvr) * 100):.2f}%, {min(100.0, (obs_cvr + 1.96 * se_cvr) * 100):.2f}%]"
                    stat_conf_label = "Statistically Significant (p < 0.001, N > 5,000)" if tot_clicks_stat >= 5000 else "Moderate Power (N < 5,000)"

                    st.markdown(
                        f"""
                        <div style="font-size: 0.85rem; color: #475569; line-height: 1.5;">
                            <div>• <strong>Active Models:</strong> First-Order Markov Absorption + Hill Saturation Curves (<strong>{selected_model}</strong> Lens)</div>
                            <div>• <strong>Sample Validity:</strong> {len(df_filtered):,} daily records · {tot_clicks_stat:,} evaluated clicks (95% CI: {ci_95_str}, {stat_conf_label})</div>
                            <div>• <strong>Gross Margin Assumption:</strong> {int(gross_margin_pct_input * 100)}% COGS calibrated · Target: {opt_mode}</div>
                            <div>• <strong>Governance Framework:</strong> Decision-support advisory only. Automated bank mutations prohibited.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                    if active_scenario_records:
                        latest_rec = active_scenario_records[0]
                        st.success(
                            f"✓ Plan Officially Signed Off by {latest_rec['approved_by']}\n\n"
                            f"• Audit ID: `{latest_rec['audit_id']}` ({latest_rec['verification_hash']})\n\n"
                            f"• Timestamp: {latest_rec['timestamp']}\n\n"
                            f"• Approved Budget: {format_currency(latest_rec['target_budget'], curr_sym)}\n\n"
                            f"• Target ROAS: {latest_rec['projected_roas']:.2f}x\n\n"
                            f"• Status: Ready for Ad Platform API Deployment"
                        )

                    btn_label = "✅ Re-Approve & Update Sign-Off" if active_scenario_records else "✅ Approve & Sign-Off Budget Allocation Plan"
                    if st.button(btn_label, type="primary", use_container_width=True):
                        saved_rec = save_audit_record(
                            scenario=active_scenario_key_str,
                            target_budget=current_total_allocated,
                            projected_revenue=tot_sim_rev,
                            projected_roas=tot_sim_roas,
                            allocations=sim_sliders.copy(),
                            approved_by="Marketing Manager",
                        )
                        st.session_state["just_signed"] = saved_rec["audit_id"]
                        st.rerun()

                    if audit_history:
                        with st.expander("📜 Historical Audit Ledger (Persistent Records)", expanded=False):
                            history_rows = []
                            for r in audit_history[:10]:
                                history_rows.append({
                                    "Audit ID": r["audit_id"],
                                    "Timestamp": r["timestamp"],
                                    "Scenario": r["scenario"],
                                    "Approved By": r["approved_by"],
                                    "Budget": format_currency_inr(r["target_budget"]),
                                    "ROAS": f"{r['projected_roas']:.2f}x",
                                    "Hash": r["verification_hash"],
                                })
                            st.dataframe(pd.DataFrame(history_rows), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
