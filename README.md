# Last-Mile Delivery Analytics

End-to-end exploratory analysis of **25,000 last-mile deliveries across India**: what drives delays and failures, how delivery cost behaves, and what shapes customer ratings.

> Built as a college data analytics project. The full analysis lives in one Jupyter notebook.

---

## Project Goals

- Clean a real-world-style logistics dataset and document every data-quality decision.
- Answer business questions on cost, delays, failures, partner performance and customer satisfaction.
- Test whether observed differences are statistically meaningful, not just visible in a chart.
- Turn the findings into practical recommendations for a logistics operator.

## Dataset

| Item | Detail |
|---|---|
| File | `data/raw/Delivery_Logistics.csv` |
| Rows | 25,000 deliveries |
| Partners | Delhivery, Blue Dart, Ekart, DHL, FedEx, Shadowfax, XpressBees, Amazon Logistics, Ecom Express |
| Regions | North, South, East, West, Central |

**Columns:** `delivery_id`, `delivery_partner`, `package_type`, `vehicle_type`, `delivery_mode`, `region`, `weather_condition`, `distance_km`, `package_weight_kg`, `delivery_time_hours`, `expected_time_hours`, `delayed`, `delivery_status`, `delivery_rating`, `delivery_cost`.

### Data issues found and handled

| Issue | How it was handled |
|---|---|
| `delivery_time_hours` and `expected_time_hours` are stored as timestamps (e.g. `1970-01-01 00:00:00.000000008`); the nanosecond count equals the hours | Parsed back into numeric hours |
| `delivery_id` is corrupted (read as float, many duplicates) | Dropped; row index used as the identifier |
| About 255 rows have a delivery time of 0 hours | Flagged and excluded from speed calculations |
| Every `failed` delivery is also marked `delayed = yes` | Outcome split into `on_time`, `late` and `failed` and analysed separately |
| Actual delivery time barely varies by delivery mode while expected time does | Documented as a dataset property; SLA results are interpreted with this in mind |

## Analysis Overview

1. **Data audit and cleaning**: missing values, duplicates, corrupted fields, invalid rows.
2. **Feature engineering**: time deviation, cost per km, cost per kg, speed, weight tier, distance band.
3. **Univariate analysis**: distributions of cost, distance, weight, partner share, delay baseline and ratings.
4. **Bivariate analysis**: partner benchmarks, weather impact, vehicle type, delivery mode, distance vs cost.
5. **Multivariate analysis**: partner x region x weather risk, vehicle x weather x distance, satisfaction drivers.
6. **Mode and SLA analysis**: actual vs expected time, regional bottlenecks, heavy packages.
7. **Statistical testing**: chi-square, ANOVA / Kruskal-Wallis, Spearman correlation with effect sizes.
8. **Extensions**: partner scorecard and a delay-risk predictor (uses only information known before delivery).
9. **Insights, recommendations and limitations.**

## Key Findings

> Preliminary results from the data exploration. Update these with the final numbers from the notebook before submitting.

- Stormy, rainy and foggy weather are associated with noticeably more delays and failures than clear weather.
- Delivery cost is driven almost entirely by distance; package weight and vehicle type have little effect.
- Delivery partners and regions perform very similarly, with only small differences.
- Delayed and failed deliveries receive much lower ratings than on-time ones.
- SLA results by delivery mode mostly reflect how expected times were set, not real-world partner performance.

## Repository Structure

```
last-mile-delivery-analytics/
├── data/
│   ├── raw/                  # original CSV, never modified
│   └── processed/            # cleaned dataset
├── notebooks/
│   └── Delivery_Analysis.ipynb
├── reports/                  # exported HTML of the executed notebook
├── PROGRESS.md               # task-by-task build log
├── requirements.txt
└── README.md
```

## Tech Stack

Python, pandas, NumPy, matplotlib, seaborn, SciPy, statsmodels, scikit-learn, Jupyter.

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/last-mile-delivery-analytics.git
cd last-mile-delivery-analytics

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the notebook
jupyter notebook notebooks/Delivery_Analysis.ipynb
```

Run all cells from top to bottom. Random seeds are fixed (`random_state=42`) so results are reproducible.

## Limitations

- The dataset has no real calendar timestamps, so true time-series or seasonality analysis is not possible.
- Delivery mode strongly determines the expected time, so SLA results should be read with care.
- Several variables (partner, region, vehicle type) show very small differences, which suggests the data may be synthetic.
- Findings show associations, not causation.

## Future Work

- Validate the findings on real operational data with true timestamps and city-level locations.
- Add cost-anomaly detection and delivery-segment clustering.
- Deploy the delay-risk predictor as a small interactive app.

## Team

| Name | Role |
|---|---|
| Akash Sarkar | |
| *(teammate)* | |
| *(teammate)* | |

## License

Add a license of your choice (for example MIT) or remove this section.
