# telco_churn/utils/lineage.py

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class DFSnapshot:
    """One point in the pipeline: what did the frame look like here?"""

    section: str
    label: str
    step_index: int

    n_rows: int
    n_cols: int

    # shape / diff vs previous
    rows_delta: Optional[int] = None
    cols_delta: Optional[int] = None

    # core “health” metrics per tracked column (flattened as columns)
    metrics: Dict[str, Any] = field(default_factory=dict)

    changed_columns: str = ""  # comma-separated names that changed vs previous
    note: str = ""
    timestamp: pd.Timestamp = field(default_factory=pd.Timestamp.utcnow)

    def to_flat_dict(self) -> Dict[str, Any]:
        base = asdict(self)
        # metrics is nested; flatten to top-level columns
        metrics = base.pop("metrics", {}) or {}
        for k, v in metrics.items():
            base[k] = v
        return base


class DFLineageTracker:
    """
    Tracks how a DataFrame evolves across a notebook / pipeline.

    - You call .snapshot(df, section="2.0.0", label="Initial load", ...)
    - It records shape, per-column metrics, and diffs vs previous snapshot.
    - At the end, call .to_frame() / .save_csv() / .plot_metric(...)
    """

    def __init__(
        self,
        name: str,
        tracked_columns: Sequence[str] = ("TotalCharges",),
        save_path: Optional[Path] = None,
        compute_changed_columns: bool = True,
    ) -> None:
        self.name = name
        self.tracked_columns = list(tracked_columns)
        self.save_path = Path(save_path) if save_path is not None else None
        self.compute_changed_columns = compute_changed_columns

        self._snapshots: List[DFSnapshot] = []
        self._last_df: Optional[pd.DataFrame] = None

    # ------------------------------------------------------------------ #
    # Core API
    # ------------------------------------------------------------------ #
    def snapshot(
        self,
        df: pd.DataFrame,
        section: str,
        label: str,
        note: str = "",
    ) -> None:
        """
        Record the current state of df at a given pipeline step.
        """
        df = df.copy(deep=False)  # cheap view; we don't mutate it here
        step_index = len(self._snapshots)

        n_rows, n_cols = int(df.shape[0]), int(df.shape[1])
        rows_delta = None
        cols_delta = None
        changed_cols: List[str] = []

        if self._last_df is not None:
            prev_rows, prev_cols = self._last_df.shape
            rows_delta = n_rows - int(prev_rows)
            cols_delta = n_cols - int(prev_cols)

            if self.compute_changed_columns:
                common_cols = [c for c in df.columns if c in self._last_df.columns]
                for col in common_cols:
                    # cheap-ish equality check; for 7k x 21 this is fine
                    try:
                        if not df[col].equals(self._last_df[col]):
                            changed_cols.append(col)
                    except Exception:
                        # if comparison fails for some weird dtype, just skip it
                            changed_cols.append(col)
        else:
            rows_delta = 0
            cols_delta = 0

        metrics = self._compute_metrics(df)

        snapshot = DFSnapshot(
            section=section,
            label=label,
            step_index=step_index,
            n_rows=n_rows,
            n_cols=n_cols,
            rows_delta=rows_delta,
            cols_delta=cols_delta,
            metrics=metrics,
            changed_columns=",".join(sorted(set(changed_cols))) if changed_cols else "",
            note=note,
        )

        self._snapshots.append(snapshot)
        self._last_df = df

    def to_frame(self) -> pd.DataFrame:
        """
        Return all snapshots as a pandas DataFrame.
        """
        if not self._snapshots:
            return pd.DataFrame()
        rows = [s.to_flat_dict() for s in self._snapshots]
        df = pd.DataFrame(rows).sort_values("step_index").reset_index(drop=True)
        return df

    def save_csv(self, path: Optional[Path] = None) -> Path:
        """
        Save lineage to CSV (atomic write). Returns final path.
        """
        if path is None:
            if self.save_path is None:
                raise ValueError("No save_path configured for DFLineageTracker.")
            path = self.save_path

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df = self.to_frame()
        tmp = path.with_suffix(".tmp.csv")
        df.to_csv(tmp, index=False)
        os.replace(tmp, path)
        return path

    # ------------------------------------------------------------------ #
    # Metrics + plotting
    # ------------------------------------------------------------------ #
    def _compute_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute metrics for each tracked column, like:
            - {col}_present
            - {col}_nulls
            - {col}_non_nulls
            - {col}_min / _max / _mean (numeric only)
        """
        m: Dict[str, Any] = {}
        for col in self.tracked_columns:
            col_key = col.replace(" ", "_")
            present = col in df.columns
            m[f"{col_key}_present"] = bool(present)
            if not present:
                m[f"{col_key}_nulls"] = None
                m[f"{col_key}_non_nulls"] = None
                m[f"{col_key}_min"] = None
                m[f"{col_key}_max"] = None
                m[f"{col_key}_mean"] = None
                continue

            series = df[col]
            nulls = int(series.isna().sum())
            non_nulls = int(series.notna().sum())
            m[f"{col_key}_nulls"] = nulls
            m[f"{col_key}_non_nulls"] = non_nulls

            if pd.api.types.is_numeric_dtype(series):
                m[f"{col_key}_min"] = float(series.min(skipna=True)) if non_nulls > 0 else None
                m[f"{col_key}_max"] = float(series.max(skipna=True)) if non_nulls > 0 else None
                m[f"{col_key}_mean"] = float(series.mean(skipna=True)) if non_nulls > 0 else None
            else:
                m[f"{col_key}_min"] = None
                m[f"{col_key}_max"] = None
                m[f"{col_key}_mean"] = None

        return m

    def plot_metric(
        self,
        metric_col: str,
        title: Optional[str] = None,
        figsize: tuple = (8, 4),
    ) -> None:
        """
        Quick line plot of a numeric metric across snapshots.

        Example metric_col:
            'TotalCharges_nulls'
            'TotalCharges_non_nulls'
            'tenure_nulls'
        """
        df = self.to_frame()
        if df.empty:
            print("⚠️ No snapshots recorded; nothing to plot.")
            return

        if metric_col not in df.columns:
            print(f"⚠️ Metric '{metric_col}' not found in lineage DataFrame.")
            print("   Available metrics:", [c for c in df.columns if metric_col.split('_')[0] in c])
            return

        x = range(len(df))
        y = df[metric_col].values

        plt.figure(figsize=figsize)
        plt.plot(x, y, marker="o")
        plt.xticks(
            ticks=x,
            labels=[f"{s} | {l}" for s, l in zip(df["section"], df["label"])],
            rotation=45,
            ha="right",
        )
        plt.ylabel(metric_col)
        plt.title(title or f"{self.name}: {metric_col} across steps")
        plt.tight_layout()
        plt.show()