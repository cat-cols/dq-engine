# Section 2.7 – Inferential Statistics Summary Report

_Generated: 2025-12-12 14:02:03_

This report summarizes key inferential diagnostics from Section 2.7,
including representativeness, distribution shape, group differences,
effect sizes, multicollinearity, and interaction effects.

## 1. Representativeness & Sample Bias

- No representativeness benchmark file (`sample_representativeness_report.csv`) was found.

## 2. Normality & Distribution Shape

- Normality tests were run on **8** numeric features.

- **24** features were flagged as clearly non-normal or heavy-tailed.

- Non-normal variables may require transformation or nonparametric modeling downstream.


## 3. Variance Homogeneity

- No variance homogeneity artifact (`variance_homogeneity_report.csv`) was found.


## 4. Group Differences & Comparative Tests

- ANOVA/Kruskal results (`anova_kruskal_results.csv`) not found.

- Chi-square relationship results (`chi_square_results.csv`) not found.

- Parametric t-test results (`t_test_results.csv`) not found.

- Nonparametric test results (`nonparametric_results.csv`) not found.

- Proportion / rate comparison results (`proportion_tests.csv`) not found.


## 5. Effect Sizes & Practical Significance

- Standardized effect sizes were computed for **8** unique tests.

- **0** effects were classified as large or very large (substantial practical impact).

**Top effect magnitude examples:**
- `tenure` – r: effect ≈ -0.352 (magnitude: medium).
- `expected_total_senior` – r: effect ≈ -0.343 (magnitude: medium).
- `expected_min_total_from_contract` – r: effect ≈ -0.287 (magnitude: small).
- `TotalCharges` – r: effect ≈ -0.199 (magnitude: small).
- `expected_total_from_tenure_monthly` – r: effect ≈ -0.199 (magnitude: small).

## 6. Multicollinearity (VIF)

- No VIF artifact (`vif_report.csv`) was found.


## 7. Interaction Effects

- No interaction artifact (`interaction_effects.csv`) was found.


## 8. Modeling Recommendations & Caveats

- Use non-normal or heavy-tailed variables with caution; consider transformations or nonparametric models.

- Address high-VIF predictors via feature selection, regularization, or dimensionality reduction to avoid unstable coefficients.

- Prioritize predictors and group splits that show both statistical significance **and** meaningful effect sizes.

- Incorporate significant interaction terms into modeling where they have clear business interpretation and adequate sample support.

- Interpret non-significant results carefully in scenarios flagged as potentially underpowered in the power analysis.

