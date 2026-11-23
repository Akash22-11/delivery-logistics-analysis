# Weaknesses Checklist — Delivery Logistics Analysis

Generated after full notebook review (kernel restart, top-to-bottom execution, zero errors).

---

## Data Issues

| # | Issue | Severity | Location | Notes |
|---|-------|----------|----------|-------|
| D1 | **Raw data likely synthetic** | High | `data/raw/Delivery_Logistics.csv` | Perfect cost–distance linearity (r=0.991, identical 5.00 INR/km slope in all 5 regions), exactly 6.2–6.3 h actual time across all 4 modes, perfectly balanced partner volumes (10.8–11.3% each). Limits real-world generalizability. |
| D2 | **No real timestamps** | High | Section 2, Section 9 | Both time columns are epoch timestamps where nanosecond field = hours. No dispatch, pickup, transit, or delivery event times. Cannot measure true SLA compliance or bottlenecks. |
| D3 | **`delivery_id` corrupted** | Medium | Section 3.3 | Float values, 498 duplicates (250 rows with value 250.99, 250 with 24750.01). Handled by using row index. |
| D4 | **255 zero-time rows** | Medium | Section 3.4, Section 5 | `delivery_time_hours == 0` but status = delivered. Flagged and excluded from speed calculations (255 NaN in `speed_kmph`). |
| D5 | **`delayed` flag redundant** | Low | Section 3.7 | Deterministic from `delivery_status`: `delayed=yes` iff status ∈ {delayed, failed}. No new information. |

---

## Analysis Gaps

| # | Issue | Severity | Location | Notes |
|---|-------|----------|----------|-------|
| A1 | **Mode/time quirk not fully explored** | High | Section 9 | Actual time ~6.2 h for ALL modes. The notebook notes this but doesn't test *why* — e.g., is `delivery_time_hours` generated as `expected_time_hours + noise`? The express mode has `corr(expected, actual)=0.678` while others are NaN (single expected value per mode). |
| A2 | **No temporal dimension** | Medium | Sections 11, 13 | Random 80/20 split. No date column exists, so time-series analysis is impossible. Concept drift, seasonality untestable. |
| A3 | **Heavy package analysis limited** | Medium | Section 9.2 | Only compares late rate by weather and outcome by mode. No interaction test (weight × weather × mode), no cost-per-kg analysis by tier. |
| A4 | **No failure root-cause codes** | Medium | Section 13 | 1,328 failed deliveries (5.3%) have no failure reason (address issue, customer unavailable, damage, etc.). Cannot segment failures. |
| A5 | **Partner analysis only at aggregate level** | Low | Section 7.1 | Late rate span = 2.6 pp. No drill-down by partner × mode × region × weather to find specific weak combinations. |

---

## Modeling Issues

| # | Issue | Severity | Location | Notes |
|---|-------|----------|----------|-------|
| M1 | **Leakage in spirit** | High | Section 11, Section 12.3, Section 13.1 | `delivery_mode` encodes the SLA target which determines the outcome. Model learns "express = late", not operational root causes. Feature importance of `delivery_mode_express` = 0.384 (RF) / coef = +4.85 (LR). |
| M2 | **No temporal split** | High | Section 11 | Random split ignores time ordering. In production, train on Jan–Mar, test on Apr. |
| M3 | **Class imbalance handled by stratification only** | Medium | Section 11 | 73/27 split. No class weights, SMOTE, or threshold tuning. For production, recall on minority class matters more. |
| M4 | **`n_jobs=-1` deprecated** | Low | Section 11 cell `aa0f9b45` | sklearn 1.8+ warns: `'n_jobs' has no effect since 1.8 and will be removed in 1.10`. Should remove or set explicitly. |
| M5 | **Single tree-based model only** | Low | Section 11 | Only Random Forest tested. No XGBoost, LightGBM, or gradient boosting for comparison. |
| M6 | **No calibration check** | Low | Section 11 | Predicted probabilities not validated (reliability diagram, Brier score). |

---

## Visualization / Presentation

| # | Issue | Severity | Location | Notes |
|---|-------|----------|----------|-------|
| V1 | **Some charts lack explicit axis units in titles** | Low | Sections 6–8 | Most have labels but titles like "Delivery Cost Distribution" don't restate "(INR)". |
| V2 | **Heatmap colorbars could be more descriptive** | Low | Sections 8, 9 | "Late-or-Failed Rate (%)" is good; "Avg Time Deviation (h)" could specify "negative = early". |
| V3 | **Section 10 summary table uses markdown** | Low | Cell `0a5bf64c` | Not rendered as a styled table in notebook; plain markdown. |
| V4 | **No interactive/dynamic charts** | Low | All | Static matplotlib/seaborn only. Could use plotly for hover details. |

---

## Reproducibility

| # | Issue | Severity | Location | Notes |
|---|-------|----------|----------|-------|
| R1 | **Execution requires project root as cwd** | Medium | README | Relative paths (`data/raw/...`) only resolve from project root. Notebook metadata path must be set to `.` for nbconvert. |
| R2 | **No requirements.txt / environment.yml** | Medium | Root | Dependencies listed in README only. No pinned versions. |
| R3 | **Random seeds set but not all libraries** | Low | Sections 2, 11 | `random_state=42` for sklearn, but numpy/pandas sampling not explicitly seeded globally. |

---

## Priority Fixes (if continuing)

1. **Add `requirements.txt` with pinned versions** — ensures reproducibility.
2. **Remove `n_jobs=-1` from LogisticRegression** — fixes deprecation warning.
3. **Add explicit note in Section 11** that model is an SLA-label classifier, not operational.
4. **Consider adding a "data provenance" section** — where did this dataset come from? Synthetic?
5. **Export HTML with `exclude_input=True`** for cleaner stakeholder view.

---

## What's Solid

- ✅ Notebook executes top-to-bottom with zero errors (90 cells, 31 code)
- ✅ Every chart has title, axis labels, and interpretation markdown
- ✅ Headings numbered consistently (1–13, with subsections 9.2, 10.1, 11.1–11.3, 12.1–12.3, 13.1–13.2)
- ✅ All numbers in Sections 12–13 trace to earlier cell outputs
- ✅ Statistical tests include hypothesis, test, p-value, effect size, plain-English conclusion
- ✅ "Significant but tiny" callouts correctly applied (none in this dataset)
- ✅ Majority-class baseline included and clearly beaten
- ✅ Honest limitations section (6 items in Section 12.3, 8 in Section 13.1)
- ✅ Future work is actionable and tied to findings (8 items)
- ✅ README.md with project summary, run instructions, folder structure
- ✅ HTML export generated (`notebooks/Delivery_Analysis.html`)
- ✅ Executed notebook saved (`notebooks/Delivery_Analysis_executed.ipynb`)