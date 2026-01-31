<details>
<summary style="
    cursor:pointer;background:#f7f7fb;border: 1px solid #e5e7eb;
    padding:10px 12px;border-radius:10px;font-weight:900;">
➡︎ ☞ ➤ ⟿ Suggestions for config
</summary>

💡💡 **You have `MULTIPLE_TESTING` defined twice.** YAML will keep the *last one* and silently overwrite the first. Decide which shape you want and **merge them into one** (or rename one, e.g. `MULTIPLE_TESTING_MASTER` vs `MULTIPLE_TESTING_SIMPLE`).

💡💡 **`CONTRACTS` vs `DATA_CONTRACTS` overlap conceptually.** If both are used by different evaluators, fine—otherwise this is cognitive tax. Consider **converging onto one list** with a `stage:` or `group:` field.

💡💡 **SeniorCitizen type/domain mismatch:**

* `SCHEMA_EXPECTED_DTYPES_SEMANTIC` says `SeniorCitizen: int`
* `EXPECTED_LEVELS` has `"0"`/`"1"` as **strings**
  Pick one reality (int 0/1 or string "0"/"1") and align **everywhere** (parsing → dtype → expected levels → tests).

💡💡 **`DRIFT.BASELINE_NUMERIC_PROFILE` path doesn’t match your PATHS conventions.** It’s `"resources/artifacts/..."` but your artifacts root is `"Level_3/resources/artifacts/"`. Normalize it (or explicitly document “relative to Level_3” vs “relative to PROJECT_ROOT”) to avoid the classic “works on my machine” curse.

💡💡 **`DERIVED_FEATURES.avg_streaming_spend` references columns that don’t exist in Telco (unless you created them):** `StreamingMoviesCharges`, `StreamingTVCharges`, `StreamingServicesCount`. Either (a) add a guard in code, (b) move these into a dataset-specific `DERIVED_FEATURES_BY_DATASET.TELCO`, or (c) remove if it’s placeholder.

💡💡 **`TEMPORAL.INTERVALS` looks like placeholders for non-Telco datasets** (`call_start_ts`, `contract_start_date`, etc.). If Telco doesn’t have them, add an `ENABLED` toggle per interval or keep them under something like `TEMPORAL.OPTIONAL_INTERVALS` so the runtime doesn’t have to guess.

💡💡 **`ONEHOT.GROUPS.contract_type.columns` aren’t quoted and include spaces/hyphens.** YAML will parse them as strings, but downstream code often expects exact column names—quote them for safety and consistency (like you already do for other lists).

💡💡 **`PROPORTION_CI.TARGETS` repeats `"Contract"` twice.** Not harmful, but it’s wasted work and confusing when you inspect outputs.

💡💡 **Consider making “Stage/Section boundaries” first-class config, not comments.** Example: `STAGES: { STAGE_4_INFERENTIAL: { ... } }` or `SECTION_2: { ... }`. Comments don’t survive programmatic transformations; keys do.

If you want, I can also give you a tiny “index map” (section → key paths) so your `C("...")` lookups stay consistent and you don’t end up with config spaghetti disguised as YAML.


---
---

* Draft a **minimal Telco-flavored `project_config.yaml`** stub that includes:

  * `LOGIC_IMPACT`, `DATA_CONTRACTS`, `PERFORMANCE.LOGIC`, `AUDIT.LOGIC`, `ANOMALY_CONTEXT`, `LOGIC.NETWORK`
* with placeholders that exactly match the column names in the IBM dataset, so you can start wiring 2.5.12–2.5.15 just by filling in thresholds.

---
---
</details>

<details>
<summary style="
    cursor:pointer;background:#f7f7fb;border: 1px solid #e5e7eb;
    padding:10px 12px;border-radius:10px;font-weight:900;">
➡︎ ☞ ➤ ⟿ Suggestions for config
</summary>

## 🧭 1. What a Professional YAML Checklist Is

Professionals treat YAML checklists as a **lightweight project manifest** — a single source of truth that documents:

* **Notebook order** (Level 0 → Level 3, etc.)
* **Expected tasks** within each notebook
* **Status** (`[ ]` pending, `[x]` complete)
* **Artifacts** (e.g., dataset outputs, reports, model files)
* **Dependencies** (what notebook or dataset must run before this one)

It’s stored in the root of the project (e.g. `project_plan.yaml` or `notebook_outline.yaml`) and version-controlled in Git.

---

## 📁 2. Example — YAML Roadmap for Your Level 3 Project

Here’s a professional-grade starting point for your Telco Churn project using your existing notebook sequence:

```yaml
# telco_project_plan.yaml
project: Telco Customer Churn
level: 3
description: >
  Level 3 introduces systematic validation, cleaning, statistical testing,
  and baseline modeling, building on modular Level 2 EDA functions.

notebooks:
  01_EDA:
    description: Exploratory data analysis and variable inspection.
    tasks:
      - [x] Load raw dataset
      - [x] Profile numerical & categorical features
      - [x] Visualize churn distribution
      - [ ] Export eda_summary.json
    outputs:
      - reports/eda_summary.json
      - figures/01_*.png

  02_Data_Validation_and_Cleaning:
    description: Validate schema, detect issues, and standardize dataset.
    tasks:
      - [x] Load schema & dtype definitions
      - [x] Perform missing value audit
      - [ ] Run logical consistency checks
      - [ ] Clean categorical and numeric columns
      - [ ] Generate validation_summary.json
    outputs:
      - data/processed/telco_clean.csv
      - reports/validation_summary.json

  03_Preprocessing:
    description: Encode, scale, and split data for modeling.
    tasks:
      - [ ] Encode categorical features
      - [ ] Scale numeric features
      - [ ] Train/validation/test split
    outputs:
      - data/processed/telco_preprocessed.csv

  04_Feature_Engineering:
    tasks:
      - [ ] Create derived variables (tenure buckets, total spend, etc.)
      - [ ] Evaluate correlation & redundancy
      - [ ] Update feature_schema.yaml
    outputs:
      - data/processed/telco_features.csv

  05_Statistical_Analysis:
    tasks:
      - [ ] Hypothesis testing (churn vs. tenure, charges, etc.)
      - [ ] Effect size calculation
      - [ ] Significance summary
    outputs:
      - reports/statistical_tests.json

  06_Visualization:
    tasks:
      - [ ] Churn by demographics & service type
      - [ ] Feature correlation heatmap
      - [ ] Export publication-quality figures
    outputs:
      - figures/06_*.png

  07_Modeling:
    tasks:
      - [ ] Baseline logistic regression
      - [ ] Evaluate AUC, accuracy, precision, recall
      - [ ] Save model pipeline (.pkl)
    outputs:
      - models/baseline_logistic.pkl
      - reports/model_metrics.json

  08_Evaluation:
    tasks:
      - [ ] Generate confusion matrix & ROC
      - [ ] Compare model variants
      - [ ] Log results
    outputs:
      - figures/08_*.png
      - reports/evaluation_summary.json

  09_Explainability:
    tasks:
      - [ ] SHAP & permutation feature importance
      - [ ] Interpret top drivers of churn
    outputs:
      - figures/09_shap_*.png
      - reports/feature_importance.json

  10_Insights:
    tasks:
      - [ ] Summarize business implications
      - [ ] Recommend retention strategies
      - [ ] Draft executive report
    outputs:
      - reports/insights_summary.md
```

---

## 🧩 3. How Professionals Use This

### a. **Track Progress**

Use `[x]` and `[ ]` boxes like a kanban board:

```bash
# quick CLI check
grep "\[ \]" telco_project_plan.yaml
```

### b. **Automate Execution**

In later levels, Python or `make` scripts parse the YAML to:

* Auto-run notebooks in order (`papermill`, `nbconvert`, `jupyter nbflow`, etc.)
* Verify expected outputs exist
* Generate progress dashboards

### c. **Team Collaboration**

Teams reference the YAML file in PRs and issue tracking:

> “Finishing 02_Data_Validation_and_Cleaning — 3/5 tasks complete ✅”

### d. **Governance and Reproducibility**

Auditors or reviewers can read this file and instantly know:

* What’s been done
* Which datasets were produced
* How each stage depends on the previous one

---

## ⚙️ 4. How to Integrate It into Your Workflow

1. **Create the file:**
   Save the YAML above as `project_plan.yaml` in your root folder.

2. **Sync with Git:**
   Commit it early and update checkboxes as you progress.

3. **Add helper function:**
   Add a Python cell in your utilities:

   ```python
   import yaml, pprint
   with open("project_plan.yaml") as f:
       plan = yaml.safe_load(f)
   pprint.pp(plan["notebooks"]["02_Data_Validation_and_Cleaning"])
   ```

4. **(Optional)** Build a small script that:

   * Loads YAML
   * Verifies outputs exist for checked tasks
   * Prints “✅ 80% complete” progress summary

---

## 🚀 5. Long-Term Benefits

| Benefit                 | Why It Matters                                         |
| ----------------------- | ------------------------------------------------------ |
| **Reproducibility**     | Makes it trivial to rebuild your pipeline from scratch |
| **Transparency**        | Reviewers or employers can see structure at a glance   |
| **Automation-ready**    | Future CI/CD integration for Level 7–12                |
| **Professional polish** | Looks like a production data-engineering manifest      |

---

Would you like me to generate a **starter `project_plan.yaml` file** (ready to drop into your `/PROJECTS/Telco/Level_3/` folder) with placeholders for task status that you can check off live as you complete each notebook?

</details>

<details>
<summary style="
    cursor:pointer;background:#f7f7fb;border: 1px solid #e5e7eb;
    padding:10px 12px;border-radius:10px;font-weight:900;">
➡︎ ☞ ➤ ⟿ Suggestions for config
</summary>

#?A **companion version** that also checks **schema consistency** (e.g., compares columns to `feature_schema.yaml` and prints mismatches)?

#?That version integrates directly with your `validate.py` logic but works interactively inside notebooks.

# Awesome — here’s a **notebook-friendly companion guard** 
# that also checks your data against **`config/feature_schema.yaml`** 
# (same rules as your CLI validator), prints a clear report,
# and lets you choose whether to **raise on critical errors.
# Drop this **single cell** near the top of your notebooks (after `df` is loaded, or let it auto-load):


# ================================================================
# 🔒 Dataset Guard (Auto-Load + Target + Schema Consistency Check)
#   - Validates against config/feature_schema.yaml
#   - Mirrors src/pipeline/validate.py logic, but for notebooks
# ================================================================
# from pathlib import Path
# import pandas as pd
# import yaml

# --------- Settings ----------
SCHEMA_PATH = Path("config/feature_schema.yaml")
AUTO_LOAD_PATTERN = ["**/telco_*.parquet", "**/telco_*.csv"]
RAISE_ON_CRITICAL = True   # flip to False if you want to continue on FAIL
TARGET_NAME = "Churn_flag"

# --------- Locate / load dataframe if df not present ----------
if "df" not in locals():
    files = []
    for pat in AUTO_LOAD_PATTERN:
        files += sorted(Path.cwd().glob(pat), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError("❌ No dataset found (looked for telco_*.parquet/csv).")
    latest = files[0]
    print(f"📦 Auto-loading dataset: {latest}")
    if latest.suffix == ".parquet":
        df = pd.read_parquet(latest)
    elif latest.suffix == ".csv":
        df = pd.read_csv(latest)
    else:
        raise ValueError(f"Unsupported format: {latest.suffix}")
else:
    print("✅ Using dataset already in memory (df)")

# --------- Ensure target exists / fix if possible ----------
if TARGET_NAME not in df.columns:
    if "Churn" in df.columns:
        print("⚙️ Creating Churn_flag from 'Churn' …")
        df["Churn"] = df["Churn"].astype(str).str.strip().str.title()
        df[TARGET_NAME] = df["Churn"].map({"No": 0, "Yes": 1}).astype("int8")
    else:
        raise ValueError(f"❌ Target '{TARGET_NAME}' missing and no 'Churn' to derive from.")

# Binary integrity of target
u = sorted(df[TARGET_NAME].dropna().unique().tolist())
if u != [0, 1]:
    raise ValueError(f"❌ Target '{TARGET_NAME}' must be binary 0/1. Found: {u}")
print(f"✅ Target '{TARGET_NAME}' verified binary (0/1)")

# --------- Load schema ----------
if not SCHEMA_PATH.exists():
    raise FileNotFoundError(f"❌ Schema file not found: {SCHEMA_PATH}")
with open(SCHEMA_PATH, "r") as f:
    schema = yaml.safe_load(f)

# Expected columns from schema
groups = ["binary", "continuous", "categorical"]
expected_cols = set([schema.get("target", TARGET_NAME)])
for g in groups:
    expected_cols.update(schema.get(g, {}).get("columns", []))

missing_cols = sorted([c for c in expected_cols if c not in df.columns])
unexpected_cols = sorted([c for c in df.columns if c not in expected_cols])

# Binary columns should have exactly two unique values
binary_cols = schema.get("binary", {}).get("columns", [])
binary_not_two = []
for c in binary_cols:
    if c in df.columns:
        nunq = int(df[c].dropna().nunique())
        if nunq != 2:
            binary_not_two.append((c, nunq))

# Target sanity (schema’s target can override local TARGET_NAME)
schema_target = schema.get("target", TARGET_NAME)
if schema_target != TARGET_NAME:
    print(f"ℹ️ Using target from schema: {schema_target}")
    TARGET_NAME = schema_target

# --------- Report ----------
row_count, col_count = df.shape
print("\n📋 Schema Consistency Report")
print(f"Rows: {row_count:,}  |  Cols: {col_count}")
print(f"Target: {TARGET_NAME}")

if missing_cols:
    print(f"\n❌ Missing columns ({len(missing_cols)}):")
    for c in missing_cols: print(f"  - {c}")
else:
    print("\n✅ No missing columns vs schema")

if binary_not_two:
    print(f"\n❌ Binary columns not 2-unique ({len(binary_not_two)}):")
    for c, n in binary_not_two: print(f"  - {c} (nunique={n})")
else:
    print("✅ All binary columns are 2-unique")

if unexpected_cols:
    print(f"\n⚠️ Unexpected columns ({len(unexpected_cols)}):")
    for c in unexpected_cols: print(f"  - {c}")
else:
    print("✅ No unexpected columns")

# Class balance
counts = df[TARGET_NAME].value_counts()
ratio = counts.get(1, 0) / counts.sum()
print(f"\n📊 Churn Balance: {counts.to_dict()}  →  {ratio*100:.1f}% churn rate")
if ratio < 0.2 or ratio > 0.8:
    print("⚠️ Imbalanced — use stratify=y or class_weight='balanced'.")

# --------- Exit behavior (notebook-friendly) ----------
critical = bool(missing_cols or binary_not_two)
status = "FAIL" if critical else ("WARN" if unexpected_cols else "OK")
print(f"\nStatus: {status}")

if critical and RAISE_ON_CRITICAL:
    raise RuntimeError("Schema validation failed (critical issues above).")
```


---
---

# Telco Churn Analysis Configuration

# Data paths
data:
  raw_data_path: "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
  processed_data_path: "data/processed/telco_processed.csv"
  interim_data_path: "data/interim/"

# Output paths
output:
  reports_dir: "reports/"
  figures_dir: "reports/figures/"
  models_dir: "models/trained_models/"

# Data preprocessing
preprocessing:
  drop_columns:
    - "customerID"
  binary_columns:
    - "gender"
    - "Partner"
    - "Dependents"
    - "PhoneService"
    - "PaperlessBilling"
  target_column: "Churn"
  handle_missing:
    strategy: "fill"
    fill_value: 0

# Feature engineering
features:
  tenure_bins: [0, 12, 24, 48, 72]
  tenure_labels: ["0-1 year", "1-2 years", "2-4 years", "4+ years"]
  charge_bins: [0, 35, 65, 90, 120]
  charge_labels: ["Low", "Medium", "High", "Very High"]
  service_columns:
    - "PhoneService"
    - "MultipleLines"
    - "InternetService"
    - "OnlineSecurity"
    - "OnlineBackup"
    - "DeviceProtection"
    - "TechSupport"
    - "StreamingTV"
    - "StreamingMovies"
  create_interactions: true

# Model training
training:
  test_size: 0.2
  random_state: 42
  cv_folds: 5
  tune_hyperparameters: false
  
  # Numerical columns to scale
  numerical_columns:
    - "tenure"
    - "MonthlyCharges"
    - "TotalCharges"
    - "total_services"
    - "avg_charge_per_service"
    - "customer_value_score"
  
  # Model configurations
  models:
    logistic_regression:
      enabled: true
      needs_scaling: true
      hyperparameters:
        C: [0.01, 0.1, 1, 10]
        penalty: ["l2"]
        solver: ["lbfgs"]
    
    random_forest:
      enabled: true
      needs_scaling: false
      hyperparameters:
        n_estimators: [50, 100, 200]
        max_depth: [10, 20, null]
        min_samples_split: [2, 5, 10]
    
    gradient_boosting:
      enabled: true
      needs_scaling: false
      hyperparameters:
        n_estimators: [50, 100, 150]
        learning_rate: [0.01, 0.1, 0.2]
        max_depth: [3, 5, 7]

# Evaluation
evaluation:
  metrics:
    - "accuracy"
    - "precision"
    - "recall"
    - "f1_score"
    - "roc_auc"
  threshold: 0.5
  save_confusion_matrix: true
  save_roc_curve: true

# Visualization
visualization:
  style: "whitegrid"
  figsize: [12, 6]
  dpi: 300
  colors:
    no_churn: "#2ecc71"
    churn: "#e74c3c"
  
  plots:
    target_distribution: true
    categorical_churn: true
    numerical_distributions: true
    correlation_matrix: true
    model_comparison: true
    confusion_matrices: true
    feature_importance: true

# Logging
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  save_to_file: true
  log_file: "logs/pipeline.log"

# =====
Project root: /Users/b/DATA/PROJECTS/Telco
Dataset: /Users/b/DATA/PROJECTS/Telco/resources/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
Figures: /Users/b/DATA/PROJECTS/Telco/Level_3/figures
Reports: /Users/b/DATA/PROJECTS/Telco/Level_3/reports


Project root: /Users/b/DATA/PROJECTS/Telco
Dataset: /Users/b/DATA/PROJECTS/Telco/resources/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
Figures: /Users/b/DATA/PROJECTS/Telco/Level_3/figures
Reports: /Users/b/DATA/PROJECTS/Telco/Level_3/reports


---
---
---

02_Data_Validation_and_Cleaning:
  description: >
    Validate schema, ensure logical consistency, clean data, and export a verified dataset
    for downstream analysis. Produces validation reports and baseline statistics.

  tasks:
    - [ ] 1. Introduction
      - [ ] 1.1 Purpose of the notebook
      - [ ] 1.2 Input and output paths (raw → cleaned dataset)
      - [ ] 1.3 Overview of validation and cleaning scope

    - [ ] 2. Schema and Data Type Checks
      - [ ] 2.1 Load schema from configs/schema.yaml
      - [ ] 2.2 Verify required columns are present
      - [ ] 2.3 Detect unexpected or missing columns
      - [ ] 2.4 Validate data types against schema
      - [ ] 2.5 Coerce or flag mismatched dtypes

    - [ ] 3. Missing and Empty Value Analysis
      - [ ] 3.1 Count missing (NaN) and empty string values
      - [ ] 3.2 Identify columns with high missingness
      - [ ] 3.3 Visualize missingness (bar chart / heatmap)
      - [ ] 3.4 Decide drop / imputation strategy

    - [ ] 4. Primary-Key & Uniqueness Checks
      - [ ] 4.1 Verify customerID exists and is unique
      - [ ] 4.2 Identify / resolve duplicate rows (define tie-break rule)

    - [ ] 5. Target Column & Leakage Guard
      - [ ] 5.1 Validate Churn values (allowed set, casing, missing)
      - [ ] 5.2 Scan for leakage columns (“churn”, “cancel”, etc.)

    - [ ] 6. Value Range & Outlier Sanity Checks
      - [ ] 6.1 Assert numeric bounds (MonthlyCharges ≥ 0, tenure ≥ 0, TotalCharges ≥ 0)
      - [ ] 6.2 Flag extreme outliers (IQR / z-score)

    - [ ] 7. Categorical Hygiene & Cardinality
      - [ ] 7.1 Normalize casing / whitespace
      - [ ] 7.2 Check high-cardinality categories (warn if > threshold)
      - [ ] 7.3 Validate expected label sets (Contract, PaymentMethod, InternetService)

    - [ ] 8. Logical Consistency Checks
      - [ ] 8.1 Validate tenure vs TotalCharges relationship
      - [ ] 8.2 Ensure MonthlyCharges ≥ 0
      - [ ] 8.3 Check contract-type consistency
      - [ ] 8.4 Detect inconsistent categorical labels
      - [ ] 8.5 Flag anomalies and prepare issue log

    - [ ] 9. Data Cleaning and Standardization
      - [ ] 9.1 Handle missing / invalid values (drop or impute)
      - [ ] 9.2 Correct inconsistent labels and whitespace
      - [ ] 9.3 Convert numeric columns stored as strings (TotalCharges)
      - [ ] 9.4 Normalize categorical values and data formats
      - [ ] 9.5 Remove duplicate records

    - [ ] 10. Readable Before / After Delta Table
      - [ ] 10.1 Compare rows, columns, nulls, invalids pre vs post
      - [ ] 10.2 Summarize row impact (kept / dropped / coerced)

    - [ ] 11. Issue Log & Data Quality Score
      - [ ] 11.1 Write issue log CSV (id, column, rule, severity)
      - [ ] 11.2 Compute DQ score (% rows passing all rules)

    - [ ] 12. Baseline Statistics Export
      - [ ] 12.1 Save column summary stats (mean, median, std, freq tables)
      - [ ] 12.2 Export to reports/baseline_stats.json

    - [ ] 13. Reproducibility & Provenance
      - [ ] 13.1 Snapshot schema.yaml into report
      - [ ] 13.2 Record library versions (pandas, python, OS)
      - [ ] 13.3 (Optional) Hash inputs/outputs (SHA-256)

    - [ ] 14. Minimal Contract / Assertions (Optional)
      - [ ] 14.1 Add assert checks (row count > 0, no NA in customerID)
      - [ ] 14.2 (Optional) Validate subset with Pandera schema

    - [ ] 15. Validation Summary & Export Clean Dataset
      - [ ] 15.1 Summarize issues pre/post cleaning
      - [ ] 15.2 Record counts fixed, dropped, or coerced
      - [ ] 15.3 Save dataset → data/processed/telco_clean.csv
      - [ ] 15.4 Export validation report → reports/validation_summary.json
      - [ ] 15.5 Confirm schema alignment and record count

  outputs:
    - data/processed/telco_clean.csv
    - reports/validation_summary.json
    - reports/ba

---


---
---
```yaml

<details>
<summary style="
    cursor:pointer;background:#f7f7fb;border: 1px solid #e5e7eb;
    padding:10px 12px;border-radius:10px;font-weight:900;">
➡︎ ☞ ➤ ⟿ Suggestions for config
</summary>

```yaml
# 📦 project_config.yaml
# * IBM Telco Churn Project * Config Hub
#  Purpose:
#   Single source of truth for paths, thresholds, and schema expectations.
#   Loaded in Section 1 (Environment Setup) → used throughout Section 2–3.

# TODO: in order for config.get to work > update vars to strict/semantic
  # strict_dtypes = CONFIG.get("SCHEMA_EXPECTED_DTYPES_STRICT", {})
  # semantic_dtypes = CONFIG.get("SCHEMA_EXPECTED_DTYPES_SEMANTIC", {})
  # use with def C
  # strict_dtypes = C("SCHEMA_EXPECTED_DTYPES_STRICT", {})
  # semantic_dtypes = C("SCHEMA_EXPECTED_DTYPES_SEMANTIC", {})

DRIFT:
  # 💡💡 Baseline snapshot for numeric profile — used by 2.3.14 drift checks
  #      This is where we store the "golden run" numeric_profile that future runs compare against.
  BASELINE_NUMERIC_PROFILE: "Level_3/resources/artifacts/baseline/numeric_profile_baseline.csv"
  # 💡💡 Drift thresholds — aligned with 2.3.14 drift_severity rules
  PSI_WARN: 0.10      # moderate drift
  PSI_FAIL: 0.25      # severe drift
  KS_WARN: 0.10       # moderate KS
  KS_FAIL: 0.20       # severe KS

META:
  PROJECT_NAME: "Telco Customer Churn"
  VERSION: "1.0"
  LAST_UPDATED: "2025-11-11"

READ_OPTS:
  encoding: "utf-8"
  na_values: ["", " ", "NA", "NaN"]
  keep_default_na: true
  low_memory: false

# strict pandas dtypes
SCHEMA_EXPECTED_DTYPES_STRICT:
  customerID: object
  tenure: int64
  MonthlyCharges: float64
  TotalCharges: float64
  Churn: object
  Churn_flag: Int8

# semantic version
SCHEMA_EXPECTED_DTYPES_SEMANTIC:
  customerID: string
  gender: category
  SeniorCitizen: int
  Partner: category
  Dependents: category
  PhoneService: category
  PaperlessBilling: category
  MultipleLines: category
  DeviceProtection: category
  OnlineBackup: category
  OnlineSecurity: category
  TechSupport: category
  StreamingMovies: category
  StreamingTV: category
  tenure: int
  MonthlyCharges: float
  TotalCharges: float

PATHS:
  RAW_DATA: "resources/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
  PROCESSED: "resources/data/processed/"
  ARTIFACTS: "Level_3/resources/artifacts/"
  REPORTS: "Level_3/resources/reports/"
  FIGURES: "Level_3/resources/figures/"
  MODELS: "Level_3/resources/models/"
  OUTPUTS: "Level_3/resources/outputs/"

TARGET:
  COLUMN: "Churn_flag"
  RAW_COLUMN: "Churn"
  POSITIVE_CLASS: "Yes"
  NEGATIVE_CLASS: "No"

KEYS:
  PRIMARY_KEYS:
    telco_customer: ["customerID"]

  FOREIGN_KEYS:
    fk_customer_to_dim:
      fk_col: "customerID"           # column in df
      ref_table: "CUSTOMER_DIM"      # name of a ref DataFrame in globals()/REF_TABLES, # must map to a DataFrame
      ref_col: "customerID"          # in CUSTOMER_DIM / PK column in that ref table
      max_unmatched_pct: 0.01         # fraction, e.g. 0.01 = 1% allowed



    # fk_customer:
    #   fk_col: customerID
    #   ref_table: CUSTOMER_DIM
    #   ref_col: customer_id
    #   max_unmatched_pct: 0.001

# LOGIC (2.5.3-2.5.6)
LOGIC_RULES:
  MUTUAL_EXCLUSION:
    no_multiple_lines_without_phone:
      description: "Cannot have MultipleLines when PhoneService == 'No'."
      columns: ["PhoneService", "MultipleLines"]
      # BAD state: no phone service, but MultipleLines says anything other than 'No phone service'
      violation_expr: "PhoneService == 'No' and MultipleLines != 'No phone service'"

    no_no_phone_service_when_phone_yes:
      description: "If PhoneService == 'Yes', MultipleLines cannot be 'No phone service'."
      columns: ["PhoneService", "MultipleLines"]
      # BAD state: PhoneService says they DO have phone, but MultipleLines claims 'No phone service'.
      violation_expr: "PhoneService == 'Yes' and MultipleLines == 'No phone service'"

    no_internet_addons_without_internet:
      description: "If InternetService == 'No', all internet add-ons must be 'No internet service'."
      columns:
        - "InternetService"
        - "OnlineSecurity"
        - "OnlineBackup"
        - "DeviceProtection"
        - "TechSupport"
        - "StreamingTV"
        - "StreamingMovies"
      # BAD state: claims no internet, but some add-on is active or not 'No internet service'
      violation_expr: >
        InternetService == 'No' and (
          OnlineSecurity != 'No internet service' or
          OnlineBackup != 'No internet service' or
          DeviceProtection != 'No internet service' or
          TechSupport != 'No internet service' or
          StreamingTV != 'No internet service' or
          StreamingMovies != 'No internet service'
        )

    no_no_internet_flag_when_internet_present:
      description: "If InternetService is DSL/Fiber, add-ons cannot say 'No internet service'."
      columns:
        - "InternetService"
        - "OnlineSecurity"
        - "OnlineBackup"
        - "DeviceProtection"
        - "TechSupport"
        - "StreamingTV"
        - "StreamingMovies"
      # BAD state: says they DO have internet, but some add-on claims 'No internet service'.
      violation_expr: >
        InternetService != 'No' and (
          OnlineSecurity == 'No internet service' or
          OnlineBackup == 'No internet service' or
          DeviceProtection == 'No internet service' or
          TechSupport == 'No internet service' or
          StreamingTV == 'No internet service' or
          StreamingMovies == 'No internet service'
        )

  DEPENDENCIES:
    # CORE RULE:
    tenure_requires_total_charges:
      description: "If tenure > 0, TotalCharges should not be null"
      columns: ["tenure", "TotalCharges"]
      if: "tenure > 0"
      then: "TotalCharges.notna()"

    zero_monthly_implies_no_services:
      description: "If MonthlyCharges == 0, customer should have no phone or internet service."
      columns: ["MonthlyCharges", "PhoneService", "InternetService"]
      if: "MonthlyCharges == 0"
      then: "(PhoneService == 'No') and (InternetService == 'No')"

    contract_implies_positive_tenure:
      description: "If Contract is not 'Month-to-month', tenure should be > 0."
      columns: ["Contract", "tenure"]
      if: "Contract != 'Month-to-month'"
      then: "tenure > 0"

    total_charges_requires_monthly:
      description: "If TotalCharges > 0, MonthlyCharges should also be > 0."
      columns: ["TotalCharges", "MonthlyCharges"]
      if: "TotalCharges > 0"
      then: "MonthlyCharges > 0"

  RATIO_CHECKS:
    total_vs_mc_tenure:
      description: "TotalCharges ≈ MonthlyCharges * tenure"
      lhs: "TotalCharges"
      rhs_expr: "MonthlyCharges * tenure"
      max_rel_error: 0.2
      max_abs_error: 20.0

###
TEMPORAL:
  # 0–2 typical?
  FUTURE_GRACE_DAYS: 0
  MIN_DATE: "1999-01-01"
  INTERVALS:
    tenure_interval:
      start_col: "pseudo_start"
      end_col: "pseudo_end"
      min_duration: 0
      max_duration: 3650     # 10 years, which is 120 months
      unit: "days"
    call_duration:
      start_col: "call_start_ts"
      end_col: "call_end_ts"
      min_duration: 0        # no negative calls
      max_duration: 360      # max 6 hours
      unit: "minutes"
    contract_lifetime:
      start_col: "contract_start_date"
      end_col: "contract_end_date"
      min_duration: 0
      max_duration: 3650     # 10 years
      unit: "days"

###
ANOMALY_CONTEXT:
  INCLUDE_SEVERITIES: ["warn", "fail"]
  MAX_ROWS: 500
  RUN_ID: null

  SOURCES:
    dependency_rule_violation:
      path: "dependency_violations.csv"
      format: "csv"
      row_key_col: "customerID"
      rule_id_col: "rule_name"
      anomaly_type: "dependency_violation"
      feature_cols: ["columns_involved"]
      severity_col: "severity"
      magnitude_col: "n_violations"
      section_ref: "2.5.4"

    dependency_row_violation:
      path: "dependency_row_violations.csv"
      format: "csv"
      row_key_col: "row_key"          # or "customerID" if you prefer
      rule_id_col: "rule_id"
      anomaly_type: "dependency_violation"
      feature_cols: ["left_col", "right_col"]
      severity_col: "severity"
      magnitude_col: "magnitude"
      section_ref: "2.5.test"

    mutual_exclusion_violation:
      path: "mutual_exclusion_report.csv"
      format: "csv"
      row_key_col: "customerID"
      rule_id_col: "rule_id"
      anomaly_type: "mutual_exclusion"
      severity_col: "severity"
      feature_cols: ["columns"]
      section_ref: "2.5.3"

    ratio_check_violation:
      path: "ratio_consistency_report.csv"
      format: "csv"
      row_key_col: "customerID"
      rule_id_col: "ratio_rule"
      anomaly_type: "ratio_violation"
      severity_col: "severity"
      feature_cols: ["lhs", "rhs_expr"]
      section_ref: "2.5.5"

    temporal_violation:
      path: "temporal_logic_report.csv"
      format: "csv"
      row_key_col: "customerID"
      rule_id_col: "interval_name"
      anomaly_type: "temporal_violation"
      feature_cols: ["start_col", "end_col"]
      severity_col: "severity"
      section_ref: "2.5.6"

    onehot_integrity_violation:
      path: "onehot_integrity_report.csv"
      format: "csv"
      row_key_col: "customerID"
      rule_id_col: "group_id"
      anomaly_type: "onehot_violation"
      feature_cols: ["columns"]
      severity_col: "severity"
      section_ref: "2.5.8"

    # 3.2 Numeric Drift (PSI per numeric feature)
    drift_numeric_psi:
      path: "numeric_drift_psi.csv"
      format: "csv"
      row_key_col: "feature"          # becomes row_key in 2.5.11
      rule_id_col: "feature"          # reused as rule_id
      anomaly_type: "numeric_drift"
      feature_cols: ["feature"]
      severity_col: "severity"
      magnitude_col: "psi"            # PSI used as magnitude
      section_ref: "3.2"

    # 3.3 Categorical Drift (PSI per categorical feature)
    drift_categorical_psi:
      path: "categorical_drift_psi.csv"
      format: "csv"
      row_key_col: "feature"
      rule_id_col: "feature"
      anomaly_type: "categorical_drift"
      feature_cols: ["feature"]
      severity_col: "severity"
      magnitude_col: "psi"
      section_ref: "3.3"

    # 3.4 Logic Drift (dependency rule violation deltas)
    drift_logic_dependency:
      path: "logic_drift_dependency.csv"
      format: "csv"
      row_key_col: "rule_name"                 # becomes row_key
      rule_id_col: "rule_name"
      anomaly_type: "logic_drift_dependency"
      feature_cols: ["rule_name"]
      severity_col: "severity"
      magnitude_col: "delta_violations"        # how much the rule changed
      section_ref: "3.4"

#########
DASHBOARD:
  LOGIC:
    ENABLED: true
    # Which high-level sections this dashboard is supposed to summarize
    INCLUDE_SECTIONS: ["2.3", "2.4", "2.5"]
    # Max rows to show in HTML tables (model/logic readiness, summary)
    LIMITS:
      MODEL_READINESS_ROWS: 20
      LOGIC_READINESS_ROWS: 20
      SECTION2_SUMMARY_ROWS: 40
      CONTRACTS_ROWS: 50
    # Panel toggles (future use – you can wire these into the HTML builder later)
    PANELS:
      SHOW_MODEL_READINESS: true
      SHOW_LOGIC_READINESS: true
      SHOW_CONTRACTS: true
      SHOW_SECTION2_SUMMARY: true
      SHOW_NUMERIC_DRIFT_KPI: true
      SHOW_RARE_CATEGORY_KPI: true
      SHOW_LOGIC_GRAPH_IMAGE: false   # once you embed PNG from 2.5.10

###############
INTEGRITY_INDEX:
  RUN_ID: null   # Optional: custom run ID label for 2.5.17

  WEIGHTS:
    # How much each sub-score contributes to the final 0–100 index.
    # These are relative weights, *not* required to sum to 1.0
    numeric: 0.30         # (placeholder until you wire numeric readiness)
    categorical: 0.30     # from model_readiness_report.csv
    logic: 0.30           # from logic_readiness_report.csv + 2.5.12
    contract_modifier: 0.10  # how strongly contract penalties affect the score

  CONTRACT_PENALTIES:
    # Status → penalty in points (multiplied by contract_modifier)
    OK: 0         # no change
    WARN: -10     # mild downgrade
    FAIL: -25     # strong downgrade

################
CATNUM_ALIGNMENT:
  ENABLED: true   # Toggle this whole 2.5.7 layer on/off
  THRESHOLDS:
    max_violating_pairs_pct: 0.2   # Maximum fraction of category pairs that can break monotonic pattern
    min_group_size: 50             # Minimum rows per category to trust comparison
  RULES:
    contract_vs_monthly:
      group_col: "Contract"
      numeric_col: "MonthlyCharges"
      expectation: "monotonic_decreasing"
      group_order:
        - "Month-to-month"
        - "One year"
        - "Two year"

    senior_discount:
      group_col: "SeniorCitizen"
      numeric_col: "MonthlyCharges"
      expectation: "group_1 <= group_0"

    internet_vs_monthly:
      group_col: "InternetService"
      numeric_col: "MonthlyCharges"
      expectation: "monotonic_increasing"
      group_order:
        - "No"
        - "DSL"
        - "Fiber optic"

    tenure_bucket_vs_monthly:
      group_col: "tenure_bucket"
      numeric_col: "MonthlyCharges"
      expectation: "monotonic_increasing"
      group_order:
        - "0-12"
        - "13-24"
        - "25-48"
        - "49-72"

    paymentmethod_vs_monthly:
      group_col: "PaymentMethod"
      numeric_col: "MonthlyCharges"
      expectation: "monotonic_increasing"
      group_order:
        - "Mailed check"
        - "Electronic check"
        - "Bank transfer (automatic)"
        - "Credit card (automatic)"

# REAL COLUMNS (DUMMY)
ONEHOT:
  GROUPS:
    contract_type:
      mode: "mutually_exclusive"
      columns:
        - "ContractType_Month-to-month"
        - "ContractType_One year"
        - "ContractType_Two year"
    internet_service:
      mode: "mutually_exclusive"
      columns:
        - "InternetService_No"
        - "InternetService_DSL"
        - "InternetService_Fiber optic"
    payment_method:
      mode: "mutually_exclusive"
      columns:
        - "PaymentMethod_Mailed check"
        - "PaymentMethod_Electronic check"
        - "PaymentMethod_Bank transfer (automatic)"
        - "PaymentMethod_Credit card (automatic)"

TOTALS:
  RULES:
    total_vs_expected_from_tenure_monthly:
      description: "TotalCharges ≈ expected_total_from_tenure_monthly (tenure × MonthlyCharges)"
      total_col: "TotalCharges"
      component_cols: ["expected_total_from_tenure_monthly"]
      tolerance_abs: 50.0
      tolerance_rel: 0.20

    zero_tenure_zero_total:
      description: "Rows with tenure ≈ 0 should have near-zero TotalCharges"
      total_col: "TotalCharges"
      component_cols: ["expected_total_for_zero_tenure"]
      tolerance_abs: 5.0
      tolerance_rel: 0.25

    contract_bounded_total:
      description: "TotalCharges should not fall below contract-implied minimum"
      total_col: "TotalCharges"
      component_cols: ["expected_min_total_from_contract"]
      tolerance_abs: 50.0
      tolerance_rel: 0.20

    senior_citizen_pricing_consistency:
      description: "Senior citizens' TotalCharges are consistent with expected billing"
      total_col: "TotalCharges"
      component_cols: ["expected_total_senior"]
      tolerance_abs: 75.0
      tolerance_rel: 0.25

    payment_method_consistency:
      description: "TotalCharges align with payment-method-specific expected pattern"
      total_col: "TotalCharges"
      component_cols: ["expected_total_from_payment_profile"]
      tolerance_abs: 40.0
      tolerance_rel: 0.15

##########
ID_COLUMNS:
  - "customerID"

FLAGS:
  RAISE_ON_CRITICAL: true
  SAVE_LOGS: true
  ENABLE_COLOR_OUTPUT: true

RANGES:
  tenure:          {min: 0,   max: 120}
  MonthlyCharges:  {min: 0,   max: 1000}
  TotalCharges:    {min: 0,   max: 100000}

DATA_QUALITY:
  NUMERIC_LIKE_THRESHOLD: 0.95
  RARE_PCT_THRESHOLD: 0.5
  RARE_MIN_COUNT: 5
  HIGH_CARD_THRESHOLD: 50
  NEARLY_CONST_THRESHOLD: 0.98
  SUSPECT_TOKENS:
    - "?"
    - "unknown"
    - "unk"
    - "n/a"
    - "na"
    - "n.a."
    - "null"
    - "none"
    - "missing"
    - "-"
    - "--"
    - "_"
    - "tbd"

MISSING_VALUES:
  MAX_NULL_FRACTION_TO_IMPUTE: 0.4
  STRATEGIES:
    NUMERIC:
      default: median
      overrides:
        TotalCharges: zero

# Telco: TotalCharges repair + logic-aware fixes
LOGIC_REPAIR:
  ENABLED: true
  TAG_COLUMN: "_logic_repair_applied"
  DEFAULT_STRATEGY: "flag_only"   # rules without explicit action will just flag
  RULES:
    tenure_requires_totalcharges_fill_zero:
      description: "If tenure > 0 and TotalCharges is null, fill TotalCharges with 0."
      if: "(tenure > 0) & (TotalCharges.isna())"
      action: "set_zero"
      columns_to_fix: ["TotalCharges"]

    tenure_zero_total_zero:
      description: "If tenure == 0 and TotalCharges is non-null and non-zero, force it to 0."
      if: "(tenure == 0) & (TotalCharges.notna()) & (TotalCharges != 0)"
      action: "set_zero"
      columns_to_fix: ["TotalCharges"]

DERIVED_FEATURES:
  ENABLED: true
  FEATURES:
    tenure_months_bucket:
      expr: "pd.cut(tenure, bins=[0,12,24,36,60,999], labels=['0-12','12-24','24-36','36-60','60+'])"
    total_charges_per_month:
      expr: "TotalCharges / (tenure.replace({0: np.nan}))"
    avg_streaming_spend:
      expr: "(StreamingMoviesCharges + StreamingTVCharges) / max(1, StreamingServicesCount)"

ENCODING_PLAN:
  ENABLED: true
  GLOBAL_DEFAULT: "one_hot"    # OR: "ordinal"
  STRATEGIES:
    LOW_CARDINALITY_MAX: 10
    HIGH_CARDINALITY_THRESHOLD: 50
    METHODS:
      ONE_HOT: ["Contract", "InternetService", "Partner", "Dependents"]
      ORDINAL: ["tenure_bucket"]
      TARGET: ["PaymentMethod"]
  EXCLUDE:
    - "customerID"

EXPECTED_LEVELS:
  gender: ["Female", "Male"]
  SeniorCitizen: ["0", "1"]
  Partner: ["Yes", "No"]
  Dependents: ["Yes", "No"]
  PhoneService: ["Yes", "No"]
  MultipleLines: ["Yes", "No", "No phone service"]
  InternetService: ["DSL", "Fiber optic", "No"]
  OnlineSecurity: ["Yes", "No", "No internet service"]
  OnlineBackup: ["Yes", "No", "No internet service"]
  DeviceProtection: ["Yes", "No", "No internet service"]
  TechSupport: ["Yes", "No", "No internet service"]
  StreamingTV: ["Yes", "No", "No internet service"]
  StreamingMovies: ["Yes", "No", "No internet service"]
  Contract: ["Month-to-month", "One year", "Two year"]
  PaperlessBilling: ["Yes", "No"]
  PaymentMethod:
    - "Electronic check"
    - "Mailed check"
    - "Bank transfer (automatic)"
    - "Credit card (automatic)"
  Churn: ["Yes", "No"]

CROSS_FIELD_TOLERANCES:
  total_vs_mc_tenure:
    tol_abs: 5.0
    tol_rel: 0.02

LOGGING:
  ENABLED: true
  FORMAT: "%(asctime)s | %(levelname)s | %(message)s"
  LEVEL: "INFO"
  SAVE_TO: "Level_3/resources/reports/section2_data_quality_log.txt"

DATA_CONTRACTS:
  # --------------------------------------------------------------------------
  # 1) BASIC NUMERIC HYGIENE (MISSINGNESS / INTEGRITY)
  # --------------------------------------------------------------------------
  - name: "numeric_nulls_under_5pct_for_features"
    description: "All numeric model features must have <= 5% missing values."
    scope: "numeric_profile"          # uses numeric_profile_df.csv
    severity: "hard"                  # failing this should FAIL the run
    where:
      role: "feature"
    target: "null_pct"
    op: "<="
    threshold: 5.0

  - name: "no_critical_numeric_integrity"
    description: "No numeric column is allowed to have critical integrity status."
    scope: "numeric_integrity"
    severity: "hard"
    target: "numeric_integrity_status"
    op: "!="
    value: "critical"

  - name: "warn_if_many_warn_integrity"
    description: "Warn if more than 30% of numeric columns are in 'warn' status."
    scope: "numeric_integrity"
    severity: "soft"
    target: "numeric_integrity_status"
    op: "fraction_eq"
    value: "warn"
    max_fraction: 0.30

  # --------------------------------------------------------------------------
  # 2) TELCO-SPECIFIC RANGES / SPECIAL CASES
  # --------------------------------------------------------------------------
  - name: "senior_citizen_is_binary"
    description: "SeniorCitizen must only contain 0/1 values (no weird codes)."
    scope: "numeric_profile"
    severity: "hard"
    where:
      column: "SeniorCitizen"
    target: "n_unique"
    op: "<="
    threshold: 2

  - name: "total_charges_not_too_sparse"
    description: "TotalCharges should not be missing for more than 2% of rows."
    scope: "numeric_profile"
    severity: "hard"
    where:
      column: "TotalCharges"
    target: "null_pct"
    op: "<="
    threshold: 2.0

  - name: "tenure_has_reasonable_nulls"
    description: "tenure allowed small nulls but should be under 1%."
    scope: "numeric_profile"
    severity: "soft"
    where:
      column: "tenure"
    target: "null_pct"
    op: "<="
    threshold: 1.0

  # --------------------------------------------------------------------------
  # 3) MODEL READINESS CONTRACTS
  # --------------------------------------------------------------------------
  - name: "most_features_readiness_above_0_7"
    description: "At least 80% of model features must have readiness_score >= 0.7."
    scope: "readiness"
    severity: "hard"
    target: "readiness_score"
    op: "fraction_ge"
    threshold: 0.7
    min_fraction: 0.80

  - name: "no_feature_with_readiness_below_0_4"
    description: "There should be no catastrophically bad features (readiness < 0.4)."
    scope: "readiness"
    severity: "hard"
    target: "readiness_score"
    op: ">="
    threshold: 0.4

  - name: "warn_if_many_low_readiness"
    description: "Warn if more than 25% of features have readiness_score < 0.6."
    scope: "readiness"
    severity: "soft"
    target: "readiness_score"
    op: "fraction_lt"
    threshold: 0.6
    max_fraction: 0.25

  # --------------------------------------------------------------------------
  # 4) DRIFT CONTRACTS (PSI / KS)
  # --------------------------------------------------------------------------
  - name: "psi_under_0_25_for_features"
    description: "No model feature should exhibit extreme drift (PSI ≥ 0.25)."
    scope: "drift"
    severity: "hard"
    target: "psi"
    op: "<"
    threshold: 0.25

  - name: "psi_warn_if_many_features_above_0_1"
    description: "Warn if more than 30% of features have PSI ≥ 0.1 (moderate drift)."
    scope: "drift"
    severity: "soft"
    target: "psi"
    op: "fraction_ge"
    threshold: 0.10
    max_fraction: 0.30

  - name: "ks_under_0_2_for_features"
    description: "No feature should have KS statistic ≥ 0.2 vs baseline."
    scope: "drift"
    severity: "hard"
    target: "ks_stat"
    op: "<"
    threshold: 0.20

  # --------------------------------------------------------------------------
  # 5) JOINT READINESS + DRIFT GUARDRAILS
  # --------------------------------------------------------------------------
  - name: "no_high_drift_low_readiness_features"
    description: "For safety, forbid features that are both high-drift and low-readiness."
    scope: "drift"
    severity: "hard"
    target: "drift_severity"
    op: "not_any_in"
    values:
      - "high_low_readiness"

  # --------------------------------------------------------------------------
  # 6) GLOBAL RUN HEALTH CONTRACT (AGGREGATED VIEW)
  # --------------------------------------------------------------------------
  - name: "run_overall_contract_health"
    description: "Global health expectations: no hard contract should fail."
    scope: "contracts"
    severity: "hard"
    target: "hard_contract_failures"
    op: "=="
    value: 0
```