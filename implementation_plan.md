# Implementation Plan: Marketing Campaign Effectiveness Decision-Support System
## Production-Grade Engineering & Business Intelligence Roadmap

**Document Version:** 4.0.0  
**Authors:** Senior Development Lead & Senior Marketing Business Analyst  
**Target Codebase:** [`app.py`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/app.py) | [`models/attribution.py`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/models/attribution.py) | [`models/optimizer.py`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/models/optimizer.py) | [`tests/test_analytics.py`](file:///e:/PROJECTS/Marketing%20Campaign%20Analysis/tests/test_analytics.py)  
**Status:** **Completed & Verified (100% Pass Rate Across 15 Automated Tests)**

---

## 1. Executive Summary & Objective

Based on our comprehensive dual-lens technical and business audit, this implementation plan outlines the exact roadmap to resolve existing technical issues and elevate the platform from a presentation prototype (75% functional completion) to an enterprise-grade Decision-Support System (100% production readiness).

### Core Problem Areas Addressed
1. **Critical Bug Fixes:** Eliminate session-state slider desynchronization upon scenario switching, approval badge state leakage, and custom CSV arbitrary channel crashes (`ZeroDivisionError` & `KeyError`).
2. **Algorithmic Authenticity:** Transition attribution from static dictionary weights to a **dynamic First-Order Markov Chain transition absorption matrix** and **Shapley coalition calculator** calculated from touchpoint journey event logs (Slide 6 & Slide 8).
3. **Executive Governance:** Implement persistent file-based audit logging for managerial approvals and add CAC (Customer Acquisition Cost) vs. Blended CPA metrics.
4. **Codebase Maintainability:** Refactor the 1,600+ line monolithic `app.py` into clean, decoupled domain modules (`models/`, `views/`, `data/`, `app.py`).

---

## 2. Phased Architecture & Work Breakdown Structure (WBS)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               PHASED IMPLEMENTATION ROADMAP                             │
├─────────────────────────┬───────────────────────────┬──────────────────────────────────┤
│ Phase 1: Critical Fixes │ Phase 2: Dynamic Engine   │ Phase 3: Governance & Reporting  │
│ • Scenario Switch State │ • Event Touchpoint Model  │ • Persistent Audit Ledger        │
│ • Sign-Off Isolation    │ • Dynamic Markov Matrix   │ • CAC vs CPA Distinction         │
│ • Custom CSV Immunity   │ • Shapley Coalition Math  │ • Executive Report Exporter      │
├─────────────────────────┴───────────────────────────┴──────────────────────────────────┤
│ Phase 4: Modular Refactoring & Full Test Suite (100% Passing Coverage)                 │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Phase Specifications

### Phase 1: Critical Bug Fixes & Session State Integrity
*Estimated Effort: 1 Day | Priority: Critical*

- [x] **1.1 Scenario Switch State Listener (`active_scenario` tracking)**
  - **Issue:** Changing `st.selectbox("Industry Business Model")` fails to update `st.session_state[f"slider_{ch}"]`, leaving sliders frozen at the previous scenario's allocations.
  - **Remediation:** Track `st.session_state["previous_scenario"]`. If `current_scenario != previous_scenario`:
    - Overwrite all channel slider values with the new scenario's `default_allocations`.
    - Reset the scenario budget difference tracker.
    - Clear any approval sign-off badge that belonged to the previous scenario.

- [x] **1.2 Approval Sign-Off Scope & Isolation**
  - **Issue:** Signing off on E-Commerce keeps the green approved banner active even when switching to B2B SaaS or uploading custom data.
  - **Remediation:** Key sign-offs by scenario name and data fingerprint hash (`st.session_state["approved_plans"][scenario_key]`).

- [x] **1.3 Custom CSV Channel Resilience (`KeyError` & `ZeroDivisionError` Prevention)**
  - **Issue:** Ingestion of CSVs with non-standard channel names (e.g., `TikTok`, `Google_Search`, `Affiliates`) causes `ZeroDivisionError` in attribution weighting and `KeyError` in the Hill optimizer.
  - **Remediation:**
    - In `compute_attribution_weights`, dynamically handle unknown channels by assigning an empirical prior or uniform baseline.
    - In `solve_optimal_budget` and `calculate_diminishing_returns`, automatically generate parameterized Hill curves for custom channels derived from observed historical CAC and AOV if not already in dictionary.

---

### Phase 2: Dynamic Attribution Engine & Customer Journey Mining
*Estimated Effort: 2 Days | Priority: High (Slide 6 & Slide 8 Alignment)*

- [x] **2.1 Event-Level Touchpoint Generator (Slide 6 Schema)**
  - Generate a relational synthetic touchpoint log dataset alongside the daily aggregated dataset:
    - `touchpoint_id`, `customer_id`, `channel`, `timestamp`, `cost`, `converted`, `revenue`.
  - Display actual path length distributions and multi-touch journey sequences.

- [x] **2.2 Algorithmic First-Order Markov Chain Transition Engine**
  - Compute the empirical transition matrix:
    $$P_{ij} = \frac{N_{i \to j}}{\sum_k N_{i \to k}}$$
    including `(start)` and `(conversion)` absorbing states.
  - Implement dynamic **Removal Effect** calculation:
    $$R(c) = \frac{P(\text{Conversion} \mid \text{Full Graph}) - P(\text{Conversion} \mid \text{Graph without } c)}{P(\text{Conversion} \mid \text{Full Graph})}$$
  - Normalize removal effects across active channels to guarantee the Attribution Revenue Invariant:
    $$\sum_{c} \text{Attributed Revenue}_c = \text{Total Revenue}$$

- [x] **2.3 Dynamic Shapley Value Attribution**
  - Evaluate characteristic function $v(S)$ representing conversion probability for all channel subsets $S \subseteq N$.
  - Calculate exact marginal contributions:
    $$\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} (v(S \cup \{i\}) - v(S))$$

---

### Phase 3: Executive Reporting, CAC Analytics & Governance
*Estimated Effort: 1.5 Days | Priority: Medium-High*

- [x] **3.1 CAC vs. Blended CPA Separation**
  - Surface distinct metrics on top KPI row:
    - **Blended CPA:** $\frac{\text{Total Spend}}{\text{Total Orders}}$ (all transactions).
    - **Estimated CAC:** $\frac{\text{Acquisition Media Spend}}{\text{New Customer Conversions}}$ (isolated using Month-0 cohort signups).
    - **LTV / CAC Ratio:** $\frac{\text{Estimated 3-Month LTV}}{\text{CAC}}$ with traffic-light health indicator ($> 3.0\times$ healthy).

- [x] **3.2 Persistent Audit Logging (Slide 4 & Slide 8 Governance)**
  - Replace ephemeral session state approval with file-persisted JSON ledger (`data/audit_log.json`).
  - Log structure:
    ```json
    {
      "audit_id": "AUD-2026-10-30-001",
      "timestamp": "2026-10-30 19:15:00",
      "scenario": "E-Commerce (B2C)",
      "approved_by": "Marketing Manager",
      "target_budget": 800000,
      "projected_revenue": 1640000,
      "projected_roas": 2.05,
      "channel_splits": {"Search": 280000, "Social": 240000, ...},
      "verification_hash": "sha256_..."
    }
    ```
  - Display full historical approval ledger in an expandable audit drawer.

- [x] **3.3 One-Click Executive Summary PDF/HTML Export**
  - Add an "Export Executive Brief" button generating a clean, printable HTML/PDF report summarizing active allocations, attribution model deltas, and projected ROAS.

---

### Phase 4: Modular Architecture Refactoring
*Estimated Effort: 1 Day | Priority: High (Clean Architecture)*

- [x] **4.1 Package Modularization**
  Refactor single 1,605-line `app.py` into a clean package structure while maintaining 100% backward compatibility:
  ```
  Marketing Campaign Analysis/
  ├── core/
  │   ├── __init__.py
  │   ├── config.py             # Scenarios, color tokens, constants
  │   ├── styles.py             # Executive Light CSS styling
  ├── models/
  │   ├── __init__.py
  │   ├── attribution.py        # Markov chain, Shapley, heuristics
  │   ├── optimizer.py          # Hill equation, SLSQP solver, marginal ROAS
  │   └── cohorts.py            # Cohort retention & LTV projection
  ├── data/
  │   ├── __init__.py
  │   ├── generator.py          # Synthetic benchmarks & journey generator
  │   ├── validator.py          # CSV schema validation & remapping
  │   └── audit_store.py        # Persistent JSON audit logging
  ├── views/
  │   ├── __init__.py
  │   ├── charts.py             # Plotly figures (ROAS, Trends, Funnel, Heatmap)
  │   └── components.py         # KPI cards, Recommendation cards, Badges
  ├── app.py                    # Streamlit execution controller (< 200 lines)
  └── tests/
      └── test_analytics.py     # Comprehensive automated test suite
  ```

---

### Phase 5: Verification, Quality Assurance & Test Suite Expansion
*Estimated Effort: 0.5 Days | Priority: Critical*

- [x] **5.1 Expanded Automated Unit Tests**
  - Test 1: Scenario switching state reset verification.
  - Test 2: Custom CSV with arbitrary channels (ensures no `KeyError` or `ZeroDivisionError`).
  - Test 3: Dynamic Markov transition absorption matrix convergence.
  - Test 4: Shapley value revenue conservation invariant across all scenarios.
  - Test 5: Persistent audit ledger write and read integrity.
  - Test 6: SLSQP budget optimizer constraints ($\sum \text{Spend}_i = \text{Target Budget}$).

---

### Phase 6: Executive Commercial Hardening & Business Perspective Remediation
*Status: Completed & 100% Verified*

- [x] **6.1 Elimination of Attribution Double-Weighting Artifact**
  - In `attach_multi_touch_attribution`, channel attributed revenue is directly assigned as $\text{Rev}_c = w_c \times \text{Total Revenue}$ distributed across channel rows. Guarantees that grouped channel revenue divided by total revenue matches the model's weight vector exactly.
- [x] **6.2 Dynamic Journey Extraction for First-Click & Last-Click**
  - In `compute_attribution_weights`, First-Click and Last-Click now dynamically tally the actual converted paths (`path[0]` and `path[-1]`) from customer journey event logs instead of falling back to static percentage dictionaries.
- [x] **6.3 Model-Linked Saturation Scaling & Optimizer Coupling**
  - Implemented `scale_curves_by_attribution` in `models/optimizer.py`. The Hill equation capacity $V_{\max}$ (`max_scale`) dynamically scales with the active attribution model's channel weights. Switching from Last-Click to Markov Chain directly increases Social/assist channel capacity and re-allocates budget towards assist channels.
- [x] **6.4 Executive Financial Realism: Gross Margin % & Net Profit Contribution Optimizer**
  - Added a Product Gross Margin % slider (COGS calibration) and an SLSQP objective toggle:
    - *Maximize Gross Revenue (Top-Line ROAS)*
    - *Maximize Net Contribution Profit* ($\sum \text{Revenue}_i \times \text{Margin} - \text{Spend}$)
  - Added Net Profit Impact and Gross Profit metrics to the simulation comparison table.
- [x] **6.5 Real Dual CSV Ingestion (Slide 6 Relational Schema)**
  - Added full support and downloadable templates for both:
    1. Daily Aggregated Campaign CSV (`date, channel, spend, conversions, revenue`)
    2. Event-Level Customer Touchpoint Log (`customer_id, channel, timestamp, converted, revenue`)
  - Automatically identifies event logs, extracts real user journeys, and indicates empirical vs. simulated attribution.
- [x] **6.6 Channel-Isolated Conversion Funnel Diagnostics**
  - Added a `channel_focus` selector in Tab 2 to isolate conversion funnel drop-offs channel-by-channel (CTR, Click-to-Visit, Visit-to-Lead, Lead-to-Conversion).
- [x] **6.7 Comprehensive Unit Economics**
  - Surfaced dynamic Acquisition Spend, Estimated CAC, 3-Month LTV, LTV:CAC health ratio ($>3.0\times$ healthy), and CAC Payback Period (Months) directly on the top executive KPI row.
- [x] **6.8 Statistical Rigor in Governance**
  - Replaced hardcoded string with computed conversion rate standard error $SE = \sqrt{p(1-p)/N}$, 95% confidence intervals, and statistical power claims ($p < 0.001$).

---

## 4. Implementation Schedule & Verification Gate

| Step | Milestone | Verification Gate | Success Metric |
| :---: | :--- | :--- | :--- |
| **G1** | Phase 1 Bugfixes | Switch scenarios and upload custom CSV in UI | Zero slider lag, no crash on arbitrary channels |
| **G2** | Phase 2 Dynamic Attribution | Run unit tests on Markov & Shapley | $\sum \text{Attributed} = \text{Total} \pm 1.0$, Dynamic removal effects |
| **G3** | Phase 3 Governance & CAC | Submit managerial sign-off and reload page | Sign-off persists across reloads in `audit_log.json` |
| **G4** | Phase 4 Refactoring | Run `python -m unittest discover tests -v` | 100% test pass rate across all modular components |
| **G5** | Phase 5 UI & Final Verification | Launch `streamlit run app.py` | Full end-to-end interactive simulation verified |
| **G6** | Phase 6 Business Remediation | Run `python -m unittest discover tests -v` | 100% pass across 13 tests (Model-coupled optimizer, Touchpoint CSV, Attribution accuracy) |
| **G7** | Phase 7 Creative & Reporting Enhancements | Run `python -m unittest discover tests -v` | 100% pass across 15 tests (Campaign hierarchy, Executive Brief, Owned-media baseline) |

---

## 5. Phase 7: Creative Hierarchy, Executive Reporting & Owned Media Baseline

*Estimated Effort: 1 Day | Priority: High | Status: ✅ Complete*

These enhancements address the remaining gap between the academic prototype and a production-grade CMO-facing BI tool as outlined in Slide 4, Slide 6, and Phase 3.3 of the original requirements.

- [x] **7.1 Campaign & Creative Hierarchy Drill-Down (Slide 4 / Slide 6)**
  - Added `CHANNEL_CAMPAIGNS` and `CHANNEL_CREATIVES` dicts to `core/config.py` with deterministic rotation (`(day + idx) % len(options)`) to ensure reproducible synthetic records.
  - `generate_synthetic_data` in `data/generator.py` now writes `campaign` and `creative_type` columns to every synthetic record.
  - Event-level aggregation and daily CSV fallback also inject `campaign` and `creative_type` if missing.
  - Added `render_campaign_drilldown(df, channel, ...)` to `views/charts.py` — a grouped bar chart comparing campaign and creative performance within a channel (Revenue, Spend, Conversions).
  - Exposed as an expandable "📊 Campaign & Creative Drill-Down" section in Tab 1 with a channel selector.

- [x] **7.2 Executive Brief HTML/PDF Export (Slide 4 Phase 3.3 / CMO Reporting)**
  - Added `generate_executive_brief_html(...)` to `views/charts.py` — a pure function with no Streamlit dependencies that generates a complete, self-contained HTML document suitable for print-to-PDF.
  - Sections: Executive KPI grid, AI Recommendation, Simulation Comparison Table, Governance Sign-Off Badge, Audit Trail footer.
  - Exposed as a `st.download_button` in Tab 4 alongside the existing CSV export.
  - The `audit_record` is threaded through to the HTML footer to tie the brief to a specific signed-off approval.

- [x] **7.3 Owned Media Baseline Demand Model (Website / Email Organic Floor)**
  - `get_channel_hill_curve` in `models/optimizer.py` now returns `baseline_conversions` for owned channels: Website = 12% of `max_scale`, Email = 8% of `max_scale`.
  - `calculate_diminishing_returns` adds `baseline_conversions` to the conversion total so owned channels never show zero revenue at zero paid spend — correctly modelling organic demand floor.
  - `solve_optimal_budget` objective function incorporates `baseline_conversions` to prevent the solver from misattributing owned-channel baseline lift to paid spend.

- [x] **7.4 Multi-Currency Display Selector**
  - Sidebar now includes a `st.selectbox` for Currency: ₹ (INR), $ (USD), € (EUR), £ (GBP).
  - `format_currency(value, symbol)` imported from `views/charts.py` and applied to all monetary figures in Tab 1 drill-down and Tab 4 executive brief.
  - INR (₹) remains the primary benchmark currency; selector affects display layer only.

- [x] **7.5 Campaign Filter Dimension**
  - Sidebar includes a `st.multiselect("Campaign Filter")` populated from the `campaign` column.
  - `filter_dataset` updated to accept `selected_campaigns: Optional[List[str]]` defaulting to `None` (no filter) so benchmark mode is unaffected.
  - Campaign filter applied alongside existing channel, date, and territory filters.

- [x] **7.6 Test Coverage Expanded: 13 → 15 Tests**
  - `test_campaign_and_creative_drilldown` — verifies that `campaign` and `creative_type` columns exist in synthetic data and that `render_campaign_drilldown` returns a non-empty Plotly figure and grouped DataFrame.
  - `test_executive_brief_html_generation` — verifies that `generate_executive_brief_html` returns a string containing the required HTML structure, KPI section, AI recommendation, and governance sign-off badge.
  - `test_event_level_touchpoint_ingestion` extended to assert `campaign` and `creative_type` columns are present after event-level ingestion.

