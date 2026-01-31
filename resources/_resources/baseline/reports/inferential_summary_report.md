# Section 2.7 – Inferential Statistics Summary Report

_Generated: 2025-12-29 10:42:11_

This report summarizes key inferential diagnostics from Section 2.7,
including representativeness, distribution shape, group differences,
effect sizes, multicollinearity, and interaction effects.

## 1. Representativeness & Sample Bias

- No representativeness benchmark file (`sample_representativeness_report.csv`) was found.

## 2. Normality & Distribution Shape

- No normality test artifact (`normality_tests.csv`) was found.


## 3. Variance Homogeneity

- No variance homogeneity artifact (`variance_homogeneity_report.csv`) was found.


## 4. Group Differences & Comparative Tests

- ANOVA/Kruskal results (`anova_kruskal_results.csv`) not found.

- Chi-square relationship results (`chi_square_results.csv`) not found.

- Parametric t-test results (`t_test_results.csv`) not found.

- Nonparametric test results (`nonparametric_results.csv`) not found.

- Proportion / rate comparison results (`proportion_tests.csv`) not found.


## 5. Effect Sizes & Practical Significance

- No effect size artifact (`effect_size_report.csv`) was found.


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

