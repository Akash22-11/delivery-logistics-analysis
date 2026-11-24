# Delivery Logistics Analysis — Executive Summary

**Dataset:** 25,000 last-mile delivery records (India)  
**Analysis:** 13-section EDA + statistical tests + predictive modeling  
**Notebook:** `notebooks/Delivery_Analysis_executed.ipynb` (runs top-to-bottom, zero errors)

---

## 🎯 Key Finding: The SLA Problem

| Delivery Mode | Promised (Expected) | Actual Avg | On-Time Rate |
|---------------|---------------------|------------|--------------|
| **Express**   | 4.5 h               | 6.2 h      | **26.2%**    |
| Same Day      | 8 h                 | 6.2 h      | 67.5%        |
| Two Day       | 16 h                | 6.3 h      | 99.6%        |
| **Standard**  | 24 h                | 6.2 h      | **100%**     |

- **Actual delivery time is ~6.2 h for ALL modes** — regardless of SLA
- Correlation between expected & actual time: **0.04** (near zero)
- **74 pp gap** between Express (26.2%) and Standard (100%) on-time rates
- **Conclusion:** SLA compliance reflects *how targets were set*, not operational performance

---

## 📊 What Drives Reliability (Ranked)

| Rank | Factor | Impact | Evidence |
|------|--------|--------|----------|
| 1 | **Delivery Mode** | **Huge** | 74 pp spread (Express → Standard) |
| 2 | **Weather** | Large | 19.6 pp (Cold 12.9% → Stormy 32.5% late) |
| 3 | **Distance** | Medium | Cost: r=0.991 with distance; Time: 3.7h → 8.7h |
| 4 | **Package Weight** | Small | Heavy: 21.5% late vs Light: 21.1% (0.4 pp) |
| 5 | **Partner** | Negligible | 2.6 pp spread (19.8% → 22.4%) |
| 6 | **Vehicle Type** | None | ANOVA F=0.41, p=0.842; cost varies 1-3% |

---

## 📈 Statistical Tests (α = 0.05)

| Test | Result | Effect Size | Interpretation |
|------|--------|-------------|----------------|
| Weather × Late/Failed | **χ² = 1354.5, p < 0.001** | Cramer's V = 0.233 | Weather strongly predicts failure |
| Partner × Late/Failed | χ² = 14.0, p = 0.081 | V = 0.024 | **Not significant** |
| Cost by Vehicle (ANOVA) | F = 0.41, p = 0.842 | η² = 0.0001 | Vehicle irrelevant for cost |
| Rating vs Time Deviation | **ρ = -0.567, p < 0.001** | Spearman ρ = -0.567 | Later = lower ratings |

> No test is "significant but tiny" — significant effects have meaningful sizes.

---

## 🤖 Predictive Model

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| Majority Class (baseline) | 0.733 | 0.000 | 0.000 | 0.000 | 0.500 |
| **Logistic Regression** | **0.897** | 0.805 | 0.808 | **0.807** | 0.962 |
| Random Forest | 0.894 | 0.797 | 0.807 | 0.802 | **0.966** |

- **Top feature:** `delivery_mode_express` (importance 0.384 / coef +4.85)
- Model learns **SLA labels**, not operational root causes
- Use for **dispatch-time flagging only** (express/same-day = high risk)

---

## 💡 Business Recommendations

| # | Action | Tied to Finding |
|---|--------|-----------------|
| 1 | **Reset Express SLA to 6–8 h** (or reprice) | Mode is an SLA label; 4.5h promise is unmeetable |
| 2 | **Weather contingency for stormy/rainy days** | +19.6 pp late rate; 3× failure rate |
| 3 | **Stop optimizing vehicle assignment for speed** | Vehicle explains ~0% variance once distance fixed |
| 4 | **Use model for risk flagging, not operations** | It predicts SLA buckets, not why deliveries fail |

---

## ⚠️ Critical Limitations

1. **Likely synthetic data** — perfect cost–distance linearity (r=0.991, identical 5.00 INR/km slope in all 5 regions), constant actual time across modes, perfectly balanced partner volumes
2. **No real timestamps** — epoch encoding only (nanosecond field = hours); no dispatch/pickup/transit events
3. **Leakage in spirit** — `delivery_mode` encodes the outcome via SLA target
4. **No temporal dimension** — random 80/20 split, no time-series analysis possible

---

## 📁 Deliverables

| File | Description |
|------|-------------|
| `notebooks/Delivery_Analysis_executed.ipynb` | Full analysis (90 cells, zero errors) |
| `notebooks/Delivery_Analysis_Report.html` | Clean HTML report (no code cells) |
| `notebooks/Delivery_Analysis.html` | Full notebook with code + outputs |
| `data/processed/delivery_features.csv` | 25,000 × 22 enriched dataset |
| `data/processed/statistical_tests_summary.csv` | Section 10 results table |
| `data/processed/model_comparison.csv` | Section 11 model metrics |
| `README.md` | Project summary, run instructions, key numbers |

---

## 🚀 Next Steps (If Continuing)

1. **Obtain real timestamp data** — dispatch, pickup, delivery events
2. **Add courier-level features** — experience, workload, traffic
3. **Temporal train/test split** — simulate production deployment
4. **A/B test Express SLA change** — pilot 7h SLA in one region
5. **Failure root-cause codes** — 1,328 failures have no reason code

---

*Generated from completed 13-section analysis. All numbers traceable to notebook cells.*