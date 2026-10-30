"""
Interactive Plotly Visualization Modules.
Executive Light BI Theme with zero element collisions.
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.config import COLOR_PRIMARY


def get_model_revenue_col(model_name: str) -> str:
    """Map UI attribution model name to dataframe column."""
    mapping = {
        "First-click": "revenue_first_click",
        "Last-click": "revenue_last_click",
        "Linear": "revenue_linear",
        "Markov Chain": "revenue_markov",
        "Shapley Value": "revenue_shapley",
    }
    return mapping.get(model_name, "revenue_markov")


def render_roas_by_channel(df_filtered: pd.DataFrame, attribution_model: str) -> go.Figure:
    """Horizontal bar chart showing ROAS by channel with clean teal palette."""
    rev_col = get_model_revenue_col(attribution_model)

    grouped = (
        df_filtered.groupby("channel")[["spend", rev_col]]
        .sum()
        .reset_index()
    )
    grouped["roas"] = np.where(grouped["spend"] > 0, grouped[rev_col] / grouped["spend"], 0.0)
    grouped = grouped.sort_values(by="roas", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=grouped["roas"],
            y=grouped["channel"],
            orientation="h",
            marker=dict(
                color="#0D9488",
                line=dict(color="#0F766E", width=1),
            ),
            text=[f"{val:.2f}x" for val in grouped["roas"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>ROAS: %{x:.2f}x<extra></extra>",
        )
    )

    max_val = max(grouped["roas"].max() * 1.25, 3.5) if not grouped.empty else 4.0
    fig.update_layout(
        title=dict(
            text=f"ROAS by Channel ({attribution_model})",
            font=dict(size=14, color=COLOR_PRIMARY),
            x=0.0,
            y=0.98,
        ),
        margin=dict(l=20, r=45, t=55, b=30),
        height=320,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(
            title="Return on Ad Spend (ROAS)",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
            range=[0, max_val],
        ),
        yaxis=dict(title="", showgrid=False),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_spend_vs_revenue(df_filtered: pd.DataFrame, attribution_model: str) -> go.Figure:
    """Monthly trend comparing Spend against Attributed Revenue with separated legend."""
    rev_col = get_model_revenue_col(attribution_model)

    temp = df_filtered.copy()
    temp["month"] = temp["date"].dt.to_period("M").dt.to_timestamp()
    monthly = temp.groupby("month")[["spend", rev_col]].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly[rev_col],
            mode="lines+markers",
            name="Attributed Revenue",
            line=dict(color="#0D9488", width=2.5),
            marker=dict(size=6, color="#0D9488"),
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["spend"],
            mode="lines+markers",
            name="Media Spend",
            line=dict(color="#94A3B8", width=2, dash="dot"),
            marker=dict(size=5, color="#94A3B8"),
            hovertemplate="<b>%{x|%b %Y}</b><br>Spend: ₹%{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="Spend vs Attributed Revenue (Monthly)",
            font=dict(size=14, color=COLOR_PRIMARY),
            x=0.0,
            y=0.98,
        ),
        margin=dict(l=20, r=20, t=55, b=30),
        height=320,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1.0,
            font=dict(size=11),
        ),
        xaxis=dict(showgrid=False, tickformat="%b %y", dtick="M1"),
        yaxis=dict(
            title="Amount (₹)",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
        ),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_funnel_pipeline(
    df_filtered: pd.DataFrame,
    channel_focus: Optional[str] = None
) -> Tuple[go.Figure, Dict[str, float]]:
    """
    Renders macro conversion pipeline or channel-isolated funnel using relative progression scaling
    to prevent needle compression between millions of impressions and thousands of conversions.
    """
    df_target = df_filtered
    if channel_focus and channel_focus != "All Channels (Macro Blended)":
        df_target = df_filtered[df_filtered["channel"] == channel_focus]

    tot_imp = int(df_target["impressions"].sum()) if not df_target.empty else 0
    tot_clicks = int(df_target["clicks"].sum()) if not df_target.empty else 0
    tot_visits = int(df_target["visits"].sum()) if not df_target.empty else 0
    tot_leads = int(df_target["leads"].sum()) if not df_target.empty else 0
    tot_conv = int(df_target["conversions"].sum()) if not df_target.empty else 0

    stages = ["Impressions", "Clicks", "Visits", "Leads", "Conversions"]
    values = [tot_imp, tot_clicks, tot_visits, tot_leads, tot_conv]

    # Calculate step transition ratios
    pct_prev = [100.0]
    for i in range(1, len(values)):
        ratio = (values[i] / values[i - 1] * 100) if values[i - 1] > 0 else 0
        pct_prev.append(ratio)

    # Scale stages on a visually balanced power-root scale
    display_widths = [100.0, 78.0, 62.0, 46.0, 32.0]

    fig = go.Figure()
    funnel_colors = ["#0284C7", "#0EA5E9", "#14B8A6", "#0D9488", "#059669"]

    for i, stage in enumerate(stages):
        val_str = f"{values[i]:,}"
        ratio_str = f"{pct_prev[i]:.1f}% of prev" if i > 0 else "Top of Funnel"
        fig.add_trace(
            go.Bar(
                name=stage,
                y=[stage],
                x=[display_widths[i]],
                orientation="h",
                marker=dict(color=funnel_colors[i]),
                text=f"<b>{val_str}</b> ({ratio_str})",
                textposition="inside",
                insidetextanchor="middle",
                hoverinfo="none",
                showlegend=False,
            )
        )

    title_suffix = f" — {channel_focus}" if channel_focus and channel_focus != "All Channels (Macro Blended)" else " (Balanced Stage Representation)"
    fig.update_layout(
        title=dict(
            text=f"Conversion Pipeline{title_suffix}",
            font=dict(size=14, color=COLOR_PRIMARY),
            x=0.0,
            y=0.98,
        ),
        margin=dict(l=20, r=20, t=55, b=25),
        height=375,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 105]),
        yaxis=dict(title="", showgrid=False, autorange="reversed"),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )

    diagnostics = {
        "ctr": (tot_clicks / tot_imp * 100) if tot_imp > 0 else 0,
        "visit_rate": (tot_visits / tot_clicks * 100) if tot_clicks > 0 else 0,
        "lead_rate": (tot_leads / tot_visits * 100) if tot_visits > 0 else 0,
        "close_rate": (tot_conv / tot_leads * 100) if tot_leads > 0 else 0,
    }

    return fig, diagnostics


def render_cohort_retention(
    cohort_df: pd.DataFrame,
    metric_type: str = "Retention Rate (%)",
    aov: float = 2400.0
) -> go.Figure:
    """Cohort heatmap supporting both Retention Rate (%) and Cumulative LTV (₹)."""
    raw_values = cohort_df.values
    z_values = []
    text_values = []

    ltv_multipliers = [1.0, 1.45, 1.82, 2.15]

    for row in raw_values:
        row_z = []
        row_text = []
        for col_idx, val in enumerate(row):
            if pd.isna(val) or val is None:
                row_z.append(None)
                row_text.append("—")
            else:
                if metric_type == "Cumulative LTV (₹)":
                    ltv_val = aov * ltv_multipliers[col_idx] * (val / 100.0 if col_idx > 0 else 1.0)
                    row_z.append(ltv_val)
                    row_text.append(f"₹{ltv_val:,.0f}")
                else:
                    row_z.append(val)
                    row_text.append(f"{val:.1f}%")
        z_values.append(row_z)
        text_values.append(row_text)

    z_clean = np.array(z_values, dtype=float)

    fig = go.Figure(
        data=go.Heatmap(
            z=z_clean,
            x=cohort_df.columns.tolist(),
            y=cohort_df.index.tolist(),
            text=text_values,
            texttemplate="%{text}",
            textfont=dict(size=11, color="#0F172A"),
            colorscale=[
                [0.0, "#F8FAFC"],
                [0.25, "#E6FFFA"],
                [0.6, "#99F6E4"],
                [1.0, "#2DD4BF"],
            ],
            showscale=False,
            hoverongaps=False,
            hovertemplate="Cohort: %{y}<br>%{x}: %{text}<extra></extra>",
        )
    )

    title_text = "User Retention by Signup Cohort" if metric_type == "Retention Rate (%)" else "Estimated Cohort Cumulative LTV (₹)"
    fig.update_layout(
        title=dict(
            text=f"{title_text} <span style='font-size:11px;color:#64748B;'>[0–3 Months]</span>",
            font=dict(size=14, color=COLOR_PRIMARY),
            x=0.0,
            y=0.98,
        ),
        margin=dict(l=20, r=20, t=55, b=25),
        height=375,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(title="", tickfont=dict(size=11)),
        yaxis=dict(title="", tickfont=dict(size=11), autorange="reversed"),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_attribution_comparison(df_filtered: pd.DataFrame) -> Tuple[go.Figure, pd.DataFrame]:
    """Compare attributed revenue across all 5 models with zero collision."""
    models_to_compare = [
        ("First-click", "revenue_first_click"),
        ("Last-click", "revenue_last_click"),
        ("Linear", "revenue_linear"),
        ("Markov Chain", "revenue_markov"),
        ("Shapley Value", "revenue_shapley"),
    ]

    summary = []
    channels = sorted(df_filtered["channel"].unique().tolist())

    for ch in channels:
        row = {"Channel": ch}
        ch_df = df_filtered[df_filtered["channel"] == ch]
        for model_label, col in models_to_compare:
            row[model_label] = ch_df[col].sum() if not ch_df.empty else 0.0
        summary.append(row)

    comp_df = pd.DataFrame(summary)

    fig = go.Figure()
    light_palette = ["#38BDF8", "#34D399", "#FBBF24", "#0D9488", "#A78BFA"]

    for i, (model_label, _) in enumerate(models_to_compare):
        fig.add_trace(
            go.Bar(
                name=model_label,
                x=comp_df["Channel"],
                y=comp_df[model_label],
                marker=dict(color=light_palette[i % len(light_palette)]),
                hovertemplate="<b>%{x}</b> (" + model_label + "): ₹%{y:,.0f}<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="group",
        title=dict(
            text="Attributed Revenue Comparison (Conserved Across Models)",
            font=dict(size=14, color=COLOR_PRIMARY),
            x=0.0,
            y=0.98,
        ),
        margin=dict(l=20, r=20, t=55, b=25),
        height=350,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1.0,
            font=dict(size=11),
        ),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(
            title="Attributed Revenue (₹)",
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=False,
        ),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )

    return fig, comp_df


def render_campaign_drilldown(
    df_channel: pd.DataFrame,
    channel_name: str,
    revenue_col: str = "revenue_markov",
) -> Tuple[go.Figure, pd.DataFrame]:
    """
    Renders drill-down analysis comparing campaigns and creative assets within an individual channel (Slide 4 step 5 & Slide 6).
    """
    if df_channel.empty:
        return go.Figure(), pd.DataFrame()

    df_c = df_channel.copy()
    if "campaign" not in df_c.columns:
        df_c["campaign"] = channel_name + " - Main Campaign"
    if "creative_type" not in df_c.columns:
        df_c["creative_type"] = "Standard Ad"

    rev_target_col = revenue_col if revenue_col in df_c.columns else "revenue"

    grouped = df_c.groupby(["campaign", "creative_type"]).agg(
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        revenue=(rev_target_col, "sum"),
    ).reset_index()

    grouped["ctr"] = np.where(grouped["impressions"] > 0, (grouped["clicks"] / grouped["impressions"]) * 100, 0.0)
    grouped["roas"] = np.where(grouped["spend"] > 0, grouped["revenue"] / grouped["spend"], 0.0)
    grouped = grouped.sort_values(by="revenue", ascending=False)

    camp_summary = df_c.groupby("campaign").agg(
        spend=("spend", "sum"),
        revenue=(rev_target_col, "sum"),
    ).reset_index().sort_values(by="revenue", ascending=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Media Spend",
            y=camp_summary["campaign"],
            x=camp_summary["spend"],
            orientation="h",
            marker=dict(color="#94A3B8"),
            hovertemplate="<b>%{y}</b><br>Spend: %{x:,.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Attributed Revenue",
            y=camp_summary["campaign"],
            x=camp_summary["revenue"],
            orientation="h",
            marker=dict(color="#0D9488"),
            hovertemplate="<b>%{y}</b><br>Revenue: %{x:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        title=dict(
            text=f"Campaign Spend vs Revenue Drill-Down — {channel_name}",
            font=dict(size=14, color=COLOR_PRIMARY),
            x=0.0,
            y=0.98,
        ),
        margin=dict(l=20, r=20, t=55, b=25),
        height=280,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1.0, font=dict(size=11)),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="", showgrid=False),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )

    return fig, grouped


def generate_executive_brief_html(
    scenario_name: str,
    attribution_model: str,
    kpis: Dict[str, float],
    unit_economics: Dict[str, Any],
    ai_recommendation: Dict[str, Any],
    simulation_rows: List[Dict[str, Any]],
    audit_record: Optional[Dict[str, Any]] = None,
    currency_symbol: str = "₹",
) -> str:
    """Generate a clean, standalone, print-ready HTML executive briefing document (Slide 4 step 9 & Phase 3.3)."""
    sign_off_badge = ""
    if audit_record:
        sign_off_badge = f"""
        <div style="background: #ECFDF5; border: 1px solid #10B981; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px;">
            <strong style="color: #065F46;">✓ Plan Approved & Signed Off</strong><br>
            <span style="font-size: 13px; color: #047857;">
                Approved by: {audit_record.get('approved_by', 'Marketing Manager')} &nbsp;|&nbsp;
                Audit ID: <code>{audit_record.get('audit_id', 'N/A')}</code> &nbsp;|&nbsp;
                Hash: <code>{audit_record.get('verification_hash', 'N/A')[:24]}...</code> &nbsp;|&nbsp;
                Timestamp: {audit_record.get('timestamp', 'N/A')}
            </span>
        </div>
        """
    else:
        sign_off_badge = """
        <div style="background: #FFFBEB; border: 1px solid #F59E0B; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px;">
            <strong style="color: #92400E;">⚠️ Plan Status: Pending Managerial Review</strong><br>
            <span style="font-size: 13px; color: #B45309;">Draft simulation proposal prepared for executive review and sign-off.</span>
        </div>
        """

    # Table rows
    table_trs = ""
    for r in simulation_rows:
        is_tot = r.get("Channel") == "TOTAL"
        bold_st = "font-weight: 700; background: #F8FAFC;" if is_tot else ""
        table_trs += f"""
        <tr style="{bold_st}">
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0;">{r.get('Channel', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right;">{r.get('Base Spend', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right;">{r.get('Sim Spend', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right;">{r.get('Sim Conv', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right;">{r.get('Sim ROAS', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right;">{r.get('Marginal ROAS', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right; color: #0D9488; font-weight: 600;">{r.get('Revenue Impact', '')}</td>
            <td style="padding: 8px 12px; border-bottom: 1px solid #E2E8F0; text-align: right; font-weight: 600;">{r.get('Profit Impact', '')}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Executive Brief: Marketing Campaign Effectiveness Decision-Support System</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0F172A; margin: 30px; line-height: 1.5; }}
    h1 {{ font-size: 22px; color: #0F172A; margin: 0 0 4px 0; }}
    .subtitle {{ color: #64748B; font-size: 13px; margin-bottom: 24px; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }}
    .kpi-card {{ border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; background: #FFFFFF; }}
    .kpi-label {{ font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 600; }}
    .kpi-val {{ font-size: 20px; font-weight: 700; color: #0F172A; margin-top: 4px; }}
    .kpi-sub {{ font-size: 11px; color: #0D9488; margin-top: 2px; }}
    .rec-box {{ background: #F0FDF4; border-left: 4px solid #10B981; padding: 14px 18px; border-radius: 4px; margin-bottom: 24px; }}
    .rec-title {{ font-size: 15px; font-weight: 700; color: #065F46; }}
    .rec-impact {{ font-size: 13px; color: #047857; margin: 4px 0 8px 0; font-weight: 600; }}
    .rec-body {{ font-size: 12px; color: #334155; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 12px; }}
    th {{ background: #F1F5F9; color: #334155; font-weight: 600; text-align: left; padding: 10px 12px; border-bottom: 1px solid #CBD5E1; }}
    @media print {{ body {{ margin: 0; }} .no-print {{ display: none; }} }}
</style>
</head>
<body>
    <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0F172A; padding-bottom: 12px; margin-bottom: 16px;">
        <div>
            <h1>Marketing Campaign Effectiveness Analysis</h1>
            <div class="subtitle">Executive Decision-Support Brief & Capital Reallocation Plan · Scenario: <strong>{scenario_name}</strong></div>
        </div>
        <div style="text-align: right; font-size: 12px; color: #64748B;">
            Lens: <strong>{attribution_model} MTA</strong><br>
            Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
        </div>
    </div>

    {sign_off_badge}

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Media Spend (Evaluated)</div>
            <div class="kpi-val">{currency_symbol}{kpis.get('spend', 0):,.0f}</div>
            <div class="kpi-sub">Total Media Outlay</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Attributed Revenue</div>
            <div class="kpi-val">{currency_symbol}{kpis.get('revenue', 0):,.0f}</div>
            <div class="kpi-sub">{attribution_model} Model</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">ROAS / Blended CPA</div>
            <div class="kpi-val">{kpis.get('roas', 0):.2f}x</div>
            <div class="kpi-sub">CPA: {currency_symbol}{unit_economics.get('cpa', 0):,.0f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">CAC / LTV:CAC Ratio</div>
            <div class="kpi-val">{unit_economics.get('ltv_cac', 0):.1f}x</div>
            <div class="kpi-sub">CAC: {currency_symbol}{unit_economics.get('cac', 0):,.0f} · {unit_economics.get('health', 'Healthy')}</div>
        </div>
    </div>

    <div class="rec-box">
        <div class="rec-title">{ai_recommendation.get('title', '')}</div>
        <div class="rec-impact">{ai_recommendation.get('impact', '')}</div>
        <div class="rec-body">{ai_recommendation.get('body', '')}</div>
    </div>

    <h2 style="font-size: 15px; margin: 20px 0 8px 0; color: #0F172A;">Forward 30-Day Budget Allocation & What-If Projection</h2>
    <table>
        <thead>
            <tr>
                <th>Channel</th>
                <th style="text-align: right;">Base Spend</th>
                <th style="text-align: right;">Target Spend</th>
                <th style="text-align: right;">Conversions</th>
                <th style="text-align: right;">ROAS</th>
                <th style="text-align: right;">Marginal ROAS</th>
                <th style="text-align: right;">Revenue Impact</th>
                <th style="text-align: right;">Net Profit Impact</th>
            </tr>
        </thead>
        <tbody>
            {table_trs}
        </tbody>
    </table>

    <div style="margin-top: 30px; padding-top: 12px; border-top: 1px solid #E2E8F0; font-size: 11px; color: #64748B; display: flex; justify-content: space-between;">
        <div>Marketing Campaign Effectiveness Decision-Support System · Confidential Executive Document</div>
        <div>Governance: Automated bank mutations strictly prohibited · Human Sign-off Required</div>
    </div>
</body>
</html>
"""
    return html
