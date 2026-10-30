"""
Executive Light Theme Styling Tokens and CSS Injector.
"""

import streamlit as st


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
