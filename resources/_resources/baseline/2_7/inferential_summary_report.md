# Section 2.7 – Inferential Statistics Summary Report

_Generated: 2026-01-07 19:21:07_

This report summarizes key inferential diagnostics from Section 2.7,
including representativeness, distribution shape, group differences,
effect sizes, multicollinearity, and interaction effects.

## 1. Representativeness & Sample Bias

- The sampling representativeness audit covered **2** benchmarked features.

- Some population benchmarks deviated from the sample: **2 WARN** and **0 FAIL** tests were detected.

**Largest absolute sample vs population deviations:**

- `gender` – category `Female`: sample is -0.01 percentage points away from population.
- `gender` – category `Male`: sample is 0.01 percentage points away from population.
- `Contract` – category `Two year`: sample is -0.01 percentage points away from population.
- `Contract` – category `One year`: sample is 0.01 percentage points away from population.
- `Contract` – category `Month-to-month`: sample is 0.00 percentage points away from population.

## 2. Normality & Distribution Shape

- Normality tests were run on **7** numeric features.

- **21** features were flagged as clearly non-normal or heavy-tailed.

- Non-normal variables may require transformation or nonparametric modeling downstream.


## 3. Variance Homogeneity

- Variance homogeneity tests were run across **3** (numeric, group) combinations.

- No major heteroskedasticity issues were detected among the configured tests.


## 4. Group Differences & Comparative Tests

- ANOVA/Kruskal tests were run for **138** (group, numeric) combinations.

- **106** of these tests showed statistically significant group differences (p ≤ 0.05).

- Chi-square tests were run for **6** categorical pairs to assess association.

- **6** categorical pairs showed significant dependence (p ≤ 0.05).

- Parametric t-tests were configured for **3** group comparisons.

- **2** comparisons showed statistically significant mean differences.

- Nonparametric tests (Mann–Whitney/Wilcoxon) were run for **3** comparisons.

- **2** nonparametric tests indicated significant group differences.

- Two-proportion tests were run for **3** scenarios (e.g., churn or adoption rates).

- **3** scenarios showed statistically significant rate differences.


## 5. Effect Sizes & Practical Significance

- Standardized effect sizes were computed for **20** unique tests.

- **6** effects were classified as large or very large (substantial practical impact).

**Top effect magnitude examples:**
- `Churn rate by Contract` – odds_ratio: effect ≈ 25.580 (magnitude: very large).
- `Churn rate by Contract` – relative_risk: effect ≈ 15.082 (magnitude: very large).
- `OnlineBackup by PaymentMethod` – odds_ratio: effect ≈ 2.200 (magnitude: large).
- `OnlineBackup by PaymentMethod` – relative_risk: effect ≈ 1.786 (magnitude: large).
- `TechSupport by SeniorCitizen` – odds_ratio: effect ≈ 1.470 (magnitude: medium).

## 6. Multicollinearity (VIF)

- No VIF artifact (`vif_report.csv`) was found.


## 7. Interaction Effects

- Two-way interaction models were evaluated for **3** (outcome, factor A, factor B) scenarios.

- **0** scenarios showed statistically significant interaction terms (p < 0.05).


## 8. Modeling Recommendations & Caveats

- Use non-normal or heavy-tailed variables with caution; consider transformations or nonparametric models.

- Address high-VIF predictors via feature selection, regularization, or dimensionality reduction to avoid unstable coefficients.

- Prioritize predictors and group splits that show both statistical significance **and** meaningful effect sizes.

- Incorporate significant interaction terms into modeling where they have clear business interpretation and adequate sample support.

- Interpret non-significant results carefully in scenarios flagged as potentially underpowered in the power analysis.

