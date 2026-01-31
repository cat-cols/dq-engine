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


# TODO: try this function
# def append_sec2(
    #     chunk: pd.DataFrame,
    #     report_path: str | Path,
    #     track_sections: bool = True,
    # ) -> Path:
    #     path = Path(report_path)
    #     tmp_path = path.with_suffix(path.suffix + ".tmp")

    #     try:
    #         path.parent.mkdir(parents=True, exist_ok=True)

    #         # --- Defensive: coerce incoming chunk to DataFrame ---
    #         if chunk is None:
    #             chunk = pd.DataFrame()
    #         if not isinstance(chunk, pd.DataFrame):
    #             chunk = pd.DataFrame(chunk)

    #         # If chunk is empty and report doesn't exist: nothing to do
    #         if chunk.empty and not path.exists():
    #             print(f"🧾 No diagnostics to append (empty chunk) → {path}")
    #             return path

    #         # --- Normalize common "nested" cells (lists/dicts) to strings (CSV-safe) ---
    #         # This prevents mixed object columns over time (and helps avoid concat dtype edge cases).
    #         for col in chunk.columns:
    #             if chunk[col].map(lambda x: isinstance(x, (list, dict))).any():
    #                 chunk[col] = chunk[col].map(
    #                     lambda x: json.dumps(x, ensure_ascii=False)
    #                     if isinstance(x, (list, dict))
    #                     else x
    #                 )

    #         # --- Write new report if none exists ---
    #         if not path.exists():
    #             out = chunk.copy()

    #         else:
    #             # Read as strings; low_memory=False avoids DtypeWarning from chunked inference
    #             existing = pd.read_csv(
    #                 path,
    #                 dtype="string",
    #                 keep_default_na=False,
    #                 low_memory=False,
    #             )

    #             # If existing is empty, just write chunk
    #             if existing.empty:
    #                 out = chunk.copy()

    #             else:
    #                 # Drop columns that are effectively empty on either side:
    #                 # 1) all NA
    #                 existing = existing.loc[:, existing.notna().any(axis=0)]
    #                 chunk    = chunk.loc[:, chunk.notna().any(axis=0)] if not chunk.empty else chunk

    #                 # 2) all "" (because keep_default_na=False means blanks are "")
    #                 existing = existing.loc[:, (existing != "").any(axis=0)]
    #                 chunk    = chunk.loc[:, (chunk    != "").any(axis=0)] if not chunk.empty else chunk

    #                 # Align schema explicitly (stable union)
    #                 all_cols = pd.Index(existing.columns).union(chunk.columns)
    #                 existing = existing.reindex(columns=all_cols)
    #                 chunk    = chunk.reindex(columns=all_cols)

    #                 out = pd.concat([existing, chunk], ignore_index=True, sort=False)

    #         # --- Optional: normalize known numeric columns (if present) ---
    #         for col in _NUMERIC_NORMALIZE_COLS:
    #             if col in out.columns:
    #                 out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

    #         out.to_csv(tmp_path, index=False)
    #         os.replace(tmp_path, path)
    #         print(f"🧾 Appended diagnostics → {path}")

    #         # --- Track section IDs (optional) ---
    #         if track_sections:
    #             try:
    #                 sec_ids = (
    #                     chunk["section"].dropna().astype(str).unique().tolist()
    #                     if "section" in chunk.columns
    #                     else []
    #                 )
    #             except Exception:
    #                 sec_ids = []

    #             if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
    #                 if isinstance(SECTION2_APPEND_SECTIONS, set):
    #                     SECTION2_APPEND_SECTIONS.update(sec_ids)

    #     except Exception as e:
    #         if tmp_path.exists():
    #             try:
    #                 tmp_path.unlink()
    #             except Exception:
    #                 pass
    #         print(f"⚠️ Could not append diagnostics: {e}")

    #     return path

# def append_sec2(
#     chunk: pd.DataFrame,
#     report_path: str | Path,
#     track_sections: bool = True,
# ) -> Path:
#     path = Path(report_path)
#     tmp_path = path.with_suffix(path.suffix + ".tmp")

#     # Ensure directory exists
#     path.parent.mkdir(parents=True, exist_ok=True)

#     # Coerce incoming chunk to DataFrame
#     if chunk is None:
#         chunk = pd.DataFrame()
#     elif not isinstance(chunk, pd.DataFrame):
#         chunk = pd.DataFrame(chunk)

#     # If chunk truly empty, nothing to append
#     if chunk.empty:
#         return path

#     # Normalize detail column to JSON strings
#     if "detail" in chunk.columns:
#         chunk["detail"] = chunk["detail"].apply(
#             lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
#         )

#     # Load existing report if it exists and is non-empty
#     existing = None
#     if path.exists() and path.stat().st_size > 0:
#         try:
#             existing = pd.read_csv(path)
#         except Exception:
#             existing = None

#     # If no existing, write chunk as the report (atomic)
#     if existing is None or existing.empty:
#         out = chunk.copy()
#     else:
#         # Align schemas both ways before concat to avoid dtype inference on all-NA extras
#         for c in existing.columns:
#             if c not in chunk.columns:
#                 chunk[c] = pd.NA
#         for c in chunk.columns:
#             if c not in existing.columns:
#                 existing[c] = pd.NA

#         # Reorder chunk columns to match existing first, then any new columns
#         ordered_cols = list(existing.columns) + [c for c in chunk.columns if c not in existing.columns]
#         out = pd.concat(
#             [existing.reindex(columns=ordered_cols), chunk.reindex(columns=ordered_cols)],
#             ignore_index=True,
#             sort=False,
#         )

#     # Optional numeric normalization
#     try:
#         for col in _NUMERIC_NORMALIZE_COLS:
#             if col in out.columns:
#                 out[col] = pd.to_numeric(out[col], errors="coerce").round(4)
#     except Exception:
#         pass

#     # Atomic write
#     try:
#         out.to_csv(tmp_path, index=False)
#         os.replace(tmp_path, path)
#         print(f"🧾 Appended diagnostics → {path}")
#     finally:
#         if tmp_path.exists():
#             try:
#                 tmp_path.unlink()
#             except Exception:
#                 pass

#     # Track section IDs
#     if track_sections:
#         try:
#             sec_ids = (
#                 chunk["section"].dropna().astype(str).unique().tolist()
#                 if "section" in chunk.columns
#                 else []
#             )
#         except Exception:
#             sec_ids = []
#         if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
#             try:
#                 if isinstance(SECTION2_APPEND_SECTIONS, set):
#                     SECTION2_APPEND_SECTIONS.update(sec_ids)
#             except Exception:
#                 pass
#     return path


# Create Reporting
# 2nd best version
    # def append_sec2(
    #     chunk: pd.DataFrame,
    #     report_path: str | Path,
    #     track_sections: bool = True,
    # ) -> Path:
    #     """
    #     Append a diagnostics chunk into the unified Section 2 report CSV.

    #     Parameters
    #     ----------
    #     chunk:
    #         1+ row DataFrame with Section 2 diagnostics.
    #         Expected to have a 'section' column like '2.1.2'.
    #     report_path:
    #         Path to the unified Section 2 CSV
    #         (usually SECTION2_REPORT_PATH from the notebook).
    #     track_sections:
    #         If True, automatically add the chunk's section IDs into
    #         SECTION2_APPEND_SECTIONS (a global set), if present.

    #     Behaviour
    #     ---------
    #     * Ensures parent directory exists
    #     * If the report exists, merges columns and appends rows
    #     * Writes through a temporary file and uses os.replace for atomicity
    #     * Normalizes a few numeric columns if present
    #     * Optionally tracks which sections have appended diagnostics
    #     """

    #     path = Path(report_path)
    #     tmp_path = path.with_suffix(path.suffix + ".tmp")

    #     try:
    #         path.parent.mkdir(parents=True, exist_ok=True)

    #         if path.exists():
    #             existing_df = pd.read_csv(path, dtype="string", keep_default_na=False)
    #             all_cols = pd.Index(existing_df.columns).union(chunk.columns)

    #             # existing: existing_df (read from CSV) and new_df (the row(s) you’re appending)
    #             # 1) If existing is empty, just write new directly (avoids concat edge case)
    #             if existing_df is None or existing_df.empty:
    #                 out = new_df.copy()
    #             else:
    #                 # 2) Drop all-NA columns on BOTH sides to avoid FutureWarning + keep dtypes stable
    #                 existing_df = existing_df.dropna(axis=1, how="all")
    #                 new_df = new_df.dropna(axis=1, how="all")

    #                 # 3) Concat
    #                 out = pd.concat([existing_df, new_df], ignore_index=True, sort=False)

    #         # Optional: normalize some known numeric columns if present
    #         for col in _NUMERIC_NORMALIZE_COLS:
    #             if col in out.columns:
    #                 out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

    #         out.to_csv(tmp_path, index=False)
    #         os.replace(tmp_path, path)
    #         print(f"🧾 Appended diagnostics → {path}")

    #         # 🔗 Optional: track which sections have appended diagnostics
    #         if track_sections:
    #             try:
    #                 # grab section IDs from the chunk, if present
    #                 if "section" in chunk.columns:
    #                     sec_ids = (
    #                         chunk["section"]
    #                         .dropna()
    #                         .astype(str)
    #                         .unique()
    #                         .tolist()
    #                     )
    #                 else:
    #                     sec_ids = []
    #             except Exception:
    #                 sec_ids = []

    #             if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
    #                 # Only update if it's a set-like object
    #                 if isinstance(SECTION2_APPEND_SECTIONS, set):
    #                     SECTION2_APPEND_SECTIONS.update(sec_ids)

    #     except Exception as e:
    #         if tmp_path.exists():
    #             try:
    #                 tmp_path.unlink()
    #             except Exception:
    #                 pass
    #         print(f"⚠️ Could not append diagnostics: {e}")

    #     return path

# 3rd best version
    # def append_sec2(
    #     chunk: pd.DataFrame,
    #     report_path: str | Path,
    # ) -> Path:
    #     """
    #     Append a diagnostics chunk into the unified Section 2 report CSV.

    #     Parameters
    #     ----------
    #     chunk:
    #         1+ row DataFrame with Section 2 diagnostics.
    #     report_path:
    #         Path to the unified Section 2 CSV
    #         (usually SECTION2_REPORT_PATH from the notebook).

    #     Behaviour
    #     ---------
    #     * Ensures parent directory exists
    #     * If the report exists, merges columns and appends rows
    #     * Writes through a temporary file and uses os.replace for atomicity
    #     * Normalizes a few numeric columns if present
    #     """

    #     path = Path(report_path)
    #     tmp_path = path.with_suffix(path.suffix + ".tmp")

    #     try:
    #         path.parent.mkdir(parents=True, exist_ok=True)

    #         if path.exists():
    #             existing = pd.read_csv(path)
    #             all_cols = pd.Index(existing.columns).union(chunk.columns)
    #             out = pd.concat(
    #                 [
    #                     existing.reindex(columns=all_cols),
    #                     chunk.reindex(columns=all_cols),
    #                 ],
    #                 ignore_index=True,
    #             )
    #         else:
    #             out = chunk.copy()

    #         # Optional: normalize some known numeric columns if present
    #         for col in _NUMERIC_NORMALIZE_COLS:
    #             if col in out.columns:
    #                 out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

    #         out.to_csv(tmp_path, index=False)
    #         os.replace(tmp_path, path)
    #         print(f"🧾 Appended diagnostics → {path}")
    #     except Exception as e:
    #         if tmp_path.exists():
    #             try:
    #                 tmp_path.unlink()
    #             except Exception:
    #                 pass
    #         print(f"⚠️ Could not append diagnostics: {e}")

    #     return path


# 1
def log_section_completion(
    section: str,
    status: str,
    *,
    run_id: str | None = None,
    level: str = "info",
    log_dir: str | Path | None = None,
    log_name: str = "section2_runlog.jsonl",
    extra: Mapping[str, Any] | None = None,
    **metrics: Any,
) -> None:
    """
    Lightweight Section 2 logger.

    - Always prints a concise console line.
    - Optionally appends a JSONL record to a run log.

    Parameters
    ----------
    section:
        Section identifier, e.g. "2.1.5".
    status:
        Status string, e.g. "OK", "WARN", "FAIL", "SKIP".
    run_id:
        Optional run identifier (e.g. SECTION2_RUN_ID) to tie sections to a single run.
    level:
        Log level string. Mostly for future use ("info", "warn", "error").
    log_dir:
        If provided, JSONL will be appended to `log_dir / log_name`.
        If None, only console output is produced.
    log_name:
        File name for the JSONL run log (default: "section2_runlog.jsonl").
    extra:
        Optional mapping of additional metadata that should be included in the record.
    **metrics:
        Arbitrary key/value metrics, e.g. checked=..., mismatched=...
    """
    ts_utc = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )

    # Build record
    record: dict[str, Any] = {
        "timestamp_utc": ts_utc,
        "section": section,
        "status": status,
        "level": level,
    }
    if run_id is not None:
        record["run_id"] = run_id

    if extra:
        record.update(dict(extra))

    if metrics:
        record["metrics"] = dict(metrics)

    # ---- Console output (human friendly) -----------------------------------
    # Example: ✅ [2.1.5] status=OK | checked=21 | mismatched=0
    parts = [f"✅ [{section}]", f"status={status}"]
    for k, v in (metrics or {}).items():
        parts.append(f"{k}={v}")
    print(" | ".join(parts))

    # ---- Optional JSONL logging --------------------------------------------
    if log_dir is None:
        return

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_name

    try:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        # We never want logging failures to break the notebook
        print(f"⚠️ log_section_completion: failed to write to {log_path}: {e}")

# TODO: add inline version first?

# V2 most simple?
#   # def log_section_completion(section: str, status: str, **metrics) -> None:
    #     """
    #     Lightweight console logger for Section 2 cells.
    #     Example:
    #       log_section_completion("2.x.x", status_2xx, checked=n_cols, mismatched=n_unassigned)
    #     """
    #     parts = [f"✅ [{section}]", f"status={status}"]
    #     for k, v in metrics.items():
    #         parts.append(f"{k}={v}")
    #     print(" | ".join(parts))


# V3 log section completion
def log_section_completion(
    section: str,
    status: str,
    *,
    checked: int | None = None,
    mismatched: int | None = None,
    notes: str | None = None,
    out_dir: str | Path | None = None,
) -> Path:
    """
    Write a small JSON completion record for a section.
    - Always safe to call.
    - Atomic write.
    """
    out_dir = Path(out_dir) if out_dir is not None else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "section": str(section),
        "status": str(status),
        "checked": int(checked) if checked is not None else None,
        "mismatched": int(mismatched) if mismatched is not None else None,
        "notes": notes,
        "timestamp_utc": datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"),
    }

    path = (out_dir / f"section_{section.replace('.', '_')}_completion.json").resolve()
    tmp = path.with_suffix(".tmp.json")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, path)
    return path


# 2 log section completion
    # def log_section_completion(
    #     section: str,
    #     status: str,
    #     *,
    #     run_id: str | None = None,
    #     level: str = "info",
    #     log_dir: str | Path | None = None,
    #     log_name: str = "section2_runlog.jsonl",
    #     extra: Mapping[str, Any] | None = None,
    #     **metrics: Any,
    # ) -> None:
    #     """
    #     Lightweight Section 2 logger.

    #     - Always prints a concise console line.
    #     - Optionally appends a JSONL record to a run log.
    #     """
    #     ts_utc = (
    #         datetime.now(timezone.utc)
    #         .isoformat(timespec="seconds")
    #         .replace("+00:00", "Z")
    #     )

    #     # Build record
    #     record: dict[str, Any] = {
    #         "timestamp_utc": ts_utc,
    #         "section": section,
    #         "status": status,
    #         "level": level,
    #     }
    #     if run_id is not None:
    #         record["run_id"] = run_id

    #     if extra:
    #         record.update(dict(extra))

    #     if metrics:
    #         record["metrics"] = dict(metrics)

    #     # ---- Console output (human friendly) -----------------------------------
    #     parts = [f"✅ [{section}]", f"status={status}"]
    #     for k, v in (metrics or {}).items():
    #         parts.append(f"{k}={v}")
    #     print(" | ".join(parts))

    #     # ---- Optional JSONL logging --------------------------------------------
    #     if log_dir is None:
    #         return

    #     log_dir = Path(log_dir)
    #     log_dir.mkdir(parents=True, exist_ok=True)
    #     log_path = log_dir / log_name

    #     try:
    #         with log_path.open("a", encoding="utf-8") as f:
    #             f.write(json.dumps(record, ensure_ascii=False) + "\n")
    #     except Exception as e:
    #         # We never want logging failures to break the notebook
    #         print(f"⚠️ log_section_completion: failed to write to {log_path}: {e}")


####################
#### DEPRECATED ####
####################

# # 2 append sec2
    # def append_sec2(
    #     chunk: pd.DataFrame,
    #     report_path: Union[str, Path],
    # ) -> Path:
    #     """
    #     Append a diagnostics chunk into the unified Section 2 report CSV.

    #     - `chunk` is a 1+ row DataFrame with Section 2 diagnostics.
    #     - `report_path` is the path to the unified Section 2 CSV
    #     (usually SECTION2_REPORT_PATH from the notebook).

    #     Behaviour:
    #     * Ensures parent directory exists
    #     * If the report exists, merges columns and appends rows
    #     * Writes through a temporary file and uses os.replace for atomicity
    #     * Normalizes a few numeric columns if present
    #     """
    #     path = Path(report_path)
    #     tmp_path = path.with_suffix(path.suffix + ".tmp")

    #     try:
    #         path.parent.mkdir(parents=True, exist_ok=True)

    #         if path.exists():
    #             existing = pd.read_csv(path)
    #             all_cols = pd.Index(existing.columns).union(chunk.columns)
    #             out = pd.concat(
    #                 [
    #                     existing.reindex(columns=all_cols),
    #                     chunk.reindex(columns=all_cols),
    #                 ],
    #                 ignore_index=True,
    #             )
    #         else:
    #             out = chunk.copy()

    #         # Optional: normalize some known numeric columns if present
    #         for col in _NUMERIC_NORMALIZE_COLS:
    #             if col in out.columns:
    #                 out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

    #         out.to_csv(tmp_path, index=False)
    #         os.replace(tmp_path, path)
    #         print(f"🧾 Appended diagnostics → {path}")
    #     except Exception as e:
    #         if tmp_path.exists():
    #             try:
    #                 tmp_path.unlink()
    #             except Exception:
    #                 pass
    #         print(f"⚠️ Could not append diagnostics: {e}")

    #     return path

    # from pathlib import Path
    # import os
    # import pandas as pd

    # from __future__ import annotations

    # from pathlib import Path
    # import os
    # from typing import Iterable

    # import pandas as pd

    # _NUMERIC_NORMALIZE_COLS: Iterable[str] = (
    #     "percent",
    #     "imbalance_ratio",
    #     "pct_inconsistent",
    #     "top_freq",
    #     "pct_not_allowed",
    # )

# # 2 log section completion
    #     def log_section_completion(section: str, status: str, **metrics) -> None:
    #         """
    #         Lightweight console logger for Section 2 cells.
    #         Example:
    #           log_section_completion("2.x.x", status_2xx, checked=n_cols, mismatched=n_unassigned)
    #         """
    #         parts = [f"✅ [{section}]", f"status={status}"]
    #         for k, v in metrics.items():
    #             parts.append(f"{k}={v}")
    #         print(" | ".join(parts))

