# --- Auto-validation & summary writer (Level 3) ---
# Requires: pandas, numpy, pyyaml
import json, re, hashlib
from pathlib import Path
import pandas as pd
import numpy as np
import yaml

# ---- Load config & schema ----
with open("configs/schema.yaml") as f:
    SCHEMA = yaml.safe_load(f)
with open("configs/config.yaml") as f:
    CFG = yaml.safe_load(f)

RAW_PATH  = Path(CFG["data"]["raw_path"])
CLEAN_PATH = Path(CFG["data"]["processed_path"])
REPORTS_DIR = Path(CFG["data"]["reports_dir"])
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

ISSUE_LOG_CSV = Path(CFG["validation"]["issue_log_path"])
VALID_SUMMARY_JSON = Path(CFG["exports"]["validation_summary"])
BASELINE_STATS_JSON = Path(CFG["exports"]["baseline_stats"])
ENV_SNAPSHOT_JSON = Path(CFG["exports"]["environment_snapshot"])

# ---- Helpers ----
def _hash_file(path: Path) -> str:
    if not path.exists(): return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""): h.update(chunk)
    return h.hexdigest()

def as_category(x): return pd.Series(x, dtype="object")

# ---- Load data (pre-clean for “before”) and cleaned (if exists) ----
df_before = pd.read_csv(RAW_PATH)
df_after  = pd.read_csv(CLEAN_PATH) if CLEAN_PATH.exists() else None

# ---- Rule config from YAML ----
expected_dtypes = SCHEMA["expected_columns"]
required_cols   = set(SCHEMA["required_columns"])
allow_missing   = set(SCHEMA.get("allow_missing", []))
exp_cats        = SCHEMA.get("expected_categories", {})
num_bounds      = SCHEMA.get("numeric_bounds", {})
pk              = SCHEMA.get("primary_key")
target          = SCHEMA.get("target_column")

z_thr   = float(CFG["outlier_detection"]["zscore_threshold"])
iqr_k   = float(CFG["outlier_detection"]["iqr_multiplier"])
hi_card = int(CFG["categorical"]["high_cardinality_threshold"])

# ---- Issue log collector ----
issues = []  # rows: dict(id, column, rule, severity, details)

def log_issue(idx, column, rule, severity, details):
    issues.append({"id": idx, "column": column, "rule": rule, "severity": severity, "details": details})

# ---- 1) Schema & dtype checks ----
present_cols = set(df_before.columns)
missing_required = list(required_cols - present_cols)
unexpected_cols  = list(present_cols - set(expected_dtypes.keys()))
if missing_required:
    for c in missing_required:
        log_issue("ALL", c, "missing_required_column", "high", "Required column missing")

# Coercion attempt for numeric columns defined in schema
dfv = df_before.copy()
for col, dtype in expected_dtypes.items():
    if col not in dfv.columns: continue
    if dtype in ("float64","float32","int64","int32"):
        dfv[col] = pd.to_numeric(dfv[col], errors="coerce")
    elif dtype == "category":
        dfv[col] = dfv[col].astype("string")
    elif dtype == "string":
        dfv[col] = dfv[col].astype("string")

# Flag dtype mismatches post-coercion (informational at L3)
for col, dtype in expected_dtypes.items():
    if col not in dfv.columns: 
        continue
    got = str(dfv[col].dtype)
    # treat pandas 'string' and 'object' leniently for Level 3
    expected_group = "string_like" if dtype in ("string","category") else dtype
    got_group = "string_like" if got in ("object","string") else got
    if expected_group != got_group:
        log_issue("ALL", col, "dtype_mismatch", "medium", f"expected={dtype}, got={got}")

# ---- 2) Missing & empties ----
def count_empty_like(s: pd.Series):
    s2 = s.astype("string")
    return int(s2.isna().sum() + (s2 == "").sum() + (s2 == " ").sum())

missing_summary = {c: count_empty_like(dfv[c]) for c in dfv.columns if c in dfv}
for c, n in missing_summary.items():
    if n>0 and c not in allow_missing:
        log_issue("ALL", c, "missing_values", "medium", f"count={n}")

# ---- 3) Primary key & uniqueness ----
if pk and pk in dfv.columns:
    if dfv[pk].isna().any():
        log_issue("ALL", pk, "pk_nulls", "high", f"null_pk_count={int(dfv[pk].isna().sum())}")
    dup_ct = int(dfv.duplicated(pk).sum())
    if dup_ct>0:
        # record up to 5 duplicates
        dup_ids = dfv[dfv.duplicated(pk, keep=False)][pk].head(5).astype(str).tolist()
        log_issue("ALL", pk, "pk_duplicates", "high", f"duplicate_count={dup_ct}; examples={dup_ids}")

# ---- 4) Target and leakage guard ----
if target and target in dfv.columns:
    # Validate allowed set if provided
    allowed = set(exp_cats.get(target, []))
    if allowed:
        bad = dfv[~dfv[target].isin(allowed)][target].dropna().unique().tolist()
        if bad:
            log_issue("ALL", target, "invalid_target_labels", "high", f"bad_labels={bad}")
# Simple leakage scan via column names
leak_cols = [c for c in dfv.columns if re.search(r"(churn|cancel|termination|disconnect)", c, flags=re.I) and c!=target]
for c in leak_cols:
    log_issue("ALL", c, "potential_leakage_column", "high", "column name suggests leakage")

# ---- 5) Numeric bounds + Outliers (log only at L3) ----
for col, bounds in num_bounds.items():
    if col not in dfv.columns: continue
    s = pd.to_numeric(dfv[col], errors="coerce")
    below = int((s < bounds.get("min", -np.inf)).sum())
    above = int((s > bounds.get("max",  np.inf)).sum())
    if below or above:
        log_issue("ALL", col, "bounds_violation", "medium", f"below={below}, above={above}, bounds={bounds}")

    # z-score
    mu, sd = s.mean(), s.std(ddof=0)
    if sd and np.isfinite(sd):
        z_out = int(((s - mu).abs() > z_thr*sd).sum())
        if z_out>0:
            log_issue("ALL", col, "zscore_outliers", "low", f"count={z_out}, z_thr={z_thr}")
    # IQR
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    if pd.notna(iqr) and iqr>0:
        lo, hi = q1 - iqr_k*iqr, q3 + iqr_k*iqr
        iqr_out = int(((s < lo) | (s > hi)).sum())
        if iqr_out>0:
            log_issue("ALL", col, "iqr_outliers", "low", f"count={iqr_out}, iqr_k={iqr_k}")

# ---- 6) Categorical hygiene & cardinality ----
for col, allowed in exp_cats.items():
    if col not in dfv.columns: continue
    uniq = set(pd.Series(dfv[col], dtype="string").dropna().unique().tolist())
    bad  = sorted(list(uniq - set(allowed)))
    if bad:
        log_issue("ALL", col, "unexpected_categories", "medium", f"unexpected={bad}, expected={allowed}")

for col in dfv.select_dtypes(include=["object","string"]).columns:
    nunique = int(dfv[col].nunique(dropna=True))
    if nunique > hi_card:
        log_issue("ALL", col, "high_cardinality", "low", f"unique={nunique}, threshold={hi_card}")

# ---- 7) Logical consistency (example: tenure vs TotalCharges) ----
if {"tenure","TotalCharges"}.issubset(dfv.columns):
    t = pd.to_numeric(dfv["tenure"], errors="coerce")
    tc = pd.to_numeric(dfv["TotalCharges"], errors="coerce")
    bad = int(((t > 0) & ((tc <= 0) | tc.isna())).sum())
    if bad>0:
        log_issue("ALL", "tenure|TotalCharges", "logical_inconsistency", "medium",
                  f"tenure>0 but TotalCharges<=0/NaN count={bad}")

# ---- 8) Compute DQ score (simple) ----
# Define row-level pass as: required columns present, pk unique & non-null (if defined)
base_checks = []
base_checks.append(len(missing_required)==0)
if pk and pk in dfv.columns:
    base_checks.append((dfv[pk].notna().all()) and (dfv[pk].nunique(dropna=False)==len(dfv)))
dq_score = round(100.0 * (sum(base_checks)/len(base_checks) if base_checks else 1.0), 1)

# ---- 9) Write issue_log.csv ----
pd.DataFrame(issues).to_csv(ISSUE_LOG_CSV, index=False)

# ---- 10) Baseline stats (post-clean baseline comes later; here is “before”) ----
def baseline_stats(df: pd.DataFrame):
    out = {"numeric":{}, "categorical":{}}
    for c in df.columns:
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            out["numeric"][c] = {
                "count": int(s.count()), "mean": float(np.nanmean(s)),
                "std": float(np.nanstd(s)), "min": float(np.nanmin(s)),
                "p50": float(np.nanpercentile(s, 50)), "max": float(np.nanmax(s))
            }
        else:
            vc = s.astype("string").value_counts(dropna=True).head(20).to_dict()
            out["categorical"][c] = {"top_values": {str(k): int(v) for k,v in vc.items()}}
    return out

baseline_before = baseline_stats(dfv)
with open(BASELINE_STATS_JSON, "w") as f:
    json.dump(baseline_before, f, indent=2)

# ---- 11) Build validation_summary.json ----
summary = {
    "dataset": {
        "raw_path": str(RAW_PATH),
        "clean_path": str(CLEAN_PATH) if CLEAN_PATH.exists() else "",
        "rows_before": int(len(df_before)),
        "rows_after":  int(len(df_after)) if isinstance(df_after, pd.DataFrame) else None,
        "columns": list(df_before.columns),
    },
    "schema": {
        "missing_required_columns": missing_required,
        "unexpected_columns": unexpected_cols,
        "dtype_expected": expected_dtypes,
    },
    "quality": {
        "dq_score_percent": dq_score,
        "missing_counts": {k:int(v) for k,v in missing_summary.items()},
        "high_cardinality_threshold": hi_card,
    },
    "rules": {
        "numeric_bounds": num_bounds,
        "expected_categories": exp_cats,
        "primary_key": pk,
        "target_column": target,
        "leakage_name_hits": leak_cols,
        "outlier_params": {"zscore_threshold": z_thr, "iqr_multiplier": iqr_k},
    },
    "artifacts": {
        "issue_log_csv": str(ISSUE_LOG_CSV),
        "baseline_stats_json": str(BASELINE_STATS_JSON),
        "environment_snapshot_json": str(ENV_SNAPSHOT_JSON),
    },
    "provenance": {
        "raw_sha256": _hash_file(RAW_PATH),
        "clean_sha256": _hash_file(CLEAN_PATH) if CLEAN_PATH.exists() else "",
        "notes": "Hashes optional at Level 3; included when files exist.",
    }
}

with open(VALID_SUMMARY_JSON, "w") as f:
    json.dump(summary, f, indent=2)

print(f"✅ Wrote:\n- {VALID_SUMMARY_JSON}\n- {ISSUE_LOG_CSV}\n- {BASELINE_STATS_JSON}")
