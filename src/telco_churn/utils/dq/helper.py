# 2.0.0.5 helper functions
def _classify_dtype(dtype_str: str) -> str:
    s = dtype_str.lower()
    if "int" in s or "float" in s:
        return "numeric"
    if "bool" in s:
        return "boolean"
    if "datetime" in s or "date" in s:
        return "datetime"
    if "category" in s:
        return "categorical"
    return "string_like"

def _append_sec2(sec2_chunk: pd.DataFrame) -> str:
    """
    Append one or more diagnostic rows to the unified Section 2 CSV.

    Expects:
        - global SECTION2_REPORT_PATH (Path)
        - sec2_chunk is a DataFrame with at least ['section', 'check', 'status'] cols.

    Notes:
        - Uses SECTION2_REPORT_PATH (Path) as the single sink for all 2.x checks.
        - Performs schema union (outer) so later sections can add new columns safely.
        - Writes atomically via temp file + os.replace.
        - Returns the final report path as a string for logging / debugging.
    """
    path = SECTION2_REPORT_PATH
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        # Make sure the folder exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # If report already exists, read + align schema; otherwise start fresh
        if path.exists():
            existing = pd.read_csv(path)
            all_cols = pd.Index(existing.columns).union(sec2_chunk.columns)
            out = pd.concat(
                [
                    existing.reindex(columns=all_cols),
                    sec2_chunk.reindex(columns=all_cols),
                ],
                ignore_index=True,
            )
        else:
            out = sec2_chunk.copy()

        # Tidy numeric-like percentage fields (if they exist)
        for col in (
            "percent",
            "imbalance_ratio",
            "pct_inconsistent",
            "top_freq",
            "pct_not_allowed",
            "overall_null_pct",
            "top_missing_pct",
        ):
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

        # Atomic write: temp → replace
        out.to_csv(tmp_path, index=False)
        os.replace(tmp_path, path)

        print(f"🧾 Appended diagnostics → {path}")
        return str(path)

    except Exception as e:
        # Best-effort cleanup
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        print(f"⚠️ Could not append diagnostics: {e}")
        return str(path)

def C(path: str, default=None):
    """
    Dotted-path lookup into CONFIG.

    Example:
        C("PATHS.RAW_DATA")
        C("RANGES.tenure.max")
        C("TARGET.POSITIVE_CLASS", default="Yes")
    """
    node = CONFIG
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return node

# inline functions
# Utility: append a single-row or small DataFrame to the unified Section 2 report (atomic)
_path = SEC2_REPORTS_DIR
def _append_sec2(chunk_df: pd.DataFrame):
    tmp = _path.with_suffix(_path.suffix + ".tmp")
    _path.parent.mkdir(parents=True, exist_ok=True)
    if _path.exists():
        existing = pd.read_csv(_path)
        all_cols = pd.Index(existing.columns).union(chunk_df.columns)
        out = pd.concat(
            [existing.reindex(columns=all_cols), chunk_df.reindex(columns=all_cols)],
            ignore_index=True,
        )
    else:
        out = chunk_df.copy()
    out.to_csv(tmp, index=False)
    os.replace(tmp, _path)

# # # 2.0.0.0 helper functions
#2.0.0.1
# def append_sec2(sec2_chunk: pd.DataFrame) -> None:
#     path = SECTION2_REPORT_PATH
#     tmp_path = path.with_suffix(path.suffix + ".tmp")

#     try:
#         path.parent.mkdir(parents=True, exist_ok=True)
#         if path.exists():
#             existing = pd.read_csv(path)
#             all_cols = pd.Index(existing.columns).union(sec2_chunk.columns)
#             out = pd.concat(
#                 [
#                     existing.reindex(columns=all_cols),
#                     sec2_chunk.reindex(columns=all_cols),
#                 ],
#                 ignore_index=True,
#             )
#         else:
#             out = sec2_chunk.copy()

#         # optional percentage tidy, if you like that behavior
#         for col in (
#             "percent",
#             "imbalance_ratio",
#             "pct_inconsistent",
#             "top_freq",
#             "pct_not_allowed",
#         ):
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
# 2.0.0.2
# # Small helper reused across 2.0.5–2.0.6
# def _classify_dtype(dtype_str: str) -> str:
#     s = dtype_str.lower()
#     if "int" in s or "float" in s:
#         return "numeric"
#     if "bool" in s:
#         return "boolean"
#     if "datetime" in s or "date" in s:
#         return "datetime"
#     if "category" in s:
#         return "categorical"
#     return "string_like"

# def _classify_dtype(dtype_str: str) -> str:
#     s = dtype_str.lower()
#     if "int" in s or "float" in s:
#         return "numeric"
#     if "bool" in s:
#         return "boolean"
#     if "datetime" in s or "date" in s:
#         return "datetime"
#     if "category" in s:
#         return "categorical"
#     return "string_like"

# def _append_sec2(sec2_chunk: pd.DataFrame) -> str:
#     """
#     Append one or more diagnostic rows to the unified Section 2 CSV.

#     Expects:
#         - global SECTION2_REPORT_PATH (Path)
#         - sec2_chunk is a DataFrame with at least ['section', 'check', 'status'] cols.

#     Notes:
#         - Uses SECTION2_REPORT_PATH (Path) as the single sink for all 2.x checks.
#         - Performs schema union (outer) so later sections can add new columns safely.
#         - Writes atomically via temp file + os.replace.
#         - Returns the final report path as a string for logging / debugging.
#     """
#     path = SECTION2_REPORT_PATH
#     tmp_path = path.with_suffix(path.suffix + ".tmp")

#     try:
#         # Make sure the folder exists
#         path.parent.mkdir(parents=True, exist_ok=True)

#         # If report already exists, read + align schema; otherwise start fresh
#         if path.exists():
#             existing = pd.read_csv(path)
#             all_cols = pd.Index(existing.columns).union(sec2_chunk.columns)
#             out = pd.concat(
#                 [
#                     existing.reindex(columns=all_cols),
#                     sec2_chunk.reindex(columns=all_cols),
#                 ],
#                 ignore_index=True,
#             )
#         else:
#             out = sec2_chunk.copy()

#         # Tidy numeric-like percentage fields (if they exist)
#         for col in (
#             "percent",
#             "imbalance_ratio",
#             "pct_inconsistent",
#             "top_freq",
#             "pct_not_allowed",
#             "overall_null_pct",
#             "top_missing_pct",
#         ):
#             if col in out.columns:
#                 out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

#         # Atomic write: temp → replace
#         out.to_csv(tmp_path, index=False)
#         os.replace(tmp_path, path)

#         print(f"🧾 Appended diagnostics → {path}")
#         return str(path)

#     except Exception as e:
#         # Best-effort cleanup
#         if tmp_path.exists():
#             try:
#                 tmp_path.unlink()
#             except Exception:
#                 pass
#         print(f"⚠️ Could not append diagnostics: {e}")
#         return str(path)

# def C(path: str, default=None):

#     """
#     Dotted-path lookup into CONFIG.

#     Example:
#         C("PATHS.RAW_DATA")
#         C("RANGES.tenure.max")
#         C("TARGET.POSITIVE_CLASS", default="Yes")
#     """
#     node = CONFIG
#     for part in path.split("."):
#         if isinstance(node, dict) and part in node:
#             node = node[part]
#         else:
#             return default
#     return node

# # 0.0.x 🔧 Helpers & Small Utilities
from pathlib import Path
from types import MappingProxyType
from datetime import datetime
import os
import pandas as pd

# Jupyter/CLI-safe display
try:
    from IPython.display import display
except Exception:
    def display(obj):
        print(obj)

# --- CONFIG lookup helper ----------------------------------------------------
def C(path: str, default=None):
    """
    Dotted-path lookup into global CONFIG.

    Example:
        C("TARGET.COLUMN")
        C("RANGES.tenure.min")
    """
    global CONFIG  # expects CONFIG to be set later (e.g., in 2.0.0)
    node = CONFIG
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return node

# --- Script / notebook name helper -------------------------------------------
def get_script_name() -> str:
    """
    Best-effort script/notebook name for logging/metadata.
    Works in .py, Jupyter, and plain REPL.
    """
    try:
        return Path(__file__).name
    except Exception:
        try:
            import sys
            if hasattr(sys, "argv") and sys.argv and sys.argv[0].endswith(".ipynb"):
                return Path(sys.argv[0]).name
            return "interactive_notebook"
        except Exception:
            return "unknown_environment"

# --- Atomic CSV append with schema-union -------------------------------------
def atomic_append_csv(path: Path, chunk_df: pd.DataFrame) -> None:
    """
    Append rows to a CSV file with schema union + atomic replace.

    - path: Path to the CSV file.
    - chunk_df: DataFrame with one or more rows to append.

    Behavior:
      * If file exists → read, union columns, append rows.
      * If not → just write chunk_df.
      * Writes via temp file + os.replace for safety.
    """
    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    # Ensure parent dir exists
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        existing = pd.read_csv(path)
        all_cols = pd.Index(existing.columns).union(chunk_df.columns)
        out = pd.concat(
            [
                existing.reindex(columns=all_cols),
                chunk_df.reindex(columns=all_cols),
            ],
            ignore_index=True,
        )
    else:
        out = chunk_df.copy()

    out.to_csv(tmp_path, index=False)
    os.replace(tmp_path, path)

# --- Section-2-specific wrapper for unified report ---------------------------
def append_sec2(sec2_chunk: pd.DataFrame) -> None:
    """
    Thin wrapper around atomic_append_csv for the unified Section 2 report.

    Expects:
      - global SECTION2_REPORT_PATH set elsewhere (e.g. in 2.0.0).
    """
    global SECTION2_REPORT_PATH
    atomic_append_csv(SECTION2_REPORT_PATH, sec2_chunk)

# --- Simple dtype classifier for later 2.0.x / 2.1+ sections -----------------
def classify_dtype(dtype_str: str) -> str:
    """
    Map a pandas dtype string to a coarse type_group.
    """
    s = dtype_str.lower()
    if "int" in s or "float" in s:
        return "numeric"
    if "bool" in s:
        return "boolean"
    if "datetime" in s or "date" in s:
        return "datetime"
    if "category" in s:
        return "categorical"
    return "string_like"

