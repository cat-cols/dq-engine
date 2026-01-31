# NEW 2.3.7.1 | Time-Series Outliers
print("\n2.3.7.1 ⏱️ Time-series outliers")

time_series_rows_2371 = []
n_features_checked_2371 = 0
n_time_outliers_2371 = 0
ran_ts_2371 = False  # track whether we actually ran temporal analysis

if has_time_col_237 and numeric_cols_237:
    df_ts_2371 = df[[time_col_237] + numeric_cols_237].copy()
    df_ts_2371[time_col_237] = pd.to_datetime(df_ts_2371[time_col_237], errors="coerce")

    # Drop rows with invalid time
    df_ts_2371 = df_ts_2371[df_ts_2371[time_col_237].notna()]
    if df_ts_2371.empty:
        print("⚠️ All values in time column are NaT after parsing — no time-series analysis run for 2.3.7.1.")
    else:
        ran_ts_2371 = True

        # Build time buckets (e.g. '2021-01')
        time_bucket_series_2371 = df_ts_2371[time_col_237].dt.to_period(time_bucket_237).astype("string")
        df_ts_2371 = df_ts_2371.assign(time_bucket=time_bucket_series_2371)

        # Aggregate mean per bucket
        bucket_means_2371 = (
            df_ts_2371
            .groupby("time_bucket", as_index=False)[numeric_cols_237]
            .mean()
        )

        # optional global for reuse in later cells
        bucket_df_237 = bucket_means_2371.copy()

        for col in numeric_cols_237:
            series_col = bucket_means_2371[col]
            valid_mask = series_col.notna()
            series_valid = series_col[valid_mask]

            if series_valid.shape[0] < 3:
                continue

            mean_val = float(series_valid.mean())
            std_val = float(series_valid.std(ddof=0))

            if std_val == 0 or pd.isna(std_val):
                continue

            n_features_checked_2371 += 1

            z_scores = (series_valid - mean_val) / std_val

            for idx in series_valid.index:
                tb_label = bucket_means_2371.loc[idx, "time_bucket"]
                bucket_mean = float(series_valid.loc[idx])
                z_val = float(z_scores.loc[idx])
                is_outlier = bool(abs(z_val) > z_thresh_bucket_237)

                if is_outlier:
                    n_time_outliers_2371 += 1

                time_series_rows_2371.append(
                    {
                        "feature":      col,
                        "time_bucket":  tb_label,
                        "metric_mean":  bucket_mean,
                        "z_score":      z_val,
                        "is_outlier":   is_outlier,
                    }
                )
else:
    if not has_time_col_237:
        print(f"⚠️ Time column '{time_col_237}' not found — no time-series analysis run for 2.3.7.1.")
    if not numeric_cols_237:
        print("⚠️ No numeric columns available — no time-series analysis run for 2.3.7.1.")

# Build DF and persist, even if empty
time_series_outliers_df_2371 = pd.DataFrame(time_series_rows_2371)

time_series_outliers_path = NUMERIC_DIR / "time_series_outliers.csv"
tmp_2371 = time_series_outliers_path.with_suffix(".tmp.csv")
time_series_outliers_df_2371.to_csv(tmp_2371, index=False)
os.replace(tmp_2371, time_series_outliers_path)

print(f"💾 Wrote time-series outliers → {time_series_outliers_path}")

# Status logic
if not ran_ts_2371:
    status_2371 = "SKIP"
else:
    status_2371 = "OK" if n_time_outliers_2371 == 0 else "WARN"

summary_2371 = pd.DataFrame([{
    "section":           "2.3.7.1",
    "section_name":      "Time-series outliers",
    "check":             "Bucketed temporal outliers per numeric feature",
    "level":             "info",
    "status":            status_2371,
    "n_features_checked":int(n_features_checked_2371),
    "n_time_outliers":   int(n_time_outliers_2371),
    "time_column":       time_col_237,
    "time_bucket":       time_bucket_237,
    "detail":            f"time_series_outliers.csv under {NUMERIC_DIR.name}",
    "timestamp":         pd.Timestamp.utcnow(),
}])

print("\n📊 2.3.7.1 time-series outliers (top 20 by |z|):")
if ran_ts_2371 and not time_series_outliers_df_2371.empty:
    ts_out_df_2371 = (
        time_series_outliers_df_2371
        .assign(abs_z=lambda d: d["z_score"].abs())
        .sort_values("abs_z", ascending=False)
    )
    preview_2371 = ts_out_df_2371.head(20)[
        ["feature", "time_bucket", "metric_mean", "z_score", "is_outlier"]
    ]
    display(preview_2371)
elif not ran_ts_2371:
    print("   (section skipped — missing time column or numeric columns)")
else:
    print("   (no time-series outliers detected)")

append_sec2(summary_2371, SECTION2_REPORT_PATH)
display(summary_2371)

print("✅ 2.3.7.1 complete.")

2.3.7.1 ⏱️ Time-series outliers
⚠️ Time column 'as_of_date' not found — no time-series analysis run for 2.3.7.1.
💾 Wrote time-series outliers → /Users/b/DATA/PROJECTS/Telco/Level_3/resources/reports/section2/numeric/time_series_outliers.csv

📊 2.3.7.1 time-series outliers (top 20 by |z|):
   (section skipped — missing time column or numeric columns)
🧾 Appended diagnostics → /Users/b/DATA/PROJECTS/Telco/Level_3/resources/reports/section2/section2_data_quality_20251210_155900.csv

How should I begun to be able to fix this on my own without help? What are the considerations that would make debugging this easier for me in the future?

Right now nothing is actually “broken” in that cell — it’s doing exactly what you told it to do:

* Look for `TEMPORAL.TIME_COLUMN` (defaults to `"as_of_date"`),
* Notice that column **doesn’t exist** in `df`,
* Log a ⚠️ and **skip** the analysis,
* Still emit an empty artifact + a SKIP row into `section2_data_quality_…csv`.

So the “debugging” story here is really:

> *Is the behavior I’m seeing what I intended? If not, where did my intent and my code/data/config get out of sync?*

Here’s how you can get better and faster at answering that question yourself.

---

## 1. Build a tiny debugging checklist for each Section 2 node

For a cell like **2.3.7.1**, you can literally keep a mental (or markdown) checklist:

1. **Check inputs / preconditions**

   ```python
   df.shape
   df.columns.tolist()
   time_col_237, has_time_col_237
   numeric_cols_237[:10]
   ```

   If `has_time_col_237` is `False` and you *expected* a time column, you already know where to look: config vs data.

2. **Check config vs reality**

   ```python
   C("TEMPORAL.TIME_COLUMN", "as_of_date")
   ```

   * Is that the column name you actually have?
   * Should it be `"tenure"`, `"InvoiceDate"`, `"ServiceDate"`, etc. instead?

3. **Check control flags / status variables**
   For time-series logic:

   ```python
   ran_ts_2371
   n_features_checked_2371
   n_time_outliers_2371
   ```

   * If `ran_ts_2371 == False`, you *expect* a SKIP status and an empty file.
   * If `ran_ts_2371 == True` but counts are zero, maybe your z-threshold is too high.

💡💡 *Habit*: when something surprises you, print or inspect **exactly** the 3–5 variables that decide the branch (e.g., `has_time_col_237`, `numeric_cols_237`, `ran_ts_2371`).

---

## 2. Keep the “contract” in your head (or in comments)

Each Section 2 node has an implicit contract:

> *If inputs A, B, C exist → do work and write artifact X; otherwise → log clearly and SKIP.*

For 2.3.7.1 the contract is roughly:

* **Requires**:

  * A time column (config-driven).
  * At least one numeric feature.
* **Produces**:

  * `time_series_outliers.csv`
  * One summary row in `section2_data_quality_*.csv`.

When debugging, ask:

* Did the **requires** part hold? (No: you had no `as_of_date`).
* Did the **produces** part happen anyway in a reasonable degraded way? (Yes: SKIP row + empty CSV).

That way you can tell “this is a legit SKIP” vs “this is a bug.”

💡💡 *Habit*: write a 1-line “Requires / Produces” comment at the top of each major cell. It trains you to think in contracts and makes debugging much easier months later.

---

## 3. Learn to trace from *symptom → decision point*

Your symptom here was just:

> “Why did it skip, and how would I fix it?”

Trace it like this:

1. **Symptom**: message
   `⚠️ Time column 'as_of_date' not found — no time-series analysis run for 2.3.7.1.`

2. **Find the branch** that prints that message:

   ```python
   if has_time_col_237 and numeric_cols_237:
       ...
   else:
       if not has_time_col_237:
           print(...)
   ```

3. **Inspect the condition variables**:

   ```python
   has_time_col_237, time_col_237
   numeric_cols_237
   ```

4. **Decide what’s wrong**:

   * If `time_col_237` is wrong → fix config (`TEMPORAL.TIME_COLUMN`).
   * If the column is missing in the raw CSV → fix your input data or earlier transformations.
   * If you *don’t* want temporal analysis for Telco at all → set a config flag to disable it, or accept SKIP as the “correct” outcome.

That 4-step trace (symptom → branch → variables → decision) is 90% of everyday debugging.

---

## 4. Make your life easier with “debug lenses”

Tiny, throwaway helpers can simplify your brain load. For example:

```python
def debug_temporal_prereqs(df):
    print("Time column from CONFIG:", C("TEMPORAL.TIME_COLUMN", "as_of_date"))
    print("Available columns:", df.columns.tolist())
    print("# numeric_cols_237:", len(numeric_cols_237))
    print("First 10 numeric cols:", numeric_cols_237[:10])
```

Call it right before the time-series block when something is weird. You don’t have to keep it forever, but having a “debug lens” pattern in your head is huge.

---

## 5. For *future* you, this tells a story, not just a stack trace

You already have:

* Guard `assert`s up top.
* Clear ⚠️ vs OK vs WARN vs SKIP.
* A single `append_sec2` row that summarizes the whole story.

So when something looks off, future-you can:

1. Open `section2_data_quality_*.csv`.
2. Filter to `section == "2.3.7.1"`.
3. Read the `status` and `detail` fields.
4. Jump back to the cell with that section number and inspect the handful of key variables.

That’s exactly the kind of structure that makes debugging *way* easier a year from now.

---

If you want, next step we can pick **one** more node (like 2.2.5 or 2.3.7.3) and I’ll walk you through a “debug rehearsal”: deliberately break a precondition and practice chasing it down using this checklist.
