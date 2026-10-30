# Marketing Campaign Effectiveness Analysis
## Interactive ROI Decision-Support System & Multi-Touch Attribution Simulator

An applied Business Intelligence (BI) and quantitative decision-support engine developed with Python, Streamlit, Plotly, and SciPy. This system enables organizations to transition away from biased single-touch attribution heuristics (such as Last-Click) toward algorithmic, multi-touch attribution and mathematically constrained budget optimization.

---

## 1. Project Purpose

In modern digital marketing, companies allocate significant capital across diverse touchpoints (Paid Search, Social Media, Email Marketing, Display Ads, Organic Web). However, standard marketing analytics software frequently relies on oversimplified attribution models:

- **Last-Click Attribution Bias:** Gives 100% of revenue credit to the final ad clicked before checkout. This systematically undervalues awareness, brand discovery, and mid-funnel nurture channels (e.g., Social, Display, Content).
- **First-Click Attribution Bias:** Gives 100% of revenue credit to the initial ad touchpoint, ignoring the effectiveness of closing and retargeting channels.
- **Budget Misallocation:** Over-investing in bottom-of-funnel channels pushes them past their point of saturation into steep **diminishing returns**, while starving high-potential assist channels.

### The Objective
This system bridges the gap between academic attribution theory and real-world executive marketing decisions by:
1. Computing **algorithmic Multi-Touch Attribution (MTA)** using Markov Chain absorption states and Shapley cooperative game-theoretic formulations.
2. Modeling **non-linear channel saturation** via the Hill equation to derive instantaneous Marginal ROAS ($\frac{d\text{Revenue}}{d\text{Spend}}$).
3. Finding global revenue-maximizing budget allocations using **SciPy's Sequential Least Squares Programming (SLSQP)** constrained optimizer.
4. Providing a **governed Human-in-the-Loop decision framework** requiring managerial review and verification before capital reallocation.

---

## 2. What Does It Do?

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                APPLICATION ARCHITECTURE                               │
├──────────────────────────┬───────────────────────────┬─────────────────────────────────┤
│    1. Ingestion Engine   │   2. Analytics Engine     │     3. Decision Support         │
│  • Industry Benchmarks   │  • 5 Attribution Models   │  • Hill Diminishing Returns     │
│    (B2C, SaaS, EdTech)   │  • 5-Stage Funnel Health  │  • Marginal ROAS Calculation    │
│  • Custom CSV Uploader   │  • Cohort LTV & Retention │  • SciPy SLSQP Budget Optimizer │
│  • Schema Auto-Remap     │  • Revenue Invariant Gate │  • Managerial Sign-Off & Audit  │
│  • Campaign/Creative     │  • Campaign Drill-Down    │  • Executive Brief HTML Export  │
└──────────────────────────┴───────────────────────────┴─────────────────────────────────┘
```

The system comprises four primary analytical modules in [`app.py`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/app.py):

### A. Flexible Data Ingestion & Sanitization
- **Benchmark Presets:** Includes three pre-calibrated industry profiles:
  - **E-Commerce (B2C):** High transaction volume, modest Average Order Value (AOV ₹2,200), short sales cycle.
  - **B2B Enterprise SaaS:** High contract value (AOV ₹75,000), multi-stage demo qualification, long sales cycle.
  - **EdTech & Courses:** Mid-tier price point (AOV ₹18,500), webinar and counselor lead generation funnel.
- **Proprietary CSV Ingestion:** Ingest custom campaign logs with an automated aliasing and validation layer (`cost` $\to$ `spend`, `sales` $\to$ `revenue`, `orders` $\to$ `conversions`) plus a downloadable sample CSV template.
- **Campaign & Creative Hierarchy:** Synthetic records include `campaign` and `creative_type` columns enabling sub-channel drill-down analysis.

### B. High-Level KPI & Performance Dashboard
- **Real-Time Financial Metrics:** Total Media Spend, Attributed Revenue, Conversions, Blended CPA (Cost Per Acquisition), and ROAS / Net ROI ($\text{ROI\%} = (\text{ROAS} - 1) \times 100$).
- **Granular Filtering:** Filter dynamically by multi-select channels, custom date windows, geographic territories, and campaign.
- **Multi-Currency Display:** Switch between ₹ INR, $ USD, € EUR, and £ GBP via the sidebar currency selector.

### C. Multi-Touch Attribution Engine
Evaluates customer touchpoints simultaneously across 5 distinct models while strictly preserving the **Attribution Revenue Invariant** ($\sum \text{Attributed Revenue} = \text{Total Evaluated Revenue}$):
1. **First-Click:** 100% credit to initial touchpoint (measures discovery).
2. **Last-Click:** 100% credit to final touchpoint (measures conversion closing).
3. **Linear:** Equal weight divided across all recorded touchpoints.
4. **Markov Chain:** Calculates channel removal effects using state transition absorption probabilities to isolate each channel's true contribution.
5. **Shapley Value:** Cooperative game-theoretic algorithm computing the marginal contribution of each channel across all possible channel coalitions.
- **Customer Journey Path Analysis:** Analyzes top multi-touch paths (e.g., `Social ➔ Search ➔ Email`) with conversion rates and assist roles.
- **Campaign & Creative Drill-Down:** Grouped bar chart comparing campaign and creative asset performance within a selected channel (Revenue, Spend, Conversions).

### D. Funnel Drop-Off Diagnostics & Cohort LTV
- **5-Stage Macro Funnel:** Tracks drop-off across Impressions $\to$ Clicks $\to$ Visits $\to$ Leads $\to$ Conversions.
- **Diagnostic Efficiency Badges:** Surfaces real-time operational ratios (CTR, Click-to-Visit Rate, Visit-to-Lead Rate, Lead-to-Conversion Close Rate).
- **Cohort Retention Matrix:** Heatmap with an interactive toggle between **Retention Rate (%)** decay and **Cumulative Lifetime Value (₹ LTV)** over months 0–3.

### E. AI What-If Simulator & Constrained Optimizer
- **Hill Equation Saturation Modeling:** Models diminishing returns where incremental revenue decelerates as spend increases. Owned channels (Website, Email) include an organic baseline demand floor so zero paid spend never implies zero revenue.
- **Marginal ROAS ($\text{mROAS}$):** Instantaneous derivative showing expected return for the next ₹1 invested in each channel.
- **SciPy SLSQP Optimizer:** Automatically solves for the global revenue-maximizing spend vector subject to a fixed budget ceiling ($\sum \text{Spend}_i = \text{Target Budget}$). Supports both *Maximize Gross Revenue* and *Maximize Net Contribution Profit* objectives.
- **Proportionate Rebalancer:** One-click scalar normalization across budget sliders.
- **Responsible AI Governance & Sign-Off:** Audit trail logging plan approvals with timestamps, target ROAS, and managerial confirmation.
- **Executive Brief Export:** Print-ready HTML/PDF export of the signed-off plan with KPI grid, AI recommendation, simulation comparison table, governance badge, and audit trail.

---

## 3. For Whom Is This Built?

| Target Audience | Primary Use Case & Role |
| :--- | :--- |
| **Chief Marketing Officers (CMOs) & VP of Growth** | Defend media budget allocations with quantitative proof of full-funnel channel ROI; eliminate wasteful ad spend in saturated channels. |
| **Performance Marketers & Media Planners** | Shift budget from low-marginal-return channels to underfunded high-assist channels; run what-if scenario simulations before committing ad spend. |
| **Marketing Data Analysts & BI Engineers** | Replace static spreadsheets with mathematically verified attribution models (Markov, Shapley) and automated CSV validation pipelines. |
| **Academic Researchers & Students** | Research and study cooperative game theory, Markov chains, and non-linear optimization applied to digital media economics. |

---

## 4. How Does It Benefit Organizations?

### 1. Eliminates Wasted Media Spend
Instead of overspending on bottom-funnel channels where Marginal ROAS has dropped below 1.0x, marketing teams can pinpoint the saturation inflection point and halt unprofitable budget increases.

### 2. Fairly Values Brand & Top-of-Funnel Channels
Brand awareness campaigns (Display, Social video) rarely receive credit under Last-Click models. By quantifying assist and removal effects via Markov and Shapley models, executive leadership can see the true revenue impact of early-stage discovery.

### 3. Provides Mathematical Rigor Over Intuition
Rather than guessing budget splits across ad channels, the built-in SciPy SLSQP non-linear optimizer calculates the mathematically optimal budget distribution to maximize top-line revenue under a constrained budget.

### 4. Mitigates Risk Through AI Governance
The system functions as a **decision-support advisory engine** rather than an autonomous actor. It enforces statistical sample size checks ($p < 0.01$) and requires explicit managerial sign-off, preventing automated or unreviewed modifications to media accounts.

---

## 5. Technology Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Interactive Visualizations:** [Plotly Graph Objects](https://plotly.com/python/)
- **Numerical Optimization:** [SciPy](https://scipy.org/) (`scipy.optimize.minimize` with SLSQP)
- **Design System:** Custom CSS executive light theme (`#0F172A` Slate & `#0D9488` Teal palette) locked via [`.streamlit/config.toml`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/.streamlit/config.toml)
- **Testing:** Python `unittest` suite in [`tests/test_analytics.py`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/tests/test_analytics.py)

---

## 6. Installation & Execution

### Prerequisites
- Python 3.9+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/RashiGupta1230/Marketing-Campaign-Analysis.git
cd "Marketing Campaign Analysis"

# Install dependencies
pip install -r requirements.txt
```

### Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### Run Unit Tests
```bash
python -m unittest discover tests -v
```
All 15 unit tests verify:
- Scenario generation for all 3 industry presets
- Revenue conservation invariant ($\sum \text{Attributed Revenue} = \text{Total Revenue}$)
- Exact match between channel attributed revenue shares and model weights without double-weighting
- CSV ingestion and column alias remapping for daily aggregated records
- Event-level touchpoint log ingestion (Slide 6 relational schema) extracting empirical customer journeys, including `campaign` and `creative_type` columns
- Custom CSV ingestion with arbitrary channel resilience (no `ZeroDivisionError` or `KeyError`)
- Dynamic First-Order Markov Chain transition absorption matrix and removal effects
- Dynamic Shapley Value coalition game-theoretic attribution
- Model-linked dynamic budget optimizer (SLSQP responds dynamically to active attribution model)
- Net Contribution Profit optimization vs. Top-line Gross Revenue optimization
- Scipy SLSQP non-linear optimizer convergence under budget conservation constraints
- Hill equation concavity and diminishing Marginal ROAS
- Persistent audit ledger with SHA-256 integrity verification
- Campaign & creative asset drill-down hierarchy rendering (grouped bar by campaign and creative type)
- Executive Brief HTML generation with sign-off badge, AI recommendation, and audit trail footer
