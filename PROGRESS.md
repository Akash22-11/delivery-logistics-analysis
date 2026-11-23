## TASK 0 — Setup (2026-11-12)
- Folder structure created: `data/raw/`, `data/processed/`, `notebooks/`.
- `data/raw/Delivery_Logistics.csv` copied from the uploaded source (25,000 rows x 15 cols).
- `requirements.txt` written with the allowed package set and pinned versions.
- `PROGRESS.md` created empty (this file).
- Skeleton notebook `notebooks/Delivery_Analysis.ipynb` created with the 13 required
  Markdown section headers and one intro cell. Zero analysis code.
- Verified: notebook is valid JSON and executes top-to-bottom with no errors (nbclient).

## TASK 1 — Section 2: Data Loading (2026-11-12)
- Added imports + plotting theme cell (consistent seaborn style, 10-colour palette).
- Added Markdown cell explaining why timestamp parsing was needed (epoch ns field = hours).
- Added load + parse cell: reads CSV, converts `delivery_time_hours` and
  `expected_time_hours` via `pd.to_datetime(...).astype('int64')`.
- Output verified: both columns are now `int64` with values 0-24 (head shows 2, 6, 8, 9, 10, 16).
- Notebook executes top-to-bottom with zero errors.

## TASK 2 — Section 3: Data Quality Audit (2026-11-12)
- Inspect-only: no fixes applied. Sections 3.1-3.7 run the checks; 3.8 is the issue table.
- Findings (all match the known issues):
  - **Missing values: 0** in every column.
  - **Full-row duplicates: 0** (exact duplicates across all 15 columns).
  - **`delivery_id`:** float, 498 duplicate values across 24,502 unique. Two values
    (`250.99`, `24750.01`) each repeat 250 times; the rest are unique. Corrupted -> use row index.
  - **Zero-time rows: 255** (1.0%), all `delivered`, all `delayed=no`, expected time mean 12.5 h
    (would be on-time by construction).
  - **Categoricals:** 9 partners, 9 package types, 6 vehicles, 4 modes, 5 regions, 6 weather.
    All roughly balanced (no rare categories).
  - **Numeric:** distance 3.6-297.1 km, weight 0.67-49.52 kg, cost 95.67-1632.72 INR,
    rating 1-5. Mild skew only (delivery_time +0.41, rating -0.47). No negatives.
  - **Crosstab:** `delayed=yes` is exactly the union of {delayed, failed} (1.0/0.0 proportions).
- Issue table written to the notebook with rows affected and proposed fixes.
- Notebook executes top-to-bottom with zero errors.

## TASK 3 — Section 4: Data Cleaning (2026-11-12)
- Applied all decisions from the Section 3 table. Nothing dropped except `delivery_id`.
- Dropped `delivery_id`, reset to a clean 0-based integer index.
- Added `zero_time_flag` (255 True / 24,745 False); zero-time rows kept but excluded from
  speed calculations. All 255 are `on_time` by construction.
- Added `outcome`: delivered -> on_time (18,331), delayed -> late (5,341),
  failed -> failed (1,328). Reproduces `delivery_status` counts exactly.
- Standardised all 8 categorical columns to lowercase + stripped; verified no uppercase remains.
- Verified: 25,000 rows preserved, 0 new nulls, `delivery_id` absent.
- Saved to `data/processed/delivery_clean.csv` (25,000 x 16 cols).
- Notebook executes top-to-bottom with zero errors.

## TASK 4 — Section 5: Feature Engineering (2026-11-12)
- Created `time_deviation_hours`, `cost_per_km`, `cost_per_kg`, `speed_kmph` (NaN on
  zero_time_flag rows), `weight_tier` (light/medium/heavy at 10/20 kg), `distance_band`
  (short/medium/long by quantiles).
- Verified: no infinite values in any feature; only 255 NaN in `speed_kmph` (by design).
- Saved to `data/processed/delivery_features.csv` (25,000 x 22 cols).
- Notebook executes top-to-bottom with zero errors.

## TASK 5 + 6 — Section 6: Univariate Analysis (2026-11-12)
- Built all five questions (6.1-6.5) with one chart each + interpretation.
- **Q1 cost:** median 867.5, mean 864.9, skew = 0.001 -> **symmetric, NOT right-skewed**.
  IQR 747.1; 40.9% of deliveries cost > 1,000 INR.
- **Q2 distance/weight:** distance median 151 km, skew 0.002 -> 25% short / 50% medium /
  25% long. Weight median 25.1 kg, skew -0.003. No haul concentration.
- **Q3 partner share:** 10.8%-11.3% each (range 0.5 pp) -> perfectly balanced.
- **Q4 outcome:** on_time 73.3%, late 21.4%, failed 5.3%.
- **Q5 rating:** mean 3.67, median 4, left-skewed; 5-star share 29.5%.
- Fixed a bug where mean was printed as median (4.00 -> correct 3.67).
- Notebook executes top-to-bottom with zero errors.

## TASK 7 — Section 7: Bivariate Analysis (2026-11-12)
- Built all five questions (7.1-7.5) with one chart each + interpretation.
- **7.1 partner:** late rate 19.8-22.4% (2.6 pp), fail rate 4.4-5.9% (1.5 pp),
  rating 3.61-3.70 (0.09) -> **differences are small**, no partner stands out.
- **7.2 weather:** late rate 12.9-32.5% (19.7 pp), fail rate 3.2-8.9% (5.8 pp),
  time dev -8.3 to -4.3h (4h) -> **weather has a large effect**, stormy/rainy worst.
- **7.3 vehicle x distance band:** cost varies ~10-15 INR (1-3%), time ~0.1-0.2h (1-3%)
  across vehicles -> **vehicle type makes little difference** once distance controlled.
- **7.4 delivery mode:** late rate 0-59.4% (59.4 pp), fail rate 0-14.4%, cost 819-930 INR (14%)
  -> **mode has very large effect on reliability**, reflects SLA label property.
- **7.5 cost vs distance:** r = 0.991 overall and per region, slope = 5.00 INR/km identically
  across regions -> **near-perfect correlation**, cost ~ base + 5.0 x distance.
- Notebook executes top-to-bottom with zero errors.

## TASK 8 — Section 8: Multivariate Analysis (2026-11-12)
- Built both questions with heatmaps.
- **8.1 Late-or-failed rate:**
  - Partner x Region: 22.9% (delhivery / east) to 31.1% (shadowfax / west), spread ~8 pp.
    Partner and region both modest effects; no dramatic combinations.
  - Weather x Region: 14.5% (cold / south) to 44.5% (stormy / south), spread 30 pp.
    **Weather dominates** (stormy/rainy 36-45% vs clear/cold/hot 14-18%); region adds little.
- **8.2 Vehicle x Weather x distance band (avg time deviation):**
  - All cells negative (actual < expected), confirming expected time is a loose SLA.
  - Overall: -8.78h (bike / foggy) to -4.05h (truck / foggy) — 4.7h spread. Foggy/rainy are
    the highest cells in every panel.
  - Weather drives most variation; **vehicle type makes negligible difference** (<1.5h within
    any weather-distance cell).
  - Pattern holds at every distance band (short: -11.08 to -6.17h; medium: -8.89 to -3.63h;
    long: -7.20 to -1.32h).
- Verified against live data: extremes recomputed from `delivery_features.csv`.
- Notebook executes top-to-bottom with zero errors.

## TASK 9 — Section 9: Delivery Mode and SLA Analysis (2026-11-13)
- Built all three questions (outcome share, expected vs actual time, partner x mode) with
  a 4-panel chart (stacked bar, grouped bar, rating bar, partner x mode heatmap).
- **Outcome share by mode:** express 26.2% on-time / 59.4% late / 14.4% failed; same day
  67.5% / 25.8% / 6.8%; standard 100% / 0% / 0%; two day 99.6% / 0.3% / 0.1%.
  74 pp gap between express and standard — the strongest single driver in the whole dataset.
- **Actual time is ~6.2-6.3h for ALL modes** regardless of SLA; expected: express 4.5h,
  same day 8h, standard 24h, two day 16h.
- **Slack (expected - actual):** express -1.7h, same day +1.8h, standard +17.8h, two day +9.7h.
  Express is over-promised; standard is under-promised.
- **Corr(expected, actual) = 0.04 overall** (near zero) — expected time is a mode label, not
  a real target. Within express (the only mode with variable expected times) r = 0.68.
- **Avg rating by mode:** express 2.72, same day 3.54, two day 4.18, standard 4.22 — tracks
  SLA tightness, not partner quality.
- **Late rate by partner x mode:** express 57.0-61.6%, same day 23.8-29.1%, standard 0.0%,
  two day 0.1-0.6%. Partners are uniform within each mode (max partner gap 4.6 pp in express).
- Notebook executes top-to-bottom with zero errors.

## NEXT: Section 10 — Statistical Tests
- Pre-computed (ready to insert): chi2 mode x outcome (V=0.483), Kruskal-Wallis cost x mode
  (eps^2=0.010), Mann-Whitney rating express vs standard (r=0.697), Pearson cost vs distance
  (r=0.991), ANOVA time_deviation x weather (eta^2=0.036), t-test cost late vs on-time
  (d=0.496), chi2 weather x late/failed (V=0.233).