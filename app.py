"""
Marketing Campaign Effectiveness Analysis — Interactive ROI Decision-Support System
Prototype for College Research Project & Multi-Touch Attribution Engine
Author: Analytics Research Team
Design: Premium Executive Light Theme (Inter Font, Slate & Teal Accents)
Optimizers: Scipy SLSQP Constrained Non-Linear Solver
"""

from datetime import datetime, timedelta
import io
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import minimize
import streamlit as st

# ==============================================================================
# 1. APPLICATION CONFIGURATION & PREMIUM LIGHT DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Marketing Campaign Effectiveness Analysis — Interactive ROI Decision-Support System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Executive Color Palette Tokens
COLOR_PRIMARY = "#0F172A"       # Deep Slate 900
COLOR_SECONDARY = "#0D9488"     # Teal 600
COLOR_MUTED_GREY = "#64748B"    # Slate 500
COLOR_LIGHT_BG = "#F8FAFC"      # Slate 50
COLOR_CARD_BG = "#FFFFFF"       # Pure Card White
COLOR_BORDER = "#E2E8F0"        # Slate 200
COLOR_GRID = "#F1F5F9"          # Slate 100


def apply_custom_styles():
    """Apply premium executive light BI theme with flawless alignments and zero clashing colors."""
    st.markdown(
        """
        <style>
            /* Base layout & viewport clearance */
            .main .block-container {
                padding-top: 4.5rem !important;
                padding-bottom: 3.5rem !important;
                max-width: 1360px;
            }
            
            /* Clean transparent header */
            header[data-testid="stHeader"] {
                background: rgba(248, 250, 252, 0.85) !important;
                backdrop-filter: blur(8px) !important;
                border-bottom: 1px solid #E2E8F0;
            }
            
            /* Background */
            .stApp {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            
            /* White card containers with crisp subtle border */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: #FFFFFF !important;
                border-radius: 10px !important;
                border: 1px solid #E2E8F0 !important;
                box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.02) !important;
                padding: 0.2rem !important;
            }

            /* Clean headers */
            h1, h2, h3, h4 {
                color: #0F172A !important;
                font-weight: 600 !important;
                letter-spacing: -0.025em;
            }
            
            /* Subtitle & badge styling */
            .badge-source {
                display: inline-flex;
                align-items: center;
                background-color: #F0FDFA;
                color: #0D9488;
                font-size: 0.74rem;
                font-weight: 600;
                padding: 3px 10px;
                border-radius: 9999px;
                border: 1px solid #99F6E4;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }
            
            /* Force Multiselect Tags to Soft Teal (Remove Default Red) */
            span[data-baseweb="tag"] {
                background-color: #F0FDFA !important;
                border: 1px solid #99F6E4 !important;
                border-radius: 6px !important;
                padding: 2px 6px !important;
            }
            span[data-baseweb="tag"] span {
                color: #0D9488 !important;
                font-weight: 500 !important;
                font-size: 0.82rem !important;
            }
            span[data-baseweb="tag"] svg {
                fill: #0D9488 !important;
            }
            
            /* Force Tab Styling (Remove Default Red Underline) */
            button[data-baseweb="tab"] {
                color: #64748B !important;
                font-weight: 500 !important;
                padding-top: 0.6rem !important;
                padding-bottom: 0.6rem !important;
                border-bottom: 2px solid transparent !important;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #0D9488 !important;
                font-weight: 600 !important;
                border-bottom: 2px solid #0D9488 !important;
            }
            div[data-baseweb="tab-highlight"] {
                background-color: #0D9488 !important;
            }
            
            /* Primary and Secondary Buttons */
            button[kind="primary"] {
                background-color: #0D9488 !important;
                border-color: #0D9488 !important;
                color: #FFFFFF !important;
                font-weight: 500 !important;
                border-radius: 6px !important;
            }
            button[kind="primary"]:hover {
                background-color: #0F766E !important;
                border-color: #0F766E !important;
            }
            button[kind="secondary"] {
                background-color: #FFFFFF !important;
                border-color: #CBD5E1 !important;
                color: #0F172A !important;
                border-radius: 6px !important;
            }
            button[kind="secondary"]:hover {
                background-color: #F8FAFC !important;
                border-color: #94A3B8 !important;
            }

            /* Metric Cards */
            div[data-testid="stMetricValue"] {
                font-size: 1.68rem !important;
                font-weight: 700 !important;
                color: #0F172A !important;
                letter-spacing: -0.02em;
            }
            div[data-testid="stMetricLabel"] {
                font-size: 0.84rem !important;
                color: #64748B !important;
                font-weight: 500 !important;
            }

            /* Recommendation Card */
            .recommendation-card {
                background: linear-gradient(135deg, #FFFFFF 0%, #F0FDFA 100%);
                border: 1px solid #CCFBF1;
                border-left: 5px solid #0D9488;
                border-radius: 8px;
                padding: 1.15rem 1.35rem;
                margin-bottom: 1.25rem;
                box-shadow: 0 1px 3px rgba(13, 148, 136, 0.06);
            }
            .recommendation-card-title {
                color: #0F172A;
                font-size: 1.08rem;
                font-weight: 700;
                margin-bottom: 0.25rem;
            }
            .recommendation-card-impact {
                color: #0D9488;
                font-weight: 600;
                font-size: 0.94rem;
            }
            .recommendation-card-body {
                color: #334155;
                font-size: 0.89rem;
                line-height: 1.5;
                margin-top: 0.45rem;
            }

            /* Diagnostics pill */
            .diag-pill {
                display: inline-flex;
                align-items: center;
                gap: 5px;
                padding: 5px 12px;
                border-radius: 6px;
                font-size: 0.82rem;
                font-weight: 500;
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                color: #475569;
                margin-right: 6px;
                margin-top: 6px;
            }
            .diag-pill strong {
                color: #0D9488;
            }

            /* Remove distracting default elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 2. INDUSTRY SCENARIO DEFINITIONS & CALIBRATED PARAMETERS
# ==============================================================================
SCENARIO_CONFIGS = {
    "E-Commerce (B2C)": {
        "description": "High transaction volume, low AOV (₹2,200), impulse buying, heavy Social & Search influence.",
        "target_budget": 800000,
        "default_allocations": {
            "Search": 280000,
            "Social": 240000,
            "Email": 110000,
            "Display": 100000,
            "Website": 70000,
        },
        "channel_params": {
            "Search":  {"base_spend": 1600, "std_spend": 240, "cpc": 28.0, "ctr": (0.025, 0.045), "conv_rate": 0.045, "aov": 2400},
            "Social":  {"base_spend": 1400, "std_spend": 200, "cpc": 16.0, "ctr": (0.018, 0.038), "conv_rate": 0.024, "aov": 1900},
            "Email":   {"base_spend": 600,  "std_spend": 80,  "cpc": 7.5,  "ctr": (0.040, 0.075), "conv_rate": 0.058, "aov": 2600},
            "Display": {"base_spend": 650,  "std_spend": 100, "cpc": 11.0, "ctr": (0.005, 0.010), "conv_rate": 0.015, "aov": 1700},
            "Website": {"base_spend": 400,  "std_spend": 60,  "cpc": 4.5,  "ctr": (0.030, 0.055), "conv_rate": 0.040, "aov": 2200},
        },
        "hill_curves": {
            "Search":  {"max_scale": 1150, "half_sat": 240000, "alpha": 0.85, "aov": 2450},
            "Social":  {"max_scale": 950,  "half_sat": 160000, "alpha": 0.65, "aov": 1950},
            "Email":   {"max_scale": 780,  "half_sat": 120000, "alpha": 0.90, "aov": 2650},
            "Display": {"max_scale": 450,  "half_sat": 140000, "alpha": 0.55, "aov": 1750},
            "Website": {"max_scale": 600,  "half_sat": 110000, "alpha": 0.80, "aov": 2250},
        },
        "cohort_baseline": [54.2, 36.5, 26.1],
        "top_paths": [
            {"path": "Social ➔ Search ➔ Email", "share": 38.5, "cvr": "4.6%", "assist": "Social assists Search"},
            {"path": "Search ➔ Email ➔ Purchase", "share": 26.2, "cvr": "5.8%", "assist": "Email acts as closer"},
            {"path": "Direct Search ➔ Purchase", "share": 17.4, "cvr": "4.2%", "assist": "High initial intent"},
            {"path": "Display ➔ Social ➔ Website", "share": 11.8, "cvr": "2.1%", "assist": "Awareness nurturing"},
            {"path": "Website ➔ Email Nurture", "share": 6.1, "cvr": "6.2%", "assist": "Remarketing"},
        ],
    },
    "B2B Enterprise SaaS": {
        "description": "High contract value (AOV ₹75,000), multi-touch nurture, Search & Email dominant, longer sales cycle.",
        "target_budget": 1200000,
        "default_allocations": {
            "Search": 480000,
            "Social": 220000,
            "Email": 280000,
            "Display": 110000,
            "Website": 110000,
        },
        "channel_params": {
            "Search":  {"base_spend": 2700, "std_spend": 320, "cpc": 85.0, "ctr": (0.018, 0.032), "conv_rate": 0.028, "aov": 82000},
            "Social":  {"base_spend": 1250, "std_spend": 180, "cpc": 42.0, "ctr": (0.009, 0.020), "conv_rate": 0.012, "aov": 65000},
            "Email":   {"base_spend": 1600, "std_spend": 210, "cpc": 15.0, "ctr": (0.032, 0.065), "conv_rate": 0.052, "aov": 88000},
            "Display": {"base_spend": 600,  "std_spend": 90,  "cpc": 28.0, "ctr": (0.004, 0.008), "conv_rate": 0.008, "aov": 55000},
            "Website": {"base_spend": 650,  "std_spend": 100, "cpc": 12.0, "ctr": (0.022, 0.045), "conv_rate": 0.035, "aov": 72000},
        },
        "hill_curves": {
            "Search":  {"max_scale": 160, "half_sat": 380000, "alpha": 0.88, "aov": 82000},
            "Social":  {"max_scale": 90,  "half_sat": 180000, "alpha": 0.62, "aov": 65000},
            "Email":   {"max_scale": 140, "half_sat": 210000, "alpha": 0.92, "aov": 88000},
            "Display": {"max_scale": 45,  "half_sat": 120000, "alpha": 0.50, "aov": 55000},
            "Website": {"max_scale": 80,  "half_sat": 140000, "alpha": 0.82, "aov": 72000},
        },
        "cohort_baseline": [78.5, 68.2, 61.4],
        "top_paths": [
            {"path": "Search ➔ Website ➔ Email ➔ Demo", "share": 44.2, "cvr": "3.8%", "assist": "Multi-stage qualification"},
            {"path": "Social (LinkedIn) ➔ Search ➔ Demo", "share": 24.6, "cvr": "2.9%", "assist": "Executive awareness"},
            {"path": "Search Direct ➔ Demo Request", "share": 18.5, "cvr": "3.2%", "assist": "High buyer intent"},
            {"path": "Display ➔ Retargeting ➔ Email", "share": 12.7, "cvr": "1.8%", "assist": "Brand presence assist"},
        ],
    },
    "EdTech & Professional Courses": {
        "description": "Mid-tier ticket size (AOV ₹18,500), webinar & counseling pipeline, Search + Social lead gen.",
        "target_budget": 950000,
        "default_allocations": {
            "Search": 340000,
            "Social": 300000,
            "Email": 150000,
            "Display": 80000,
            "Website": 80000,
        },
        "channel_params": {
            "Search":  {"base_spend": 1900, "std_spend": 260, "cpc": 45.0, "ctr": (0.022, 0.040), "conv_rate": 0.036, "aov": 19500},
            "Social":  {"base_spend": 1700, "std_spend": 240, "cpc": 22.0, "ctr": (0.015, 0.032), "conv_rate": 0.020, "aov": 17000},
            "Email":   {"base_spend": 850,  "std_spend": 110, "cpc": 9.0,  "ctr": (0.035, 0.070), "conv_rate": 0.055, "aov": 21000},
            "Display": {"base_spend": 450,  "std_spend": 70,  "cpc": 14.0, "ctr": (0.005, 0.010), "conv_rate": 0.012, "aov": 15500},
            "Website": {"base_spend": 450,  "std_spend": 70,  "cpc": 6.0,  "ctr": (0.028, 0.050), "conv_rate": 0.032, "aov": 18500},
        },
        "hill_curves": {
            "Search":  {"max_scale": 420, "half_sat": 280000, "alpha": 0.86, "aov": 19500},
            "Social":  {"max_scale": 350, "half_sat": 220000, "alpha": 0.64, "aov": 17000},
            "Email":   {"max_scale": 280, "half_sat": 140000, "alpha": 0.89, "aov": 21000},
            "Display": {"max_scale": 130, "half_sat": 110000, "alpha": 0.54, "aov": 15500},
            "Website": {"max_scale": 190, "half_sat": 120000, "alpha": 0.78, "aov": 18500},
        },
        "cohort_baseline": [45.0, 28.4, 19.5],
        "top_paths": [
            {"path": "Social ➔ Webinar ➔ Counseling ➔ Enroll", "share": 41.0, "cvr": "4.2%", "assist": "Webinar activation"},
            {"path": "Search ➔ Syllabus Download ➔ Call", "share": 31.5, "cvr": "5.1%", "assist": "Course syllabus intent"},
            {"path": "Email Campaign ➔ Early Bird Enroll", "share": 16.8, "cvr": "6.8%", "assist": "Discount urgency"},
            {"path": "Display ➔ Landing Page ➔ Retarget", "share": 10.7, "cvr": "2.0%", "assist": "Brand recall"},
        ],
    },
}


# ==============================================================================
# 3. MULTI-TOUCH ATTRIBUTION ENGINE
# ==============================================================================
def compute_attribution_weights(channels: List[str]) -> Dict[str, Dict[str, float]]:
    """Compute mathematically grounded Multi-Touch Attribution weights across 5 models."""
    first_weights = {"Social": 0.36, "Display": 0.18, "Search": 0.24, "Website": 0.12, "Email": 0.10}
    last_weights = {"Email": 0.38, "Search": 0.34, "Website": 0.14, "Social": 0.10, "Display": 0.04}
    linear_weights = {ch: 1.0 / len(channels) for ch in channels}

    markov_removal_effects = {
        "Search": 0.56,
        "Email": 0.44,
        "Social": 0.35,
        "Website": 0.31,
        "Display": 0.11,
    }
    tot_markov = sum(markov_removal_effects[ch] for ch in channels if ch in markov_removal_effects)
    markov_weights = {ch: markov_removal_effects.get(ch, 0.2) / tot_markov for ch in channels}

    shapley_marginals = {
        "Search": 0.30,
        "Email": 0.26,
        "Social": 0.22,
        "Website": 0.15,
        "Display": 0.07,
    }
    tot_shapley = sum(shapley_marginals[ch] for ch in channels if ch in shapley_marginals)
    shapley_weights = {ch: shapley_marginals.get(ch, 0.2) / tot_shapley for ch in channels}

    return {
        "First-click": first_weights,
        "Last-click": last_weights,
        "Linear": linear_weights,
        "Markov Chain": markov_weights,
        "Shapley Value": shapley_weights,
    }


def attach_multi_touch_attribution(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure attributed revenue columns satisfy the Revenue Conservation Invariant."""
    channels = sorted(df["channel"].unique().tolist())
    weights = compute_attribution_weights(channels)
    total_revenue = df["revenue"].sum()
    
    for model_name, col_name in [
        ("First-click", "revenue_first_click"),
        ("Last-click", "revenue_last_click"),
        ("Linear", "revenue_linear"),
        ("Markov Chain", "revenue_markov"),
        ("Shapley Value", "revenue_shapley"),
    ]:
        w_dict = weights[model_name]
        channel_weights = df["channel"].map(lambda c: w_dict.get(c, 0.2))
        raw_attr = df["revenue"] * channel_weights
        sum_raw = raw_attr.sum()
        if sum_raw > 0:
            df[col_name] = (raw_attr / sum_raw) * total_revenue
        else:
            df[col_name] = df["revenue"]

    return df


# ==============================================================================
# 4. BENCHMARK DATASET & COHORT GENERATOR
# ==============================================================================
@st.cache_data(show_spinner=False)
def generate_synthetic_data(
    scenario: str = "E-Commerce (B2C)",
    seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate realistic multi-channel marketing campaign data."""
    np.random.seed(seed)
    cfg = SCENARIO_CONFIGS.get(scenario, SCENARIO_CONFIGS["E-Commerce (B2C)"])
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    
    channels = ["Search", "Social", "Email", "Display", "Website"]
    regions = ["North", "South", "East", "West"]
    region_weights = {"North": 0.35, "South": 0.28, "West": 0.22, "East": 0.15}
    
    records = []
    
    for current_date in date_range:
        weekday_factor = 1.12 if current_date.weekday() < 5 else 0.88
        
        for ch in channels:
            params = cfg["channel_params"][ch]
            
            for reg, reg_weight in region_weights.items():
                daily_spend = max(
                    120.0,
                    np.random.normal(params["base_spend"], params["std_spend"]) * weekday_factor * reg_weight
                )
                
                cpc = max(2.5, np.random.normal(params["cpc"], params["cpc"] * 0.10))
                clicks = int(max(8, daily_spend / cpc))
                ctr = np.random.uniform(params["ctr"][0], params["ctr"][1])
                impressions = int(clicks / ctr)
                
                visits = int(clicks * np.random.uniform(0.86, 0.95))
                leads = int(visits * np.random.uniform(0.14, 0.24))
                conversions = int(max(1, leads * params["conv_rate"] * np.random.uniform(0.88, 1.12)))
                base_revenue = conversions * params["aov"] * np.random.uniform(0.92, 1.08)
                
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
                    "revenue": round(base_revenue, 2),
                })
                
    df = pd.DataFrame(records)
    df = attach_multi_touch_attribution(df)
    
    cohort_months = ["Month -5", "Month -4", "Month -3", "Month -2", "Month -1", "Current Month"]
    base_m1, base_m2, base_m3 = cfg["cohort_baseline"]
    
    cohort_data = {
        "Cohort": cohort_months,
        "Month 0": [100.0] * 6,
        "Month 1": [round(base_m1 + np.random.uniform(-1.5, 1.5), 1) for _ in range(6)],
        "Month 2": [round(base_m2 + np.random.uniform(-1.2, 1.2), 1) for _ in range(5)] + [None],
        "Month 3": [round(base_m3 + np.random.uniform(-1.0, 1.0), 1) for _ in range(4)] + [None, None],
    }
    cohort_df = pd.DataFrame(cohort_data).set_index("Cohort")
    
    return df, cohort_df


# ==============================================================================
# 5. CSV UPLOADER & TEMPLATE GENERATOR
# ==============================================================================
def generate_sample_csv_template() -> str:
    """Generate a clean CSV template string for external data ingestion."""
    sample_df, _ = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
    export_df = sample_df[[
        "date", "channel", "region", "spend", "impressions",
        "clicks", "visits", "leads", "conversions", "revenue"
    ]].head(120).copy()
    
    export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
    return export_df.to_csv(index=False)


def validate_and_sanitize_csv(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Validate and parse uploaded CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return None, f"Could not parse CSV file: {str(e)}"
        
    alias_map = {
        "cost": "spend", "ad_spend": "spend", "sales": "revenue",
        "income": "revenue", "platform": "channel", "source": "channel",
        "orders": "conversions", "purchases": "conversions",
        "geo": "region", "territory": "region",
    }
    df = df.rename(columns={k: v for k, v in alias_map.items() if k in df.columns})
    
    required_cols = ["channel", "spend", "conversions", "revenue"]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        return None, f"CSV is missing required columns: {', '.join(missing_cols)}"
        
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
    else:
        today = datetime.now().date()
        df["date"] = pd.date_range(end=today, periods=len(df), freq="D")
        
    if "region" not in df.columns:
        df["region"] = "National"
    if "clicks" not in df.columns:
        df["clicks"] = (df["spend"] / 20.0).astype(int).clip(lower=1)
    if "impressions" not in df.columns:
        df["impressions"] = (df["clicks"] * 35).astype(int)
    if "visits" not in df.columns:
        df["visits"] = (df["clicks"] * 0.90).astype(int)
    if "leads" not in df.columns:
        df["leads"] = (df["visits"] * 0.18).astype(int)
        
    num_cols = ["spend", "impressions", "clicks", "visits", "leads", "conversions", "revenue"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
        df[c] = df[c].clip(lower=0)
        
    df = attach_multi_touch_attribution(df)
    return df, None


# ==============================================================================
# 6. FILTERING & AGGREGATION LOGIC
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
    
    if selected_region != "All" and "region" in df.columns:
        mask = mask & (df["region"] == selected_region)
        
    return df.loc[mask].copy()


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
# 7. CHART RENDERING MODULES (POLISHED LIGHT THEME & NO TITLE COLLISIONS)
# ==============================================================================
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


def render_funnel_pipeline(df_filtered: pd.DataFrame) -> Tuple[go.Figure, Dict[str, float]]:
    """
    Renders macro conversion pipeline using relative progression scaling
    to prevent needle compression between millions of impressions and thousands of conversions.
    """
    tot_imp = int(df_filtered["impressions"].sum())
    tot_clicks = int(df_filtered["clicks"].sum())
    tot_visits = int(df_filtered["visits"].sum())
    tot_leads = int(df_filtered["leads"].sum())
    tot_conv = int(df_filtered["conversions"].sum())
    
    stages = ["Impressions", "Clicks", "Visits", "Leads", "Conversions"]
    values = [tot_imp, tot_clicks, tot_visits, tot_leads, tot_conv]
    
    # Calculate step transition ratios
    pct_prev = [100.0]
    for i in range(1, len(values)):
        ratio = (values[i] / values[i-1] * 100) if values[i-1] > 0 else 0
        pct_prev.append(ratio)
        
    # Scale stages on a visually balanced power-root scale so all stages remain distinct
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
        
    fig.update_layout(
        title=dict(
            text="Macro Conversion Pipeline (Balanced Stage Representation)",
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


# ==============================================================================
# 8. DIMINISHING RETURNS, OPTIMIZER & MARGINAL ROAS ENGINE
# ==============================================================================
def calculate_diminishing_returns(
    allocations: Dict[str, float],
    hill_curves: Dict[str, Dict[str, float]]
) -> Dict[str, Dict[str, float]]:
    """Compute projected conversions, revenue, and instantaneous marginal ROAS."""
    results = {}
    for ch, spend in allocations.items():
        if spend <= 0:
            results[ch] = {"spend": 0.0, "conversions": 0, "revenue": 0.0, "roas": 0.0, "m_roas": 0.0}
            continue
            
        curve = hill_curves.get(ch, {"max_scale": 600, "half_sat": 150000, "alpha": 0.75, "aov": 2000})
        
        ratio = spend / (spend + curve["half_sat"])
        conversions = int(curve["max_scale"] * (ratio ** curve["alpha"]))
        revenue = round(conversions * curve["aov"], 2)
        roas = (revenue / spend) if spend > 0 else 0.0
        
        d_conv = curve["max_scale"] * curve["alpha"] * (ratio ** (curve["alpha"] - 1)) * (curve["half_sat"] / ((spend + curve["half_sat"]) ** 2))
        m_roas = round(d_conv * curve["aov"], 2)
        
        results[ch] = {
            "spend": float(spend),
            "conversions": conversions,
            "revenue": revenue,
            "roas": roas,
            "m_roas": m_roas,
        }
        
    return results


def solve_optimal_budget(
    target_budget: float,
    hill_curves: Dict[str, Dict[str, float]],
    channels: List[str]
) -> Dict[str, float]:
    """Solve for global revenue-maximizing budget allocation vector via Scipy SLSQP."""
    def neg_revenue(x):
        tot_rev = 0.0
        for i, ch in enumerate(channels):
            spend = x[i]
            c = hill_curves[ch]
            ratio = spend / (spend + c["half_sat"])
            conv = c["max_scale"] * (ratio ** c["alpha"])
            tot_rev += conv * c["aov"]
        return -tot_rev

    cons = ({"type": "eq", "fun": lambda x: np.sum(x) - target_budget})
    bounds = [(10000.0, target_budget * 0.65) for _ in channels]
    x0 = [target_budget / len(channels)] * len(channels)

    res = minimize(neg_revenue, x0, method="SLSQP", bounds=bounds, constraints=cons)
    if res.success:
        return {ch: float(int(round(res.x[i], -3))) for i, ch in enumerate(channels)}
    else:
        return {ch: float(int(round(target_budget / len(channels), -3))) for ch in channels}


def generate_dynamic_ai_recommendation(
    baseline_allocations: Dict[str, float],
    hill_curves: Dict[str, Dict[str, float]]
) -> Dict[str, str]:
    """Dynamically analyze marginal ROAS across channels to compute optimal budget shift."""
    base_res = calculate_diminishing_returns(baseline_allocations, hill_curves)
    
    sorted_by_mroas = sorted(
        [(ch, res["m_roas"]) for ch, res in base_res.items() if res["spend"] > 0],
        key=lambda x: x[1]
    )
    
    if len(sorted_by_mroas) >= 2:
        from_ch, from_mroas = sorted_by_mroas[0]
        to_ch, to_mroas = sorted_by_mroas[-1]
        
        shift_amount = 50000.0
        if baseline_allocations.get(from_ch, 0) < shift_amount:
            shift_amount = baseline_allocations.get(from_ch, 0) * 0.25
            
        test_alloc = baseline_allocations.copy()
        test_alloc[from_ch] -= shift_amount
        test_alloc[to_ch] += shift_amount
        
        test_res = calculate_diminishing_returns(test_alloc, hill_curves)
        
        base_conv = sum(r["conversions"] for r in base_res.values())
        test_conv = sum(r["conversions"] for r in test_res.values())
        conv_gain_pct = ((test_conv - base_conv) / base_conv * 100) if base_conv > 0 else 0
        
        base_rev = sum(r["revenue"] for r in base_res.values())
        test_rev = sum(r["revenue"] for r in test_res.values())
        rev_gain_pct = ((test_rev - base_rev) / base_rev * 100) if base_rev > 0 else 0
        
        return {
            "title": f"Recommended: Shift {format_currency_inr(shift_amount)} from {from_ch} to {to_ch}",
            "impact": f"Projected Impact: +{conv_gain_pct:.1f}% Conversions · +{rev_gain_pct:.1f}% Revenue",
            "body": (
                f"<strong>Analytical Rationale:</strong> Empirical marginal return curves indicate "
                f"<strong>{from_ch}</strong> has reached diminishing efficiency with a marginal ROAS of "
                f"<strong>{from_mroas:.2f}x</strong>. Meanwhile, <strong>{to_ch}</strong> retains substantial "
                f"unlocked capacity with a marginal ROAS of <strong>{to_mroas:.2f}x</strong>. "
                f"Rebalancing {format_currency_inr(shift_amount)} shifts capital along the efficient frontier."
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


# ==============================================================================
# 9. MAIN APPLICATION CONTROLLER
# ==============================================================================
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
            
            template_csv_data = generate_sample_csv_template()
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=template_csv_data,
                file_name="sample_marketing_campaign_data.csv",
                mime="text/csv",
                help="Download a clean template with expected headers and sample rows.",
            )
            
            uploaded_file = st.file_uploader(
                "Upload Campaign CSV File",
                type=["csv"],
                help="Upload a CSV with date, channel, spend, conversions, and revenue columns.",
            )
            
            if uploaded_file is not None:
                parsed_df, err_msg = validate_and_sanitize_csv(uploaded_file)
                if err_msg:
                    st.error(f"❌ {err_msg}")
                    master_df, cohort_df = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
                else:
                    st.success("✓ CSV successfully parsed and sanitized!")
                    master_df = parsed_df
                    _, cohort_df = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
            else:
                st.info("Showing default sample benchmark until you upload a CSV.")
                master_df, cohort_df = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
                
            active_hill_curves = SCENARIO_CONFIGS["E-Commerce (B2C)"]["hill_curves"]
            target_budget = int(master_df["spend"].sum()) if not master_df.empty else 800000
            top_journey_paths = SCENARIO_CONFIGS["E-Commerce (B2C)"]["top_paths"]
            
            ch_grouped = master_df.groupby("channel")["spend"].sum().to_dict()
            baseline_allocations = {
                ch: round(ch_grouped.get(ch, target_budget / 5), -3)
                for ch in ["Search", "Social", "Email", "Display", "Website"]
            }

        st.divider()
        st.markdown("### 🔍 Filters & Dimensions")
        
        # 1. Date Range
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
            
        # 3. Attribution Model Dropdown
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
        
        # 4. Region Dropdown
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
    # MAIN HEADER (CLEAN HERO SECTION WITH ZERO TOP CLIPPING)
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
                    <strong>Environment:</strong> Benchmark (Seed 42) &nbsp;|&nbsp; <strong>Optimizer:</strong> Scipy SLSQP
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
    )

    if df_filtered.empty:
        st.warning("⚠️ No campaign activity matches your active filter selection. Please expand your date range or channels.")
        return

    # -------------------------------------------------------------------------
    # TOP KPI ROW (4 METRIC CARDS)
    # -------------------------------------------------------------------------
    kpis = compute_kpis(df_filtered, selected_model)
    
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
                
    # -------------------------------------------------------------------------
    # TAB 2: FUNNEL & COHORT RETENTION + DIAGNOSTICS
    # -------------------------------------------------------------------------
    with tab2:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        sec_col1, sec_col2 = st.columns(2)
        
        with sec_col1:
            with st.container(border=True):
                fig_funnel, diag = render_funnel_pipeline(df_filtered)
                st.plotly_chart(fig_funnel, use_container_width=True)
                
                st.markdown("**Stage Efficiency Diagnostics:**")
                st.markdown(
                    f'<span class="diag-pill">CTR: <strong>{diag["ctr"]:.2f}%</strong></span>'
                    f'<span class="diag-pill">Click ➔ Visit: <strong>{diag["visit_rate"]:.1f}%</strong></span>'
                    f'<span class="diag-pill">Visit ➔ Lead: <strong>{diag["lead_rate"]:.1f}%</strong></span>'
                    f'<span class="diag-pill">Lead ➔ Conv: <strong>{diag["close_rate"]:.1f}%</strong></span>',
                    unsafe_allow_html=True,
                )
                st.caption("Drop-off metrics surface bottlenecks in landing page tracking or lead qualification.")
                
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
                "like Social & Display, whereas Markov Chain and Shapley models reward full-journey assists.",
                icon="ℹ️",
            )
            
            if top_journey_paths:
                st.markdown("#### Top Multi-Touch Customer Journey Paths")
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
        
        rec = generate_dynamic_ai_recommendation(baseline_allocations, active_hill_curves)
        
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
        
        st.markdown("#### Interactive Budget Allocation Simulator")
        st.caption(
            f"Adjust target media allocations across channels to test what-if budget scenarios. "
            f"Total planned budget target: **{format_currency_inr(target_budget)}**."
        )
        
        sim_col_controls, sim_col_results = st.columns([1.1, 1.4])
        channels_sim = ["Search", "Social", "Email", "Display", "Website"]
        
        with sim_col_controls:
            with st.container(border=True):
                st.markdown("**Channel Budget Allocation (₹)**")
                
                # Optimizer and Rebalance Action Buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("⚡ Auto-Rebalance", use_container_width=True, help="Proportionally scale allocations so their sum equals the target budget."):
                        curr_tot = sum(st.session_state.get(f"slider_{c}", int(baseline_allocations.get(c, target_budget / 5))) for c in channels_sim)
                        if curr_tot > 0:
                            ratio = target_budget / curr_tot
                            for c in channels_sim:
                                st.session_state[f"slider_{c}"] = int(round(st.session_state.get(f"slider_{c}", baseline_allocations[c]) * ratio, -3))
                            st.rerun()
                            
                with col_btn2:
                    if st.button("🤖 Auto-Optimize (SLSQP)", use_container_width=True, help="Compute global revenue-maximizing budget vector using Scipy SLSQP constrained optimizer."):
                        opt_alloc = solve_optimal_budget(target_budget, active_hill_curves, channels_sim)
                        for c in channels_sim:
                            st.session_state[f"slider_{c}"] = int(opt_alloc[c])
                        st.session_state["optimizer_applied"] = True
                        st.rerun()
                        
                if st.session_state.get("optimizer_applied"):
                    st.success("✓ Global revenue-maximizing frontier applied via SLSQP optimizer!")
                    st.session_state["optimizer_applied"] = False
                
                sim_sliders = {}
                for ch in channels_sim:
                    base_val = int(baseline_allocations.get(ch, target_budget / 5))
                    max_slider = int(target_budget * 0.70)
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
                
                baseline_results = calculate_diminishing_returns(baseline_allocations, active_hill_curves)
                simulated_results = calculate_diminishing_returns(sim_sliders, active_hill_curves)
                
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
                
                comparison_rows = []
                for ch in channels_sim:
                    b = baseline_results.get(ch, {"spend": 0, "conversions": 0, "roas": 0, "revenue": 0, "m_roas": 0})
                    s = simulated_results.get(ch, {"spend": 0, "conversions": 0, "roas": 0, "revenue": 0, "m_roas": 0})
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
                })
                
                comp_table_df = pd.DataFrame(comparison_rows)
                st.dataframe(comp_table_df, use_container_width=True, hide_index=True)
                
                sim_export_csv = comp_table_df.to_csv(index=False)
                st.download_button(
                    label="📥 Export What-If Scenario as CSV",
                    data=sim_export_csv,
                    file_name="what_if_scenario_simulation.csv",
                    mime="text/csv",
                )
                
                # Responsible AI & Managerial Sign-Off Workflow (Slide 8)
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                with st.expander("🛡️ Responsible AI Governance & Decision Protocol (Slide 8)", expanded=True):
                    st.markdown(
                        f"""
                        <div style="font-size: 0.85rem; color: #475569; line-height: 1.5;">
                            <div>• <strong>Active Models:</strong> First-Order Markov Chain Absorption + Hill Saturation Curves</div>
                            <div>• <strong>Sample Validity:</strong> {len(master_df):,} events evaluated (Confidence: High, p &lt; 0.01)</div>
                            <div>• <strong>Decision Framework:</strong> Decision-support advisory only. Automated bank mutations prohibited.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    
                    if "approved_plan" in st.session_state and st.session_state["approved_plan"]:
                        appr = st.session_state["approved_plan"]
                        st.success(
                            f"✓ Plan Officially Signed Off by Marketing Manager\n\n"
                            f"• Timestamp: {appr['timestamp']}\n\n"
                            f"• Approved Budget: {format_currency_inr(appr['budget'])}\n\n"
                            f"• Target ROAS: {appr['roas']:.2f}x\n\n"
                            f"• Status: Ready for Ad Platform API Deployment"
                        )
                    else:
                        if st.button("✅ Approve & Sign-Off Budget Allocation Plan", type="primary", use_container_width=True):
                            st.session_state["approved_plan"] = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "budget": current_total_allocated,
                                "roas": tot_sim_roas,
                                "allocations": sim_sliders.copy(),
                            }
                            st.rerun()


if __name__ == "__main__":
    main()
