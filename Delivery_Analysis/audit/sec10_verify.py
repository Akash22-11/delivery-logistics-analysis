"""Verify Section 10 statistical-test numbers against delivery_features.csv."""
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data/processed/delivery_features.csv")
ALPHA = 0.05
lof = df["outcome"].isin(["late", "failed"])  # late-or-failed binary

print("=" * 70)
print("1. Chi-square: weather_condition x late-or-failed")
ct = pd.crosstab(df["weather_condition"], lof)
chi2, p, dof, exp = stats.chi2_contingency(ct)
n = ct.values.sum()
min_dim = min(ct.shape) - 1
v = np.sqrt(chi2 / (n * min_dim))
print(f"  chi2={chi2:.1f}  p={p:.3e}  dof={dof}  Cramer's V={v:.3f}")

print("=" * 70)
print("2. Chi-square: delivery_partner x late-or-failed")
ct = pd.crosstab(df["delivery_partner"], lof)
chi2, p, dof, exp = stats.chi2_contingency(ct)
v = np.sqrt(chi2 / (n * min_dim))
print(f"  chi2={chi2:.1f}  p={p:.3g}  dof={dof}  Cramer's V={v:.3f}")

print("=" * 70)
print("3. Chi-square: delivery_mode x outcome")
ct = pd.crosstab(df["delivery_mode"], df["outcome"])
chi2, p, dof, exp = stats.chi2_contingency(ct)
n = ct.values.sum()
min_dim = min(ct.shape) - 1
v = np.sqrt(chi2 / (n * min_dim))
print(f"  chi2={chi2:.1f}  p={p:.3e}  dof={dof}  Cramer's V={v:.3f}")

print("=" * 70)
print("4. ANOVA: delivery_cost across vehicle_type")
groups = [g["delivery_cost"].values for _, g in df.groupby("vehicle_type")]
F, p = stats.f_oneway(*groups)
grand = df["delivery_cost"]
ss_between = sum(len(g) * (g.mean() - grand.mean()) ** 2 for g in groups)
ss_total = ((grand - grand.mean()) ** 2).sum()
eta2 = ss_between / ss_total
print(f"  F={F:.2f}  p={p:.3f}  eta^2={eta2:.4f}")

print("=" * 70)
print("5. ANOVA: time_deviation_hours across weather_condition")
tdf = df.dropna(subset=["time_deviation_hours"])
groups = [g["time_deviation_hours"].values for _, g in tdf.groupby("weather_condition")]
F, p = stats.f_oneway(*groups)
grand = tdf["time_deviation_hours"]
ss_between = sum(len(g) * (g.mean() - grand.mean()) ** 2 for g in groups)
ss_total = ((grand - grand.mean()) ** 2).sum()
eta2 = ss_between / ss_total
print(f"  F={F:.2f}  p={p:.3e}  eta^2={eta2:.3f}")

print("=" * 70)
print("6. Kruskal-Wallis: delivery_cost across vehicle_type")
groups = [g["delivery_cost"].values for _, g in df.groupby("vehicle_type")]
H, p = stats.kruskal(*groups)
k = len(groups)
N = len(df)
eps2 = (H - (k - 1)) / (N - 1)  # epsilon-squared
print(f"  H={H:.2f}  p={p:.3f}  epsilon^2={eps2:.3f}")

print("=" * 70)
print("6b. Kruskal-Wallis: delivery_cost across delivery_mode (for contrast)")
groups = [g["delivery_cost"].values for _, g in df.groupby("delivery_mode")]
H, p = stats.kruskal(*groups)
k = len(groups)
N = len(df)
eps2 = (H - (k - 1)) / (N - 1)
print(f"  H={H:.2f}  p={p:.3e}  epsilon^2={eps2:.3f}")

print("=" * 70)
print("7. Spearman: delivery_rating vs time_deviation_hours")
rho, p = stats.spearmanr(df["delivery_rating"], df["time_deviation_hours"])
print(f"  rho={rho:.3f}  p={p:.3e}")

print("=" * 70)
print("8. Welch t-test: delivery_cost late-or-failed vs on-time")
a = df.loc[lof, "delivery_cost"].values
b = df.loc[~lof, "delivery_cost"].values
t, p = stats.ttest_ind(a, b, equal_var=False)
d = (a.mean() - b.mean()) / np.sqrt((a.std(ddof=1) ** 2 + b.std(ddof=1) ** 2) / 2)
print(f"  t={t:.2f}  p={p:.3e}  Cohen's d={d:.3f}")

print("=" * 70)
print("9. Pearson: delivery_cost vs distance_km")
r, p = stats.pearsonr(df["delivery_cost"], df["distance_km"])
print(f"  r={r:.3f}  p={p:.3e}")

print("=" * 70)
print("10. Mann-Whitney: delivery_rating express vs standard")
a = df.loc[df["delivery_mode"] == "express", "delivery_rating"].values
b = df.loc[df["delivery_mode"] == "standard", "delivery_rating"].values
U, p = stats.mannwhitneyu(a, b, alternative="two-sided")
n1, n2 = len(a), len(b)
r = 1 - (2 * U) / (n1 * n2)
print(f"  U={U:.0f}  p={p:.3e}  r={r:.3f}")