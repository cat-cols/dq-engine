# dq module

# append section 2 report
from pathlib import Path
import os
import pandas as pd

# config accessor
def C(key, default=None, *, required=False, config=None):
    """
    Safe access into CONFIG using dotted keys, e.g. C("RANGES.tenure.max").
    """
    cfg = config or globals().get("CONFIG", {})
    if not isinstance(cfg, dict):
        if required:
            raise TypeError("CONFIG is not a dict")
        return default

    parts = key.split(".")
    cur = cfg
    for p in parts:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            if required:
                raise KeyError(f"Missing CONFIG key: {key}")
            return default
    return cur

def append_sec2(chunk_df, path=None):
    """
    Atomic append of a diagnostics chunk into the unified Section 2 report.
    Uses SECTION2_REPORT_PATH from globals() if path is None.
    """
    if path is None:
        if "SECTION2_REPORT_PATH" not in globals():
            raise RuntimeError("SECTION2_REPORT_PATH not defined")
        path = SECTION2_REPORT_PATH

    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

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

    for col in ("percent", "imbalance_ratio", "pct_inconsistent",
                "top_freq", "pct_not_allowed"):
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

    out.to_csv(tmp_path, index=False)
    os.replace(tmp_path, path)

#
def atomic_write_csv(df, path, *, index=False):
    """
    Write df to CSV atomically via a .tmp file.
    """
    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(tmp_path, index=index)
    os.replace(tmp_path, path)
