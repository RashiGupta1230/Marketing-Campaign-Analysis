"""
Unit Test Suite for Marketing Campaign Effectiveness Analysis System
Verifies:
1. Multi-scenario synthetic generation
2. Multi-touch attribution revenue conservation invariant (sum == total)
3. CSV ingestion, aliasing, and schema validation
4. Scipy SLSQP non-linear budget optimizer
5. Hill equation diminishing returns and marginal ROAS
"""

import io
import sys
import os
import unittest
import numpy as np
import pandas as pd

# Add workspace path to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
import app


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


if __name__ == "__main__":
    unittest.main()
