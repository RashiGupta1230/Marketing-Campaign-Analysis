"""
Core Configuration & Industry Scenario Calibration Parameters.
"""

from typing import Any, Dict

# Executive Color Palette Tokens
COLOR_PRIMARY = "#0F172A"       # Deep Slate 900
COLOR_SECONDARY = "#0D9488"     # Teal 600
COLOR_MUTED_GREY = "#64748B"    # Slate 500
COLOR_LIGHT_BG = "#F8FAFC"      # Slate 50
COLOR_CARD_BG = "#FFFFFF"       # Pure Card White
COLOR_BORDER = "#E2E8F0"        # Slate 200
COLOR_GRID = "#F1F5F9"          # Slate 100

# Channel-to-Campaign and Creative Asset Taxonomy (Slide 4 & Slide 6 Relational Hierarchy)
CHANNEL_CAMPAIGNS = {
    "Search": ["Brand Protection", "High-Intent Generic", "Competitor Conquest"],
    "Social": ["Top-Funnel Video", "Product Showcase Carousel", "Retargeting Catalog"],
    "Email": ["Subscriber Welcome Flow", "Abandoned Cart Recovery", "Weekly VIP Digest"],
    "Display": ["Programmatic Awareness", "Dynamic Retargeting", "Affiliate Network"],
    "Website": ["Direct Organic", "SEO Landing Pages", "Partner Referrals"],
}

CHANNEL_CREATIVES = {
    "Search": ["Responsive Search Ad", "Sitelink Extension Ad", "Exact Match Text"],
    "Social": ["Short-Form Video (9:16)", "Carousel Showcase (1:1)", "Static High-Impact Banner"],
    "Email": ["HTML Template Promo", "Personalized Text Email", "Flash Sale Countdown"],
    "Display": ["Medium Rectangle (300x250)", "Leaderboard (728x90)", "Half Page (300x600)"],
    "Website": ["Homepage Hero Banner", "Pricing Table CTA", "Blog In-Line Form"],
}

SCENARIO_CONFIGS: Dict[str, Dict[str, Any]] = {
    "E-Commerce (B2C)": {
        "description": "High transaction volume, low AOV (₹2,200), impulse buying, heavy Social & Search influence.",
        "target_budget": 800000,
        "gross_margin_pct": 0.65,
        "new_customer_rate": 0.68,
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
        "gross_margin_pct": 0.85,
        "new_customer_rate": 0.78,
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
        "gross_margin_pct": 0.72,
        "new_customer_rate": 0.70,
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
