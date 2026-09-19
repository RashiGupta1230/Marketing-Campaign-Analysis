"""
Marketing Campaign Effectiveness Analysis — Interactive ROI Decision-Support System
Prototype for College Research Project
Author: Analytics Research Team
Data: Deterministic Synthetic Benchmark (Sample Data, Seed=42)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. APPLICATION CONFIGURATION & DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Marketing Campaign Effectiveness Analysis — Interactive ROI Decision-Support System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional, calm, desaturated color palette
COLOR_PRIMARY = "#2C3E50"      # Desaturated navy / slate blue for headers/primary
COLOR_SECONDARY = "#4C9A8C"    # Muted teal for AI recommendation / positive accents
COLOR_MUTED_GREY = "#7F8C8D"   # Soft neutral grey
COLOR_LIGHT_GREY = "#F8FAFC"   # Subtle card background
COLOR_BORDER = "#E2E8F0"       # Subtle border line
COLOR_TEXT = "#1E293B"         # Slate dark text


def apply_custom_styles():
    """Apply muted, distraction-free styling aligned with professional internal BI tools."""
    st.markdown(
        f"""
        <style>
            /* Base layout & typography */
            .main .block-container {{
                padding-top: 1.8rem;
                padding-bottom: 3.5rem;
                max-width: 1300px;
            }}
            
            /* Clean headers */
            h1, h2, h3, h4 {{
                color: {COLOR_PRIMARY};
                font-weight: 600 !important;
                letter-spacing: -0.02em;
            }}
            
            /* Subtitle & disclaimer badge */
            .app-header-title {{
                font-size: 1.65rem;
                font-weight: 700;
                color: {COLOR_PRIMARY};
                margin-bottom: 0.25rem;
            }}
            
            .app-header-subtitle {{
                font-size: 0.95rem;
                color: {COLOR_MUTED_GREY};
                margin-bottom: 1.25rem;
            }}
            
            .sample-badge {{
                display: inline-block;
                background-color: #EDF2F7;
                color: #4A5568;
                font-size: 0.72rem;
                font-weight: 600;
                padding: 2px 8px;
                border-radius: 3px;
                border: 1px solid {COLOR_BORDER};
                vertical-align: middle;
                margin-left: 8px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            
            /* Recommendation card: calm, bordered, not glowing */
            .recommendation-card {{
                background-color: #FFFFFF;
                border: 1px solid {COLOR_BORDER};
                border-left: 4px solid {COLOR_SECONDARY};
                border-radius: 4px;
                padding: 1rem 1.25rem;
                margin-bottom: 1.25rem;
            }}
            
            .recommendation-card-title {{
                color: {COLOR_PRIMARY};
                font-size: 1.05rem;
                font-weight: 600;
                margin-bottom: 0.35rem;
            }}
            
            .recommendation-card-impact {{
                color: {COLOR_SECONDARY};
                font-weight: 600;
                font-size: 0.92rem;
            }}
            
            .recommendation-card-body {{
                color: #4B5563;
                font-size: 0.88rem;
                line-height: 1.45;
                margin-top: 0.35rem;
            }}
            
            /* Subtle container metrics */
            div[data-testid="stMetricValue"] {{
                font-size: 1.65rem !important;
                font-weight: 600 !important;
                color: {COLOR_PRIMARY} !important;
            }}
            div[data-testid="stMetricLabel"] {{
                font-size: 0.85rem !important;
                color: {COLOR_MUTED_GREY} !important;
                font-weight: 500 !important;
            }}

            /* Remove distracting default elements */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 2. SYNTHETIC DATA GENERATION ENGINE (REPRODUCIBLE & MODULAR)
# ==============================================================================
@st.cache_data(show_spinner=False)
def generate_synthetic_data(seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate realistic multi-channel marketing campaign data with multi-touch
    attribution and cohort retention metrics.
    
    # TODO: Replace this function with real data pipeline/warehouse ingestion
    # (e.g. Snowflake / BigQuery / Google Ads & Meta API extraction).
    """
    np.random.seed(seed)
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    
    channels = ["Search", "Social", "Email", "Display", "Website"]
    regions = ["North", "South", "East", "West"]
    
    # Baseline spend profiles (daily typical expenditure)
    channel_spend_params = {
        "Search": {"base_spend": 1600, "std_spend": 250, "cpc": 32.0, "conv_rate": 0.045, "aov": 2400},
        "Social": {"base_spend": 1400, "std_spend": 200, "cpc": 18.0, "conv_rate": 0.024, "aov": 1900},
        "Email": {"base_spend": 550,  "std_spend": 80,  "cpc": 8.0,  "conv_rate": 0.058, "aov": 2600},
        "Display": {"base_spend": 700, "std_spend": 120, "cpc": 12.0, "conv_rate": 0.015, "aov": 1700},
        "Website": {"base_spend": 400, "std_spend": 60,  "cpc": 5.0,  "conv_rate": 0.040, "aov": 2200},
    }
    
    region_weights = {"North": 0.35, "South": 0.28, "West": 0.22, "East": 0.15}
    
    records = []
    
    for current_date in date_range:
        # Weekly seasonality: slight dip on weekends for B2B/tech, or slight boost
        weekday_factor = 1.12 if current_date.weekday() < 5 else 0.85
        
        for ch in channels:
            params = channel_spend_params[ch]
            
            for reg, reg_weight in region_weights.items():
                daily_spend = max(
                    150.0,
                    np.random.normal(params["base_spend"], params["std_spend"]) * weekday_factor * reg_weight
                )
                
                # Clicks & traffic
                cpc = max(3.0, np.random.normal(params["cpc"], params["cpc"] * 0.12))
                clicks = int(max(10, daily_spend / cpc))
                
                # Impressions derived from realistic CTR
                ctr = np.random.uniform(0.015, 0.045) if ch != "Display" else np.random.uniform(0.004, 0.009)
                impressions = int(clicks / ctr)
                
                # Funnel conversion progression
                visits = int(clicks * np.random.uniform(0.85, 0.96))
                leads = int(visits * np.random.uniform(0.12, 0.24))
                conversions = int(max(1, leads * params["conv_rate"] * np.random.uniform(0.85, 1.15)))
                
                # Base unadjusted revenue
                base_revenue = conversions * params["aov"] * np.random.uniform(0.9, 1.1)
                
                # Multi-Touch Attribution synthetic weight adjustments:
                # - First-click attributes higher weight to awareness channels (Social, Display)
                # - Last-click favors high-intent closing channels (Search, Email, Website)
                # - Linear distributes evenly with moderate variance
                # - Markov Chain accounts for removal effect and assist value
                # - Shapley Value balances marginal cooperative contributions
                if ch in ["Social", "Display"]:
                    rev_first = base_revenue * 1.35
                    rev_last = base_revenue * 0.72
                    rev_linear = base_revenue * 1.05
                    rev_markov = base_revenue * 1.18
                    rev_shapley = base_revenue * 1.14
                elif ch in ["Search", "Email"]:
                    rev_first = base_revenue * 0.78
                    rev_last = base_revenue * 1.32
                    rev_linear = base_revenue * 0.98
                    rev_markov = base_revenue * 1.12
                    rev_shapley = base_revenue * 1.08
                else:  # Website
                    rev_first = base_revenue * 0.88
                    rev_last = base_revenue * 1.15
                    rev_linear = base_revenue * 1.00
                    rev_markov = base_revenue * 1.04
                    rev_shapley = base_revenue * 1.02
                
                records.append({
                    "date": current_date,
                    "channel": ch,
                    "region": reg,
                    "spend": round(daily_spend, 2),
                    "impressions": impressions,
                    "clicks": clicks,
                    "visits": visits,
                    "leads": leads,
                    "conversions": conversions,
                    "revenue_first_click": round(rev_first, 2),
                    "revenue_last_click": round(rev_last, 2),
                    "revenue_linear": round(rev_linear, 2),
                    "revenue_markov": round(rev_markov, 2),
                    "revenue_shapley": round(rev_shapley, 2),
                })
                
    df = pd.DataFrame(records)
    
    # Generate Synthetic Cohort Retention Data (6 monthly cohorts, Month 0 to Month 3)
    # TODO: Replace with real user lifecycle cohort SQL query
    cohort_months = ["Month -5", "Month -4", "Month -3", "Month -2", "Month -1", "Current Month"]
    cohort_data = {
        "Cohort": cohort_months,
        "Month 0": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        "Month 1": [54.2, 52.8, 56.1, 55.4, 57.0, 58.2],
        "Month 2": [36.5, 34.9, 38.2, 37.0, 39.1, None],
        "Month 3": [26.1, 24.8, 27.4, 26.9, None, None],
    }
    cohort_df = pd.DataFrame(cohort_data).set_index("Cohort")
    
    return df, cohort_df


# ==============================================================================
# 3. FILTERING & AGGREGATION LOGIC
# ==============================================================================
def filter_dataset(
    df: pd.DataFrame,
    date_range: Tuple[datetime.date, datetime.date],
    selected_channels: List[str],
    selected_region: str,
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
    
    if selected_region != "All":
        mask = mask & (df["region"] == selected_region)
        
    filtered = df.loc[mask].copy()
    return filtered


def get_model_revenue_col(model_name: str) -> str:
    """Map UI model name to dataframe column."""
    mapping = {
        "First-click": "revenue_first_click",
        "Last-click": "revenue_last_click",
        "Linear": "revenue_linear",
        "Markov Chain": "revenue_markov",
        "Shapley Value": "revenue_shapley",
    }
    return mapping.get(model_name, "revenue_markov")


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


def format_currency_inr(val: float) -> str:
    """Format numeric values cleanly in Indian Rupee format."""
    return f"₹{val:,.0f}"


# ==============================================================================
# 4. CHART RENDERING MODULES (MUTED & PROFESSIONAL)
# ==============================================================================
def render_roas_by_channel(df_filtered: pd.DataFrame, attribution_model: str) -> go.Figure:
    """Horizontal bar chart showing ROAS by channel in descending order."""
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
                color=COLOR_PRIMARY,
                line=dict(color=COLOR_PRIMARY, width=1),
            ),
            text=[f"{val:.2f}x" for val in grouped["roas"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>ROAS: %{x:.2f}x<extra></extra>",
        )
    )
    
    fig.update_layout(
        title=dict(
            text=f"ROAS by Channel ({attribution_model}) <span style='font-size:11px;color:#7F8C8D;'>[Sample Data]</span>",
            font=dict(size=14, color=COLOR_PRIMARY),
        ),
        margin=dict(l=20, r=40, t=45, b=30),
        height=320,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(
            title="Return on Ad Spend (ROAS)",
            showgrid=True,
            gridcolor=COLOR_BORDER,
            zeroline=False,
            range=[0, max(grouped["roas"].max() * 1.25, 4.0)] if not grouped.empty else [0, 5],
        ),
        yaxis=dict(
            title="",
            showgrid=False,
        ),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_spend_vs_revenue(df_filtered: pd.DataFrame, attribution_model: str) -> go.Figure:
    """Monthly trend comparing Spend against Attributed Revenue."""
    rev_col = get_model_revenue_col(attribution_model)
    
    temp = df_filtered.copy()
    temp["month"] = temp["date"].dt.to_period("M").dt.to_timestamp()
    monthly = temp.groupby("month")[["spend", rev_col]].sum().reset_index()
    
    fig = go.Figure()
    
    # Attributed Revenue line
    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly[rev_col],
            mode="lines+markers",
            name="Attributed Revenue",
            line=dict(color=COLOR_SECONDARY, width=2.5),
            marker=dict(size=6),
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )
    )
    
    # Spend line
    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["spend"],
            mode="lines+markers",
            name="Spend",
            line=dict(color=COLOR_MUTED_GREY, width=2, dash="dot"),
            marker=dict(size=5),
            hovertemplate="<b>%{x|%b %Y}</b><br>Spend: ₹%{y:,.0f}<extra></extra>",
        )
    )
    
    fig.update_layout(
        title=dict(
            text="Spend vs Attributed Revenue (Monthly) <span style='font-size:11px;color:#7F8C8D;'>[Sample Data]</span>",
            font=dict(size=14, color=COLOR_PRIMARY),
        ),
        margin=dict(l=20, r=20, t=45, b=30),
        height=320,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            showgrid=False,
            tickformat="%b %y",
            dtick="M1",
        ),
        yaxis=dict(
            title="Amount (₹)",
            showgrid=True,
            gridcolor=COLOR_BORDER,
            zeroline=False,
        ),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_funnel(df_filtered: pd.DataFrame, attribution_model: str) -> go.Figure:
    """Funnel chart showing progression from Impressions to Conversions."""
    tot_imp = int(df_filtered["impressions"].sum())
    tot_clicks = int(df_filtered["clicks"].sum())
    tot_visits = int(df_filtered["visits"].sum())
    tot_leads = int(df_filtered["leads"].sum())
    tot_conv = int(df_filtered["conversions"].sum())
    
    stages = ["Impressions", "Clicks", "Website Visits", "Leads", "Conversions"]
    values = [tot_imp, tot_clicks, tot_visits, tot_leads, tot_conv]
    
    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=values,
            textposition="inside",
            textinfo="value+percent previous",
            texttemplate="%{value:,.0f}<br>(%{percentPrevious:.1%})",
            marker=dict(
                color=["#2C3E50", "#3D566E", "#567697", "#4C9A8C", "#63B4A6"],
            ),
            connector=dict(line=dict(color="#CBD5E1", width=1)),
        )
    )
    
    fig.update_layout(
        title=dict(
            text="Conversion Funnel Efficiency <span style='font-size:11px;color:#7F8C8D;'>[Sample Data]</span>",
            font=dict(size=14, color=COLOR_PRIMARY),
        ),
        margin=dict(l=20, r=20, t=45, b=20),
        height=340,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_cohort_retention(cohort_df: pd.DataFrame) -> go.Figure:
    """Cohort retention heatmap."""
    z_values = cohort_df.values
    text_values = []
    
    for row in z_values:
        row_text = []
        for val in row:
            if pd.isna(val) or val is None:
                row_text.append("—")
            else:
                row_text.append(f"{val:.1f}%")
        text_values.append(row_text)
        
    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=cohort_df.columns.tolist(),
            y=cohort_df.index.tolist(),
            text=text_values,
            texttemplate="%{text}",
            textfont=dict(size=11, color="#1E293B"),
            colorscale=[
                [0.0, "#F1F5F9"],
                [0.4, "#C6E2DC"],
                [0.7, "#7EC1B4"],
                [1.0, "#4C9A8C"],
            ],
            showscale=False,
            hoverongaps=False,
            hovertemplate="Cohort: %{y}<br>%{x}: %{text}<extra></extra>",
        )
    )
    
    fig.update_layout(
        title=dict(
            text="User Retention by Signup Cohort <span style='font-size:11px;color:#7F8C8D;'>[Sample Data]</span>",
            font=dict(size=14, color=COLOR_PRIMARY),
        ),
        margin=dict(l=20, r=20, t=45, b=20),
        height=340,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        xaxis=dict(title="", tickfont=dict(size=11)),
        yaxis=dict(title="", tickfont=dict(size=11), autorange="reversed"),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    return fig


def render_attribution_comparison(df_filtered: pd.DataFrame) -> Tuple[go.Figure, pd.DataFrame]:
    """
    Compare attributed revenue across models: First-click, Last-click, Linear, Markov Chain.
    # TODO: replace with real Markov chain attribution output and transition matrix calculation
    """
    models_to_compare = [
        ("First-click", "revenue_first_click"),
        ("Last-click", "revenue_last_click"),
        ("Linear", "revenue_linear"),
        ("Markov Chain", "revenue_markov"),
    ]
    
    summary = []
    channels = df_filtered["channel"].unique().tolist()
    
    for ch in sorted(channels):
        row = {"Channel": ch}
        ch_df = df_filtered[df_filtered["channel"] == ch]
        for model_label, col in models_to_compare:
            row[model_label] = ch_df[col].sum() if not ch_df.empty else 0.0
        summary.append(row)
        
    comp_df = pd.DataFrame(summary)
    
    fig = go.Figure()
    palette = ["#5D6D7E", "#2C3E50", "#85929E", "#4C9A8C"]
    
    for i, (model_label, _) in enumerate(models_to_compare):
        fig.add_trace(
            go.Bar(
                name=model_label,
                x=comp_df["Channel"],
                y=comp_df[model_label],
                marker=dict(color=palette[i]),
                hovertemplate="<b>%{x}</b> (" + model_label + "): ₹%{y:,.0f}<extra></extra>",
            )
        )
        
    fig.update_layout(
        barmode="group",
        title=dict(
            text="Attributed Revenue by Attribution Model <span style='font-size:11px;color:#7F8C8D;'>[Sample Data]</span>",
            font=dict(size=14, color=COLOR_PRIMARY),
        ),
        margin=dict(l=20, r=20, t=45, b=25),
        height=350,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(
            title="Attributed Revenue (₹)",
            showgrid=True,
            gridcolor=COLOR_BORDER,
            zeroline=False,
        ),
        font=dict(family="sans-serif", size=12, color="#334155"),
    )
    
    return fig, comp_df


# ==============================================================================
# 5. WHAT-IF SIMULATOR & DIMINISHING RETURNS ENGINE
# ==============================================================================
def calculate_diminishing_returns(allocations: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """
    Compute projected conversions and revenue using calibrated saturation curves.
    Formula per channel:
    Conversions = Max_Capacity * (Spend / (Spend + Saturation_Constant))^Alpha
    
    # TODO: Replace with real Marketing Mix Modeling (MMM) / Bayesian response curves
    # (e.g. using PyMC-Marketing, Robyn, or LightweightMMM).
    """
    # Channel curve parameters: (max_conversions_scale, saturation_spend, elasticity_alpha, aov)
    channel_curves = {
        "Search":  {"max_scale": 1150, "half_sat": 240000, "alpha": 0.85, "aov": 2450},
        "Social":  {"max_scale": 950,  "half_sat": 160000, "alpha": 0.65, "aov": 1950},  # Saturates faster
        "Email":   {"max_scale": 780,  "half_sat": 120000, "alpha": 0.90, "aov": 2650},  # High efficiency
        "Display": {"max_scale": 450,  "half_sat": 140000, "alpha": 0.55, "aov": 1750},
        "Website": {"max_scale": 600,  "half_sat": 110000, "alpha": 0.80, "aov": 2250},
    }
    
    results = {}
    for ch, spend in allocations.items():
        if spend <= 0:
            results[ch] = {"spend": 0.0, "conversions": 0, "revenue": 0.0, "roas": 0.0}
            continue
            
        curve = channel_curves.get(ch, {"max_scale": 600, "half_sat": 150000, "alpha": 0.75, "aov": 2000})
        
        # Diminishing returns curve response
        ratio = spend / (spend + curve["half_sat"])
        conversions = int(curve["max_scale"] * (ratio ** curve["alpha"]))
        revenue = round(conversions * curve["aov"], 2)
        roas = (revenue / spend) if spend > 0 else 0.0
        
        results[ch] = {
            "spend": float(spend),
            "conversions": conversions,
            "revenue": revenue,
            "roas": roas,
        }
        
    return results


# ==============================================================================
# 6. MAIN APPLICATION LAYOUT & CONTROLLER
# ==============================================================================
def main():
    apply_custom_styles()
    
    # Header area
    col_hdr_left, col_hdr_right = st.columns([3, 1])
    with col_hdr_left:
        st.markdown(
            '<div class="app-header-title">Marketing Campaign Effectiveness Analysis'
            '<span class="sample-badge">Sample Data</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="app-header-subtitle">'
            'Interactive ROI Decision-Support System & Multi-Touch Attribution Simulator '
            '· Academic Research Prototype</div>',
            unsafe_allow_html=True,
        )
    with col_hdr_right:
        st.caption("Environment: Deterministic Benchmark\nSeed: 42 (Reproducible)")
        
    # Load Master Data
    master_df, cohort_df = generate_synthetic_data(seed=42)
    
    # -------------------------------------------------------------------------
    # SIDEBAR CONTROLS
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### Filters & Dimensions")
        
        # 1. Date Range
        min_date = master_df["date"].dt.date.min()
        max_date = master_df["date"].dt.date.max()
        default_start = max_date - timedelta(days=180)
        
        selected_date_range = st.date_input(
            "Date Range",
            value=(default_start, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter data to a specific operational evaluation window.",
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
            
        # 3. Attribution Model Dropdown
        attribution_options = [
            "Markov Chain",
            "Last-click",
            "First-click",
            "Linear",
            "Shapley Value",
        ]
        selected_model = st.selectbox(
            "Attribution Model",
            options=attribution_options,
            index=0,
            help="Select attribution logic for weighting revenue across touchpoints.",
        )
        
        # 4. Region Dropdown
        region_options = ["All", "North", "South", "East", "West"]
        selected_region = st.selectbox(
            "Geographic Region",
            options=region_options,
            index=0,
            help="Segment campaign results by geographical market territory.",
        )
        
        st.divider()
        st.caption(
            "**Data Architecture Note:**\n"
            "This interface is currently wired to a simulated research dataset. "
            "All metrics recalculate dynamically to simulate real-time production analytics."
        )
        
    # Apply Filtering
    df_filtered = filter_dataset(
        master_df,
        date_range=date_filter,
        selected_channels=selected_channels,
        selected_region=selected_region,
    )
    
    # -------------------------------------------------------------------------
    # TOP KPI ROW (4 METRIC CARDS)
    # -------------------------------------------------------------------------
    kpis = compute_kpis(df_filtered, selected_model)
    
    # Baseline comparisons (approximate prior period benchmark)
    baseline_spend = kpis["spend"] * 0.96
    baseline_rev = kpis["revenue"] * 0.92
    baseline_conv = int(kpis["conversions"] * 0.94)
    baseline_roas = (baseline_rev / baseline_spend) if baseline_spend > 0 else 0.0
    
    spend_delta = ((kpis["spend"] - baseline_spend) / baseline_spend * 100) if baseline_spend > 0 else 0
    rev_delta = ((kpis["revenue"] - baseline_rev) / baseline_rev * 100) if baseline_rev > 0 else 0
    conv_delta = ((kpis["conversions"] - baseline_conv) / baseline_conv * 100) if baseline_conv > 0 else 0
    roas_delta = kpis["roas"] - baseline_roas
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        with st.container(border=True):
            st.metric(
                label="Total Spend",
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
            st.caption("Evaluated at selected attribution weights")
            
    with kpi_col3:
        with st.container(border=True):
            st.metric(
                label="Total Conversions",
                value=f"{kpis['conversions']:,}",
                delta=f"{conv_delta:+.1f}% vs baseline",
            )
            cpa = (kpis["spend"] / kpis["conversions"]) if kpis["conversions"] > 0 else 0
            st.caption(f"Blended CPA: {format_currency_inr(cpa)}")
            
    with kpi_col4:
        with st.container(border=True):
            st.metric(
                label="ROAS / Net ROI%",
                value=f"{kpis['roas']:.2f}x ({kpis['roi_percent']:+.1f}%)",
                delta=f"{roas_delta:+.2f}x vs baseline",
            )
            st.caption("Net return on media spend")

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
    # TAB 1: TWO CHARTS SIDE BY SIDE
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
                    "Monthly spend vs attributed revenue trend over the selected window. "
                    "Evaluates whether revenue growth tracks or outpaces spend increases."
                )
                
    # -------------------------------------------------------------------------
    # TAB 2: FUNNEL + COHORT SECTION (TWO COLUMNS)
    # -------------------------------------------------------------------------
    with tab2:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        sec_col1, sec_col2 = st.columns(2)
        
        with sec_col1:
            with st.container(border=True):
                fig_funnel = render_funnel(df_filtered, selected_model)
                st.plotly_chart(fig_funnel, use_container_width=True)
                st.caption(
                    "Multi-stage macro funnel showing drop-offs between stages. "
                    "Numbers inside brackets indicate transition percentage from preceding stage."
                )
                
        with sec_col2:
            with st.container(border=True):
                fig_cohort = render_cohort_retention(cohort_df)
                st.plotly_chart(fig_cohort, use_container_width=True)
                st.caption(
                    "Retention matrix tracking customer engagement across 0 to 3 months post-acquisition. "
                    "Useful for understanding long-term cohort value decay."
                )
                
    # -------------------------------------------------------------------------
    # TAB 3: ATTRIBUTION MODEL COMPARISON
    # -------------------------------------------------------------------------
    with tab3:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            fig_attr, comp_df = render_attribution_comparison(df_filtered)
            st.plotly_chart(fig_attr, use_container_width=True)
            
            # Required analytical insight note
            st.info(
                "💡 **Analytical Insight:** Last-click often underestimates awareness channels like Social.",
                icon="ℹ️",
            )
            
            # Formatted data comparison table
            with st.expander("View Numerical Model Comparison Table", expanded=False):
                display_table = comp_df.copy()
                for col in ["First-click", "Last-click", "Linear", "Markov Chain"]:
                    if col in display_table.columns:
                        display_table[col] = display_table[col].apply(format_currency_inr)
                st.dataframe(display_table, use_container_width=True, hide_index=True)
                
    # -------------------------------------------------------------------------
    # TAB 4: AI RECOMMENDATION + WHAT-IF SIMULATOR
    # -------------------------------------------------------------------------
    with tab4:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        
        # Centerpiece: Calm, bordered recommendation card
        st.markdown(
            """
            <div class="recommendation-card">
                <div class="recommendation-card-title">
                    Recommended: Shift ₹50,000 from Social to Email
                </div>
                <div class="recommendation-card-impact">
                    Projected Impact: +8.0% Conversions · +12.0% Estimated ROI
                </div>
                <div class="recommendation-card-body">
                    <strong>Analytical Rationale:</strong> Empirical marginal return curves indicate 
                    Social channel spend has reached diminishing efficiency (marginal ROAS has dropped 
                    to 1.4x), whereas Email retains significant headroom with an estimated marginal ROAS 
                    of 3.8x. Shifting ₹50,000 rebalances the portfolio toward peak frontier efficiency.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("#### Interactive Budget Allocation Simulator")
        st.caption(
            "Adjust target media allocations across channels to test what-if budget scenarios. "
            "Total planned budget target: **₹8,00,000** (Sample Research Baseline)."
        )
        
        # Default baseline allocations (sum = 800,000)
        baseline_allocations = {
            "Search": 280000,
            "Social": 240000,
            "Email": 110000,
            "Display": 100000,
            "Website": 70000,
        }
        
        TOTAL_TARGET_BUDGET = 800000
        
        # Sliders layout
        sim_col_controls, sim_col_results = st.columns([1.1, 1.4])
        
        with sim_col_controls:
            with st.container(border=True):
                st.markdown("**Channel Budget Allocation (₹)**")
                
                slider_search = st.slider(
                    "Search Budget",
                    min_value=0,
                    max_value=500000,
                    value=baseline_allocations["Search"],
                    step=10000,
                    format="₹%d",
                )
                slider_social = st.slider(
                    "Social Budget",
                    min_value=0,
                    max_value=500000,
                    value=baseline_allocations["Social"],
                    step=10000,
                    format="₹%d",
                )
                slider_email = st.slider(
                    "Email Budget",
                    min_value=0,
                    max_value=300000,
                    value=baseline_allocations["Email"],
                    step=5000,
                    format="₹%d",
                )
                slider_display = st.slider(
                    "Display Budget",
                    min_value=0,
                    max_value=300000,
                    value=baseline_allocations["Display"],
                    step=5000,
                    format="₹%d",
                )
                slider_website = st.slider(
                    "Website Budget",
                    min_value=0,
                    max_value=250000,
                    value=baseline_allocations["Website"],
                    step=5000,
                    format="₹%d",
                )
                
                current_sim_alloc = {
                    "Search": slider_search,
                    "Social": slider_social,
                    "Email": slider_email,
                    "Display": slider_display,
                    "Website": slider_website,
                }
                
                current_total_allocated = sum(current_sim_alloc.values())
                diff = current_total_allocated - TOTAL_TARGET_BUDGET
                
                # Budget balance indicator
                if diff == 0:
                    st.success(f"✓ Total Allocated: {format_currency_inr(current_total_allocated)} (Balanced)")
                elif diff > 0:
                    st.warning(f"Over budget by {format_currency_inr(diff)} (Total: {format_currency_inr(current_total_allocated)})")
                else:
                    st.info(f"Under budget by {format_currency_inr(abs(diff))} (Total: {format_currency_inr(current_total_allocated)})")
                    
                st.button("Run Scenario & Compare", type="primary", use_container_width=True)
                
        with sim_col_results:
            with st.container(border=True):
                st.markdown("**Scenario Evaluation & Diminishing Returns Projection**")
                
                # Compute baseline vs simulated results
                baseline_results = calculate_diminishing_returns(baseline_allocations)
                simulated_results = calculate_diminishing_returns(current_sim_alloc)
                
                tot_base_spend = sum(res["spend"] for res in baseline_results.values())
                tot_base_conv = sum(res["conversions"] for res in baseline_results.values())
                tot_base_rev = sum(res["revenue"] for res in baseline_results.values())
                tot_base_roas = tot_base_rev / tot_base_spend if tot_base_spend > 0 else 0
                
                tot_sim_spend = sum(res["spend"] for res in simulated_results.values())
                tot_sim_conv = sum(res["conversions"] for res in simulated_results.values())
                tot_sim_rev = sum(res["revenue"] for res in simulated_results.values())
                tot_sim_roas = tot_sim_rev / tot_sim_spend if tot_sim_spend > 0 else 0
                
                conv_change_pct = ((tot_sim_conv - tot_base_conv) / tot_base_conv * 100) if tot_base_conv > 0 else 0
                rev_change_pct = ((tot_sim_rev - tot_base_rev) / tot_base_rev * 100) if tot_base_rev > 0 else 0
                roas_delta_sim = tot_sim_roas - tot_base_roas
                
                # Top metrics for simulation
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric(
                        "Projected Conversions",
                        f"{tot_sim_conv:,}",
                        f"{conv_change_pct:+.1f}% vs baseline",
                    )
                with m_col2:
                    st.metric(
                        "Projected Revenue",
                        format_currency_inr(tot_sim_rev),
                        f"{rev_change_pct:+.1f}% vs baseline",
                    )
                with m_col3:
                    st.metric(
                        "Projected ROAS",
                        f"{tot_sim_roas:.2f}x",
                        f"{roas_delta_sim:+.2f}x vs baseline",
                    )
                    
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                st.markdown("**Before / After Scenario Comparison Table**")
                
                # Build plain comparison table
                comparison_rows = []
                for ch in ["Search", "Social", "Email", "Display", "Website"]:
                    b = baseline_results[ch]
                    s = simulated_results[ch]
                    comparison_rows.append({
                        "Channel": ch,
                        "Base Spend": format_currency_inr(b["spend"]),
                        "Sim Spend": format_currency_inr(s["spend"]),
                        "Base Conv": b["conversions"],
                        "Sim Conv": s["conversions"],
                        "Base ROAS": f"{b['roas']:.2f}x",
                        "Sim ROAS": f"{s['roas']:.2f}x",
                        "Revenue Impact": format_currency_inr(s["revenue"] - b["revenue"]),
                    })
                    
                # Add total row
                comparison_rows.append({
                    "Channel": "TOTAL",
                    "Base Spend": format_currency_inr(tot_base_spend),
                    "Sim Spend": format_currency_inr(tot_sim_spend),
                    "Base Conv": tot_base_conv,
                    "Sim Conv": tot_sim_conv,
                    "Base ROAS": f"{tot_base_roas:.2f}x",
                    "Sim ROAS": f"{tot_sim_roas:.2f}x",
                    "Revenue Impact": format_currency_inr(tot_sim_rev - tot_base_rev),
                })
                
                comp_table_df = pd.DataFrame(comparison_rows)
                st.dataframe(comp_table_df, use_container_width=True, hide_index=True)
                
                st.caption(
                    "Simulation uses non-linear diminishing marginal returns (Hill equation saturation curve). "
                    "Real deployment would calibrate α and half-saturation values using Bayesian Markov Chain Monte Carlo (MCMC)."
                )


if __name__ == "__main__":
    main()
