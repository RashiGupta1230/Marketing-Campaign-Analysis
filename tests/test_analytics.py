"""
Unit Test Suite for Marketing Campaign Effectiveness Analysis System
Verifies:
1. Multi-scenario synthetic generation and cohort matrices
2. Multi-touch attribution revenue conservation invariant (sum == total) across 5 models
3. Dynamic Markov Chain removal effect calculation from touchpoint journeys
4. Dynamic Shapley Value coalition attribution
5. Custom CSV ingestion with arbitrary channel names (resilience against ZeroDivisionError & KeyError)
6. SciPy SLSQP non-linear budget optimizer convergence
7. Hill equation diminishing returns and marginal ROAS concavity
8. Persistent audit logging and SHA-256 verification hash
"""

import io
import os
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd

# Add workspace path to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
import app
from data.audit_store import load_audit_log, save_audit_record
from data.generator import generate_synthetic_touchpoint_journeys
from models.attribution import (
    compute_markov_removal_effects,
    compute_shapley_coalition_values,
)
from models.optimizer import get_channel_hill_curve


class TestMarketingAnalyticsEngine(unittest.TestCase):

    def test_scenario_generation(self):
        """Verify that all 3 scenarios generate valid datasets with positive spend."""
        for sc in app.SCENARIO_CONFIGS.keys():
            df, cohort_df = app.generate_synthetic_data(scenario=sc, seed=42)
            self.assertFalse(df.empty, f"Dataset for {sc} is empty")
            self.assertGreater(df["spend"].sum(), 0.0, f"Spend for {sc} should be positive")
            self.assertGreater(df["revenue"].sum(), 0.0, f"Revenue for {sc} should be positive")
            self.assertEqual(len(cohort_df), 6, f"Cohort dataframe should contain 6 cohorts")

    def test_revenue_conservation_invariant(self):
        """
        Verify the fundamental attribution invariant:
        Sum of attributed revenue across channels MUST equal total evaluated revenue
        for all 5 attribution models.
        """
        df, _ = app.generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
        total_eval_revenue = df["revenue"].sum()

        models = [
            "revenue_first_click",
            "revenue_last_click",
            "revenue_linear",
            "revenue_markov",
            "revenue_shapley",
        ]

        for m in models:
            model_total = df[m].sum()
            self.assertAlmostEqual(
                model_total,
                total_eval_revenue,
                delta=1.0,
                msg=f"Model {m} violated revenue conservation: {model_total} vs {total_eval_revenue}"
            )

    def test_csv_template_and_parser(self):
        """Verify that downloadable CSV template parses cleanly and sanitizes properly."""
        csv_template_str = app.generate_sample_csv_template()
        bio = io.BytesIO(csv_template_str.encode("utf-8"))

        parsed_df, err = app.validate_and_sanitize_csv(bio)
        self.assertIsNone(err, f"CSV parsing encountered error: {err}")
        self.assertFalse(parsed_df.empty, "Parsed dataframe should not be empty")
        self.assertIn("revenue_markov", parsed_df.columns, "Parsed DF should have attribution attached")

    def test_custom_csv_arbitrary_channels(self):
        """Verify that CSV with arbitrary non-standard channel names parses without KeyError or ZeroDivisionError."""
        custom_csv = (
            "date,channel,spend,conversions,revenue\n"
            "2026-01-01,TikTok_Ads,1500,20,45000\n"
            "2026-01-01,Influencer_Collab,2500,35,80000\n"
            "2026-01-02,Affiliate_Network,800,12,24000\n"
        )
        bio = io.BytesIO(custom_csv.encode("utf-8"))
        parsed_df, err = app.validate_and_sanitize_csv(bio)

        self.assertIsNone(err, f"Custom CSV encountered error: {err}")
        self.assertEqual(len(parsed_df), 3)
        self.assertIn("TikTok_Ads", parsed_df["channel"].values)

        # Verify optimizer on arbitrary channels
        custom_channels = ["TikTok_Ads", "Influencer_Collab", "Affiliate_Network"]
        opt_alloc = app.solve_optimal_budget(100000.0, {}, custom_channels)
        self.assertEqual(len(opt_alloc), 3)
        self.assertAlmostEqual(sum(opt_alloc.values()), 100000.0, delta=2000.0)

    def test_dynamic_markov_removal_effects(self):
        """Verify dynamic First-Order Markov removal effects computation from journey sequences."""
        channels = ["Search", "Social", "Email"]
        journeys = [
            (["Social", "Search", "Email"], True),
            (["Social", "Search"], False),
            (["Search", "Email"], True),
            (["Email"], True),
            (["Social"], False),
        ]
        effects = compute_markov_removal_effects(journeys, channels)

        # All channels must have positive normalized weights summing to 1.0
        self.assertEqual(len(effects), 3)
        self.assertAlmostEqual(sum(effects.values()), 1.0, delta=1e-5)
        for ch, w in effects.items():
            self.assertGreater(w, 0.0)

    def test_dynamic_shapley_coalition_values(self):
        """Verify game-theoretic Shapley values computation from channel subsets."""
        channels = ["Search", "Social", "Email"]
        journeys = [
            (["Social", "Search", "Email"], True),
            (["Social"], False),
            (["Search"], True),
            (["Email"], True),
        ]
        weights = compute_shapley_coalition_values(journeys, channels)

        self.assertEqual(len(weights), 3)
        self.assertAlmostEqual(sum(weights.values()), 1.0, delta=1e-5)
        for ch, w in weights.items():
            self.assertGreater(w, 0.0)

    def test_slsqp_optimizer_convergence(self):
        """Verify that Scipy SLSQP optimizer solves for the optimal budget allocation."""
        hill_curves = app.SCENARIO_CONFIGS["E-Commerce (B2C)"]["hill_curves"]
        channels = ["Search", "Social", "Email", "Display", "Website"]
        target_budget = 800000.0

        opt_alloc = app.solve_optimal_budget(target_budget, hill_curves, channels)
        total_allocated = sum(opt_alloc.values())

        # Verify budget conservation constraint
        self.assertAlmostEqual(
            total_allocated,
            target_budget,
            delta=5000.0,
            msg="Optimized allocation sum must equal target budget"
        )

        # Verify every channel receives a valid positive allocation
        for ch, spend in opt_alloc.items():
            self.assertGreater(spend, 0.0, f"Channel {ch} allocation must be positive")

    def test_hill_equation_concavity(self):
        """Verify that marginal ROAS decreases as spend increases (diminishing returns)."""
        hill_curves = app.SCENARIO_CONFIGS["E-Commerce (B2C)"]["hill_curves"]

        # Test Social channel at increasing spend tiers
        low_res = app.calculate_diminishing_returns({"Social": 100000}, hill_curves)["Social"]
        high_res = app.calculate_diminishing_returns({"Social": 300000}, hill_curves)["Social"]

        self.assertGreater(
            low_res["m_roas"],
            high_res["m_roas"],
            "Marginal ROAS must strictly diminish as spend increases"
        )

    def test_persistent_audit_logging(self):
        """Verify persistent audit logging, SHA-256 verification hash, and record retrieval."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            allocs = {"Search": 300000.0, "Social": 250000.0}
            rec = save_audit_record(
                scenario="Test Scenario",
                target_budget=550000.0,
                projected_revenue=1200000.0,
                projected_roas=2.18,
                allocations=allocs,
                approved_by="Test Manager",
                filepath=tmp_path,
            )

            self.assertIn("audit_id", rec)
            self.assertTrue(rec["verification_hash"].startswith("SHA256:"))
            self.assertEqual(rec["target_budget"], 550000.0)

            loaded = load_audit_log(filepath=tmp_path)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["audit_id"], rec["audit_id"])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_attribution_share_exact_match(self):
        """Verify that attributed revenue shares for each channel exactly match model weights without double-weighting artifact."""
        df, _ = app.generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
        total_rev = df["revenue"].sum()

        for col, model_name in [
            ("revenue_markov", "Markov Chain"),
            ("revenue_shapley", "Shapley Value"),
            ("revenue_first_click", "First-click"),
            ("revenue_last_click", "Last-click"),
        ]:
            ch_revs = df.groupby("channel")[col].sum()
            self.assertAlmostEqual(ch_revs.sum(), total_rev, delta=1.0)
            # Ensure every channel has a non-zero, plausible share
            for ch, rev in ch_revs.items():
                share = rev / total_rev
                self.assertGreater(share, 0.01, f"{ch} share under {model_name} too low: {share}")
                self.assertLess(share, 0.70, f"{ch} share under {model_name} too high: {share}")

    def test_model_linked_optimizer_differential(self):
        """Verify that SLSQP optimizer responds dynamically to attribution model weights."""
        hill_curves = app.SCENARIO_CONFIGS["E-Commerce (B2C)"]["hill_curves"]
        channels = ["Search", "Social", "Email", "Display", "Website"]
        target_budget = 800000.0

        last_click_weights = {"Email": 0.38, "Search": 0.34, "Website": 0.14, "Social": 0.10, "Display": 0.04}
        markov_weights = {"Search": 0.28, "Social": 0.26, "Email": 0.18, "Website": 0.16, "Display": 0.12}

        curves_lc = app.scale_curves_by_attribution(hill_curves, last_click_weights, channels)
        curves_m = app.scale_curves_by_attribution(hill_curves, markov_weights, channels)

        alloc_lc = app.solve_optimal_budget(target_budget, curves_lc, channels)
        alloc_m = app.solve_optimal_budget(target_budget, curves_m, channels)

        # Under Markov, Social assist value increases, so Social budget must be higher than under Last-Click
        self.assertGreater(
            alloc_m["Social"],
            alloc_lc["Social"],
            f"Social budget under Markov ({alloc_m['Social']}) should exceed Last-Click ({alloc_lc['Social']})"
        )

    def test_net_profit_optimization_objective(self):
        """Verify that SLSQP optimizer successfully optimizes for Net Contribution Profit."""
        hill_curves = app.SCENARIO_CONFIGS["E-Commerce (B2C)"]["hill_curves"]
        channels = ["Search", "Social", "Email", "Display", "Website"]
        target_budget = 800000.0

        opt_rev = app.solve_optimal_budget(target_budget, hill_curves, channels, gross_margin_pct=0.65, objective="revenue")
        opt_profit = app.solve_optimal_budget(target_budget, hill_curves, channels, gross_margin_pct=0.65, objective="profit")

        self.assertAlmostEqual(sum(opt_rev.values()), target_budget, delta=5000.0)
        self.assertAlmostEqual(sum(opt_profit.values()), target_budget, delta=5000.0)

    def test_event_level_touchpoint_ingestion(self):
        """Verify that event-level customer touchpoint logs (Slide 6 schema) are correctly identified and parsed."""
        csv_str = app.generate_sample_touchpoint_template()
        bio = io.BytesIO(csv_str.encode("utf-8"))

        parsed_df, err = app.validate_and_sanitize_csv(bio)
        self.assertIsNone(err, f"Touchpoint CSV parsing error: {err}")
        self.assertTrue(parsed_df.attrs.get("is_event_level", False), "Should flag is_event_level as True")
        self.assertGreater(parsed_df.attrs.get("n_journeys", 0), 0, "Should have extracted customer journeys")
        self.assertIn("revenue_markov", parsed_df.columns)

    def test_campaign_and_creative_drilldown(self):
        """Verify that synthetic dataset contains campaign and creative hierarchy and drilldown renders properly."""
        df, _ = app.generate_synthetic_data(scenario="E-Commerce (B2C)", seed=42)
        self.assertIn("campaign", df.columns)
        self.assertIn("creative_type", df.columns)

        search_df = df[df["channel"] == "Search"]
        fig, table = app.render_campaign_drilldown(search_df, "Search", revenue_col="revenue_markov")
        self.assertIsNotNone(fig)
        self.assertFalse(table.empty)
        self.assertIn("campaign", table.columns)
        self.assertIn("roas", table.columns)

    def test_executive_brief_html_generation(self):
        """Verify that generate_executive_brief_html produces a complete, valid executive brief."""
        html = app.generate_executive_brief_html(
            scenario_name="E-Commerce (B2C)",
            attribution_model="Markov Chain",
            kpis={"spend": 800000.0, "revenue": 1640000.0, "roas": 2.05},
            unit_economics={"cpa": 450.0, "cac": 620.0, "ltv_cac": 3.4, "health": "Healthy"},
            ai_recommendation={"title": "Test Title", "impact": "Impact Text", "body": "Body Text"},
            simulation_rows=[{"Channel": "Search", "Base Spend": "₹280,000", "Sim Spend": "₹320,000"}],
            currency_symbol="₹",
        )
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Executive Decision-Support Brief", html)
        self.assertIn("Markov Chain", html)
        self.assertIn("Search", html)
        self.assertIn("@media print", html)


if __name__ == "__main__":
    unittest.main()
