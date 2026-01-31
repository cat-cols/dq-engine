> FutureWarning
> The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.

/Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/telco_churn/utils/reporting.py:62: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
  out = pd.concat([existing, chunk], ignore_index=True, sort=False)
🧾 Appended diagnostics → /Users/b/DATA/PROJECTS/Telco/_T2/Level_3/resources/reports/section2/section2_report.csv

That warning means **either `existing` or `chunk` still has at least one column that is “empty”** (all NA *or* effectively empty), and pandas is warning that concat’s dtype inference around those columns is changing in the future.

You can kill it deterministically by **excluding “all-empty” columns before concat** (on both sides), *then* aligning columns.

Since you read with `keep_default_na=False` (so blanks are `""`, not NA), you should drop columns that are **all `""` OR all NA**. Do this right before `pd.concat`.

Drop-in replacement for the concat block:

```python
# 2) Drop "empty" columns on BOTH sides BEFORE concat
# Empty means: all NA OR all "" (because keep_default_na=False makes blanks "")
existing = existing.loc[:, existing.notna().any(axis=0)]
chunk    = chunk.loc[:, chunk.notna().any(axis=0)] if not chunk.empty else chunk

existing = existing.loc[:, (existing != "").any(axis=0)]
chunk    = chunk.loc[:, (chunk    != "").any(axis=0)] if not chunk.empty else chunk

# 3) Align schema (union of remaining cols)
all_cols = pd.Index(existing.columns).union(chunk.columns)
existing = existing.reindex(columns=all_cols)
chunk    = chunk.reindex(columns=all_cols)

# 4) Concat (warning should be gone)
out = pd.concat([existing, chunk], ignore_index=True, sort=False)
```

If you want the *minimal* change (and you’re fine keeping blanks as blanks), this single line often fixes it:

```python
existing = existing.loc[:, (existing != "").any(axis=0)]
chunk    = chunk.loc[:, (chunk    != "").any(axis=0)]
```

### One more common cause in your notebook

You sometimes set `detail` to a **Python list** (`detail: [ "Baseline: ...", ... ]`). When that hits CSV, pandas may coerce weirdly across rows. A clean pattern is to force `detail` (and `notes`, etc.) to strings:

```python
if "detail" in chunk.columns:
    chunk["detail"] = chunk["detail"].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
```

If you paste your current `append_sec2` function (the exact version that’s producing the warning), I’ll edit it inline so you can copy/paste once and never see that warning again.
