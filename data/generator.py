"""
Data Generation, Customer Journey Mining, and CSV Ingestion Pipelines.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import streamlit as st

from core.config import (
    CHANNEL_CAMPAIGNS,
    CHANNEL_CREATIVES,
    SCENARIO_CONFIGS,
)
from models.attribution import attach_multi_touch_attribution


def generate_synthetic_touchpoint_journeys(
    channels: List[str],
    n_journeys: int = 1200,
    seed: int = 42
) -> List[Tuple[List[str], bool]]:
    """
    Generate realistic multi-touch customer touchpoint journeys (Slide 6 schema).
    Returns list of tuples: (path_sequence, converted_bool)
    """
    np.random.seed(seed)
    journeys = []

    # Channel transition tendencies: Social/Display introduce, Search qualifies, Email closes
    first_probs = {"Social": 0.35, "Display": 0.22, "Search": 0.25, "Website": 0.10, "Email": 0.08}
    first_weights = np.array([first_probs.get(c, 0.2) for c in channels])
    first_weights = first_weights / first_weights.sum()

    for _ in range(n_journeys):
        path_len = np.random.choice([1, 2, 3, 4], p=[0.25, 0.40, 0.25, 0.10])
        first_ch = np.random.choice(channels, p=first_weights)
        path = [first_ch]

        for _ in range(path_len - 1):
            next_ch = np.random.choice(channels)
            if next_ch != path[-1]:  # No consecutive identical touches
                path.append(next_ch)

        # Multi-touch paths have higher conversion probability
        base_cvr = 0.022 * (1.0 + 0.35 * (len(path) - 1))
        if "Email" in path:
            base_cvr *= 1.4
        if "Search" in path:
            base_cvr *= 1.25

        converted = bool(np.random.random() < min(base_cvr, 0.28))
        journeys.append((path, converted))

    return journeys


@st.cache_data(show_spinner=False)
def generate_synthetic_data(
    scenario: str = "E-Commerce (B2C)",
    seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate realistic multi-channel marketing campaign data with dynamic journey-backed attribution."""
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
            camp_options = CHANNEL_CAMPAIGNS.get(ch, [f"{ch} - Campaign"])
            creat_options = CHANNEL_CREATIVES.get(ch, [f"{ch} - Creative"])

            for reg_idx, (reg, reg_weight) in enumerate(region_weights.items()):
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

                campaign = camp_options[(current_date.day + reg_idx) % len(camp_options)]
                creative_type = creat_options[(current_date.day * 2 + reg_idx) % len(creat_options)]

                records.append({
                    "date": current_date,
                    "channel": ch,
                    "campaign": campaign,
                    "creative_type": creative_type,
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

    # Generate customer journey sequences and calculate algorithmic Markov & Shapley weights
    journeys = generate_synthetic_touchpoint_journeys(channels, n_journeys=1500, seed=seed)
    df = attach_multi_touch_attribution(df, journeys=journeys)

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


def generate_sample_csv_template() -> str:
    """Generate a clean daily aggregated CSV template string for external data ingestion."""
    sample_df, _ = generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
    export_df = sample_df[[
        "date", "channel", "region", "spend", "impressions",
        "clicks", "visits", "leads", "conversions", "revenue"
    ]].head(120).copy()

    export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
    return export_df.to_csv(index=False)


def generate_sample_touchpoint_template() -> str:
    """Generate a clean sample event-level touchpoint log CSV template (Slide 6 relational schema)."""
    records = []
    channels = ["Social", "Search", "Email", "Display", "Website"]
    now = datetime.now()
    np.random.seed(42)

    for i in range(120):
        cid = f"CUST-{1000 + i}"
        n_touches = int(np.random.choice([1, 2, 3, 4], p=[0.25, 0.45, 0.20, 0.10]))
        converted = bool(np.random.random() < 0.26)
        c_rev = round(float(np.random.normal(2400, 300)), 2) if converted else 0.0

        for t_idx in range(n_touches):
            ch = str(np.random.choice(channels))
            t_cost = round(float(np.random.uniform(15, 65)), 2)
            is_last = (t_idx == n_touches - 1)
            t_date = now - timedelta(days=int(np.random.uniform(1, 90)))
            records.append({
                "touchpoint_id": f"TP-{len(records)+1:05d}",
                "customer_id": cid,
                "channel": ch,
                "timestamp": t_date.strftime("%Y-%m-%d %H:%M"),
                "cost": t_cost,
                "converted": 1 if (is_last and converted) else 0,
                "revenue": c_rev if (is_last and converted) else 0.0,
            })

    return pd.DataFrame(records).to_csv(index=False)


def validate_and_sanitize_csv(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Validate and parse uploaded CSV file.
    Supports two enterprise ingestion schemas:
    1. Event-Level Customer Touchpoint Log (Slide 6 Schema: customer_id, channel, timestamp, converted, revenue)
    2. Daily Channel-Aggregated Campaign Data (date, channel, spend, conversions, revenue)
    """
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return None, f"Could not parse CSV file: {str(e)}"

    alias_map = {
        "cost": "spend", "ad_spend": "spend", "sales": "revenue",
        "income": "revenue", "platform": "channel", "source": "channel",
        "orders": "conversions", "purchases": "conversions",
        "geo": "region", "territory": "region",
        "user_id": "customer_id", "client_id": "customer_id",
        "conversion": "converted",
    }
    df = df.rename(columns={k: v for k, v in alias_map.items() if k in df.columns})

    # Schema Detection: Check for Event-Level Customer Touchpoint Log
    if "customer_id" in df.columns and "channel" in df.columns:
        # Event-Level Touchpoint Pipeline
        if "timestamp" in df.columns:
            df["date"] = pd.to_datetime(df["timestamp"], errors="coerce")
        elif "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        else:
            df["date"] = pd.to_datetime(datetime.now().date())

        df = df.dropna(subset=["customer_id", "channel", "date"])
        df = df.sort_values(by=["customer_id", "date"])

        if "spend" not in df.columns:
            df["spend"] = 25.0
        if "converted" not in df.columns:
            df["converted"] = 0
        if "revenue" not in df.columns:
            df["revenue"] = 0.0

        # Extract true empirical customer journeys
        journeys: List[Tuple[List[str], bool]] = []
        for _, group in df.groupby("customer_id"):
            path = group["channel"].tolist()
            converted = bool((group["converted"].sum() > 0) or (group["revenue"].sum() > 0))
            journeys.append((path, converted))

        # Aggregate event records to daily channel level for visualization
        df["day"] = df["date"].dt.date
        agg_df = df.groupby(["day", "channel"]).agg(
            spend=("spend", "sum"),
            conversions=("converted", "sum"),
            revenue=("revenue", "sum"),
        ).reset_index()

        agg_df = agg_df.rename(columns={"day": "date"})
        agg_df["date"] = pd.to_datetime(agg_df["date"])
        agg_df["region"] = "National"
        agg_df["campaign"] = agg_df["channel"] + " - Main Campaign"
        agg_df["creative_type"] = agg_df["channel"] + " - Standard Creative"
        agg_df["clicks"] = (agg_df["spend"] / 18.0).astype(int).clip(lower=1)
        agg_df["impressions"] = (agg_df["clicks"] * 32).astype(int)
        agg_df["visits"] = (agg_df["clicks"] * 0.90).astype(int)
        agg_df["leads"] = (agg_df["visits"] * 0.20).astype(int)

        # Attach multi-touch attribution directly from real customer journeys
        agg_df = attach_multi_touch_attribution(agg_df, journeys=journeys)
        agg_df.attrs["is_event_level"] = True
        agg_df.attrs["n_journeys"] = len(journeys)
        return agg_df, None

    # Fallback to Daily Channel-Aggregated Ingestion
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
    if "campaign" not in df.columns:
        df["campaign"] = df["channel"] + " - Main Campaign"
    if "creative_type" not in df.columns:
        df["creative_type"] = df["channel"] + " - Standard Creative"
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

    # Attach attribution with resilient dynamic handling
    channels = df["channel"].dropna().unique().tolist()
    journeys = generate_synthetic_touchpoint_journeys(channels, n_journeys=800, seed=42)
    df = attach_multi_touch_attribution(df, journeys=journeys)
    df.attrs["is_event_level"] = False
    return df, None
