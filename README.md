# Data Quality Engine - Data Product Pipeline

DEMO  WORK IN PROGRESS ⚠️

Welcome to my data blob. This repository is a work in progress and is not yet ready for production use.
It serves as practice and learning for me. It is overengineered because it is about exploring the capabilities of Python and the tools I can use.

I built a notebook-first data quality engine with config-driven contracts, append-only diagnostics, and reproducible artifacts — and I’ve been evolving it in tiers as my skills grow.

I started with a Telco churn dataset to scope the project as an analyst, but I am more interested in data integrity.

---

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Pandas: 2.1.4](https://img.shields.io/badge/Pandas-2.1.4-blue.svg)](https://pandas.pydata.org/)
[![Plotly: 5.18.0](https://img.shields.io/badge/Plotly-5.18.0-blue.svg)](https://plotly.com/)

![BigQuery](https://img.shields.io/badge/Google%20BigQuery-Analytics%20Warehouse-669DF6?logo=googlecloud)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-3C7EBB)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts%20%26%20Plots-11557C)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Pipeline-F7931E?logo=scikitlearn)

A **config-driven data quality & validation pipeline** built around the IBM Telco Customer Churn dataset.
This project profiles data, detects integrity issues, applies controlled cleaning, and produces **audit artifacts + dashboards + quality/readiness scores** suitable for analytics engineering workflows.

## Why this exists
In real analytics engineering, “clean data” is not a vibe — it’s a **repeatable process**:
- Validate inputs (schema, types, nulls, outliers, domain rules)
- Detect drift and instability
- Apply controlled fixes with a clear audit trail
- Produce **quality signals** that downstream modeling/BI can trust

This repo is designed to demonstrate that end-to-end workflow as a portfolio project.

---

## What this project does

### 1) Environment & Config Readiness
- Validates runtime assumptions, directory structure, and configuration bindings.
- Captures run metadata for traceability.

### 2) Data Profiling & Integrity Checks
- Numeric integrity and outlier detection (IQR / z-score style checks)
- Categorical profiling, token validation, allow-lists, domain enforcement
- Cross-domain consistency checks (numeric ↔ categorical bridging)
- Logic rule checks (constraints, dependency violations, rule catalog)

### 3) Controlled Cleaning + Audit Trail
- Cleaning orchestrator that applies fixes deterministically
- Safe type coercion, missing value handling, outlier treatment
- Domain/range enforcement and rare-category consolidation
- Change logs + before/after metrics + schema/version logs

### 4) Statistical Diagnostics & Explainability
- Group tests (ANOVA/Kruskal style where relevant)
- Effect sizes, relationships, and supporting diagnostics
- “Explainability” style artifacts for anomalies (context + index)

### 5) Drift & Stability Layer
- Drift metrics and verification artifacts
- Dataset hash/version registry for provenance

### 6) Quality Aggregation & Readiness Scoring
- Produces rollups that answer: *“Is this dataset ready for downstream use?”*
- Alerts/indices intended as lightweight governance hooks

---

## Outputs (Artifacts)

Artifacts are written into run-scoped output locations (recommended: `runs/<timestamp>/...`).

Representative outputs you’ll see include:
- `numeric_validation_report.csv`, `outlier_report_iqr_z.csv`
- `categorical_profile_df.csv`, `invalid_tokens.csv`
- `logic_integrity_report.csv`, `dependency_violations.csv`, `dq_rule_catalog.csv`
- `before_after_summary.csv`, `cleaning_change_log.csv` (names may vary by config)
- `drift_report.csv`, `data_drift_metrics.csv`, `dataset_version_registry.csv`
- `section2_unified_report.csv` (cross-section summary)
- Dashboards (HTML), e.g.:
  - `data_quality_dashboard.html`
  - `inferential_statistics_dashboard.html`
  - `master_dashboard.html`

> Note: Exact filenames can be configured in `project_config.yaml`.

---

## Repo Structure (recommended)

```text
.
├── README.md
├── notebooks/
│   ├── 01_EDA.ipynb
│   └── 02_DQ_IF.ipynb
├── src/
│   └── dq_engine/
│       ├── utils/
│       │   └── config.py
│       └── helpers/
├── config/
│   ├── project_config.yaml
│   └── setup_summary.json
├── data/
│   ├── raw/            # dataset lives here (gitignored)
│   └── processed/      # optional (gitignored)
├── resources/
│   └── _dash/          # optional: saved dashboards for demo
└── runs/               # run outputs (gitignored)


++++

And your README should have:

git clone ...
cd ...
python -m venv .venv
source .venv/bin/activate  # or Windows equivalent
pip install -e .
python -m dq_engine run --config config/project_config.yaml