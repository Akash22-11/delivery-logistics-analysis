# Delivery Logistics - Last-Mile Analysis (India)

**25,000 last-mile delivery records** • End-to-end EDA, statistical tests, predictive modeling, business insights

---

## Project Summary

This notebook performs a complete exploratory data analysis of a last-mile delivery dataset from India. The analysis covers:

- **Data quality audit & cleaning** — handles corrupted IDs, epoch-encoded timestamps, zero-time rows
- **Univariate, bivariate, multivariate analysis** — 6+5+2 questions with charts
- **Delivery mode & SLA analysis** — exposes the core finding: actual delivery time (~6.2 h) is constant across all modes while expected time varies by SLA
- **Statistical tests** — chi-square, ANOVA, Kruskal-Wallis, Spearman with effect sizes
- **Predictive modeling** — Logistic Regression + Random Forest predicting late/failed using only pre-delivery features
- **Business recommendations** — 4 actionable items tied to findings
- **Honest limitations** — data issues, synthetic timestamps, leakage in spirit

**Key finding:** Delivery mode is an SLA label, not an operational signal. Express promises 4.5 h but takes 6.2 h → 59% late rate by construction. The fix is contractual (reset SLA), not operational.

---

## How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn nbformat nbconvert
```

### Execute the notebook
```bash
cd delivery-logistics-analysis
# Option 1: Run via nbconvert (from project root)
python -m nbconvert --execute --to notebook --inplace notebooks/Delivery_Analysis.ipynb

# Option 2: Run via Python script (from project root)
python -c "
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
with open('notebooks/Delivery_Analysis.ipynb') as f:
    nb = nbformat.read(f, as_version=4)
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': '.'}})
with open('notebooks/Delivery_Analysis_executed.ipynb', 'w') as f:
    nbformat.write(nb, f)
"
```

**Important:** Run from the **project root** (`delivery-logistics-analysis/`) so relative paths (`data/raw/...`, `data/processed/...`) resolve correctly.

### View the HTML export
Open `notebooks/Delivery_Analysis.html` in a browser for a rendered copy with all charts and outputs.

---

## Folder Structure

```
delivery-logistics-analysis/
├── data/
│   ├── raw/
│   │   └── Delivery_Logistics.csv          # Original 25k rows × 15 cols
│   └── processed/
│       ├── delivery_clean.csv              # Cleaned data (25k × 16)
│       ├── delivery_features.csv           # With engineered features (25k × 22)
│       ├── statistical_tests_summary.csv   # Section 10 results
│       └── model_comparison.csv            # Section 11 results
├── notebooks/
│   ├── Delivery_Analysis.ipynb             # Main notebook (13 sections, 90 cells)
│   ├── Delivery_Analysis_executed.ipynb    # Executed copy with outputs
│   └── Delivery_Analysis.html              # HTML export
├── audit/
│   └── sec10_verify.py                     # Standalone verification script for Section 10
└── README.md
```

---

## Notebook Sections

| Section | Title | Key Outputs |
|---------|-------|-------------|
| 1 | Introduction | Dataset description, known issues |
| 2 | Data Loading | Timestamp parsing (epoch ns → hours) |
| 3 | Data Quality Audit | Missing, duplicates, ID corruption, zero-time, categorical counts, numeric summaries |
| 4 | Data Cleaning | Drop ID, flag zero-time, create outcome, standardize text |
| 5 | Feature Engineering | time_deviation, cost_per_km, cost_per_kg, speed, weight_tier, distance_band |
| 6 | Univariate Analysis | 6 charts: cost, distance/weight, partner volume, outcome, rating |
| 7 | Bivariate Analysis | 5 charts: partner, weather, vehicle×distance, mode, cost×distance |
| 8 | Multivariate Analysis | 2 heatmaps: partner×region, weather×region; vehicle×weather×distance |
| 9 | Delivery Mode & SLA | Outcome share, actual vs expected, SLA slack, rating, partner×mode, heavy packages |
| 10 | Statistical Tests | 5 tests with hypothesis, p-value, effect size, conclusion; summary table |
| 11 | Predictive Model | Logistic Regression + Random Forest vs majority baseline; feature importances |
| 12 | Insights & Recommendations | 7 findings, 4 recommendations, limitations table |
| 13 | Limitations & Future Work | 8 limitations, 8 future work ideas |

---

## Key Numbers at a Glance

| Metric | Value |
|--------|-------|
| Rows | 25,000 |
| On-time / Late / Failed | 73.3% / 21.4% / 5.3% |
| Express on-time rate | 26.2% |
| Standard on-time rate | 100% |
| Actual delivery time (all modes) | ~6.2–6.3 h |
| Corr(expected, actual) | 0.04 |
| Weather late-rate spread | 12.9% (cold) → 32.5% (stormy) |
| Cost–distance correlation | r = 0.991 |
| Model ROC-AUC (LogReg / RF) | 0.962 / 0.966 |
| Model F1 (LogReg / RF) | 0.807 / 0.802 |

---

## Known Weaknesses (Checklist)

See [WEAKNESSES_CHECKLIST.md](WEAKNESSES_CHECKLIST.md) for a detailed audit of remaining issues.

**Top concerns:**
1. Raw data (`data/raw/Delivery_Logistics.csv`) is likely synthetic — perfect cost–distance linearity, constant actual time, balanced partner volumes
2. No real timestamps — epoch encoding only, no dispatch/checkpoint events
3. `delivery_mode` leakage in spirit — model learns SLA labels, not operations
4. No temporal split — random 80/20 ignores time ordering
5. 255 zero-time rows excluded from speed calculations
6. Section 11 uses `n_jobs=-1` deprecated in sklearn 1.8+

---

## License

MIT — free to use, modify, distribute.