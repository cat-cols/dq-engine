# 2.0.1 🧾 Reporting Bootstrap & Environment Readiness
# (2.0.1.1-.5) Build SECTION2_REPORT_PATH: Guard globals, directories, CONFIG roots, df shape
print("\n📋 2.0.1 Part A ⚙️ Environment & Config Readiness Check")

# -- 1) 🧾 Unified Section 2 Data Quality report path
assert "SECTION2_REPORT_PATH" in globals(), ("❌ SECTION2_REPORT_PATH missing. Run Bootstrap in 2.0.0 first.")
print(f"🧾 Unified Section 2 report → {SECTION2_REPORT_PATH}")

# -- 2) Verify required globals (no C here)
required_globals = [
    "PROJECT_ROOT",
    "CONFIG",
    "RAW_DATA",
    "REPORTS_DIR",
    "ARTIFACTS_DIR",
    "FIGURES_DIR",
    "MODELS_DIR",
    "OUTPUTS_DIR",
    "df",
]

missing_globals = [g for g in required_globals if g not in globals()]
if missing_globals:
    raise RuntimeError(
        f"❌ Section 2 preflight failed — missing globals from Section 1/2 bootstrap: "
        f"{', '.join(missing_globals)}"
    )

# -- 3) Directory readiness
core_dirs = {
    "REPORTS_DIR":   REPORTS_DIR,
    "ARTIFACTS_DIR": ARTIFACTS_DIR,
    "FIGURES_DIR":   FIGURES_DIR,
    "MODELS_DIR":    MODELS_DIR,
    "OUTPUTS_DIR":   OUTPUTS_DIR,
}

for name, d in core_dirs.items():
    if not isinstance(d, Path):
        raise TypeError(f"❌ {name} is not a pathlib.Path: {d!r}")
    d.mkdir(parents=True, exist_ok=True)

# -- 4) Required CONFIG roots for Section 2
required_roots = ["TARGET", "ID_COLUMNS", "RANGES", "DATA_QUALITY"]

missing_roots = [r for r in required_roots if r not in CONFIG]
if missing_roots:
    raise KeyError(
        f"❌ Section 2 requires config roots missing from CONFIG: {', '.join(missing_roots)}"
    )

if "FLAGS" not in CONFIG:
    print("⚠️ CONFIG.FLAGS missing (optional). Using code defaults where needed.")

# -- 5) Working DataFrame sanity
n_rows, n_cols = df.shape
if n_rows == 0 or n_cols == 0:
    raise ValueError(f"❌ 'df' is empty, shape={df.shape}. Section 2 cannot proceed.")

# ✅ Summary printout
print("\n✅ Section 2 preflight OK.")
print(f"   • shape: {n_rows:,} rows × {n_cols:,} columns")
print(f"   • PROJECT_ROOT: {PROJECT_ROOT}")
print(f"   • REPORTS_DIR:  {REPORTS_DIR}")
print(f"   • CONFIG roots confirmed: {', '.join(required_roots)}")
print(f"   • Unified Section 2 report: {SECTION2_REPORT_PATH}")

# -- 7) 🧾 Log preflight summary into unified Section 2 report (INLINE APPEND)
summary_201 = pd.DataFrame([{
        "section":      "2.0.1",
        "section_name": "Environment & config readiness preflight",
        "check":        "Environment & config readiness preflight",
        "level":        "info",
        "n_rows":       n_rows,
        "n_cols":       n_cols,
        "status":       "OK",
        "detail":       [("Section 2 bootstrap complete: globals, directories, "
            "CONFIG roots, and working df are all ready.")],
        "timestamp":    pd.Timestamp.now(),
}])

display(summary_201)

# ✅ Use shared helper and track usage for metrics
append_sec2(summary_201, SECTION2_REPORT_PATH)
SECTION2_APPEND_SECTIONS.add("2.0.1")  # this section now counted in refactor stats

# OUTPUT:
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:155: DtypeWarning: Columns (0,1,9,15,19,20,31,32,33,34,35,36,47,261,262,269,271,272,279,284,286,287,293) have mixed types. Specify dtype option on import or set low_memory=False.
  existing = pd.read_csv(path)
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:166: PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
  chunk[c] = pd.NA
/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:173: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
  out = pd.concat(
🧾 Appended diagnostics → /Users/b/DATA/PROJECTS/Telco/_T2/Level_3/resources/reports/section2/section2_report.csv

# Telco/Level_3/src/telco_churn/utils/reporting.py
from __future__ import annotations

from pathlib import Path
import os
from typing import Union
from datetime import datetime, timezone
import pandas as pd
from collections.abc import Mapping
from typing import Any
import json

# Columns we often want numerically coerced & rounded in the unified Section 2 report
_NUMERIC_NORMALIZE_COLS = (
    "percent",
    "imbalance_ratio",
    "pct_inconsistent",
    "top_freq",
    "pct_not_allowed",
)


def append_sec2(
    chunk: pd.DataFrame,
    report_path: str | Path,
    track_sections: bool = True,
) -> Path:
    path = Path(report_path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Coerce incoming chunk to DataFrame
    if chunk is None:
        chunk = pd.DataFrame()
    elif not isinstance(chunk, pd.DataFrame):
        chunk = pd.DataFrame(chunk)

    # If chunk truly empty, nothing to append
    if chunk.empty:
        return path

    # Normalize detail column to JSON strings
    if "detail" in chunk.columns:
        chunk["detail"] = chunk["detail"].apply(
            lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
        )

    # Load existing report if it exists and is non-empty
    existing = None
    if path.exists() and path.stat().st_size > 0:
        try:
            existing = pd.read_csv(path)
        except Exception:
            existing = None

    # If no existing, write chunk as the report (atomic)
    if existing is None or existing.empty:
        out = chunk.copy()
    else:
        # Align schemas both ways before concat to avoid dtype inference on all-NA extras
        for c in existing.columns:
            if c not in chunk.columns:
                chunk[c] = pd.NA
        for c in chunk.columns:
            if c not in existing.columns:
                existing[c] = pd.NA

        # Reorder chunk columns to match existing first, then any new columns
        ordered_cols = list(existing.columns) + [c for c in chunk.columns if c not in existing.columns]
        out = pd.concat(
            [existing.reindex(columns=ordered_cols), chunk.reindex(columns=ordered_cols)],
            ignore_index=True,
            sort=False,
        )

    # Optional numeric normalization
    try:
        for col in _NUMERIC_NORMALIZE_COLS:
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce").round(4)
    except Exception:
        pass

    # Atomic write
    try:
        out.to_csv(tmp_path, index=False)
        os.replace(tmp_path, path)
        print(f"🧾 Appended diagnostics → {path}")
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass

    # Track section IDs
    if track_sections:
        try:
            sec_ids = (
                chunk["section"].dropna().astype(str).unique().tolist()
                if "section" in chunk.columns
                else []
            )
        except Exception:
            sec_ids = []

        if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
            try:
                if isinstance(SECTION2_APPEND_SECTIONS, set):
                    SECTION2_APPEND_SECTIONS.update(sec_ids)
            except Exception:
                pass

    return path

Those warnings come from two things in `append_sec2`:

1. **Fragmentation**: you do `chunk[c] = pd.NA` in a loop for hundreds of columns. That repeatedly inserts columns. Pandas warns.

2. **DtypeWarning + FutureWarning**: `pd.read_csv` sees mixed types, and `pd.concat` is deciding dtypes when you introduce all-NA columns.

Fix: never “insert” columns in a loop. Build a **single target column index**, `reindex` both frames once, and drop “new all-NA columns” from the incoming chunk before concat. Also read CSV with `low_memory=False`.

Replace `append_sec2` with this version:

```python
def append_sec2(
    chunk: pd.DataFrame,
    report_path: str | Path,
    track_sections: bool = True,
) -> Path:
    path = Path(report_path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    path.parent.mkdir(parents=True, exist_ok=True)

    # Coerce incoming chunk to DataFrame
    if chunk is None:
        chunk = pd.DataFrame()
    elif not isinstance(chunk, pd.DataFrame):
        chunk = pd.DataFrame(chunk)

    if chunk.empty:
        return path

    # Normalize detail column to JSON strings
    if "detail" in chunk.columns:
        chunk = chunk.copy()
        chunk["detail"] = chunk["detail"].apply(
            lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
        )

    # Load existing report (avoid mixed-type warning churn)
    existing = None
    if path.exists() and path.stat().st_size > 0:
        try:
            existing = pd.read_csv(path, low_memory=False)
        except Exception:
            existing = None

    if existing is None or existing.empty:
        out = chunk.copy()
    else:
        # Drop "new columns" that are entirely NA in chunk (prevents dtype/FutureWarning noise)
        new_cols = [c for c in chunk.columns if c not in existing.columns]
        if new_cols:
            drop_cols = [c for c in new_cols if chunk[c].isna().all()]
            if drop_cols:
                chunk = chunk.drop(columns=drop_cols)

        # Build final column order: keep existing order, then append new cols (no per-col inserts)
        final_cols = list(existing.columns) + [c for c in chunk.columns if c not in existing.columns]

        existing2 = existing.reindex(columns=final_cols)
        chunk2    = chunk.reindex(columns=final_cols)

        out = pd.concat([existing2, chunk2], ignore_index=True, sort=False)

    # Optional numeric normalization
    for col in _NUMERIC_NORMALIZE_COLS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

    # Atomic write
    try:
        out.to_csv(tmp_path, index=False)
        os.replace(tmp_path, path)
        print(f"🧾 Appended diagnostics → {path}")
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass

    # Track section IDs
    if track_sections:
        try:
            sec_ids = (
                chunk["section"].dropna().astype(str).unique().tolist()
                if "section" in chunk.columns
                else []
            )
        except Exception:
            sec_ids = []

        if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
            try:
                if isinstance(SECTION2_APPEND_SECTIONS, set):
                    SECTION2_APPEND_SECTIONS.update(sec_ids)
            except Exception:
                pass

    return path
```

Expected outcome:

* Fragmentation warning disappears (no repeated column inserts).
* DtypeWarning is much less likely (low_memory=False).
* FutureWarning about empty/all-NA concat is much less likely (drops new all-NA cols before concat).

💡💡 If you want the unified report to be *stable-typed* (no mixed columns ever), the next step is: maintain a “report schema” list in CONFIG and always `reindex` to that schema before writing. That fully eliminates mixed-type drift.
