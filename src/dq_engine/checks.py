from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Sequence
import pandas as pd

@dataclass(frozen=True)
class CheckResult:
    run_id: str
    dataset_id: str
    check_id: str
    check_type: str
    severity: str
    status: str
    table_name: str
    column_name: Optional[str]
    metric_name: str
    metric_value: float
    threshold: Optional[float]
    details_json: Dict[str, Any]

def accepted_values(run_id: str, dataset_id: str, check_id: str, severity: str,
                    table_name: str, column_name: str, allowed: Sequence[Any], df: pd.DataFrame) -> CheckResult:
    bad = df[~df[column_name].isin(list(allowed))]
    bad_n = float(len(bad))
    status = "pass" if bad_n == 0 else ("fail" if severity == "fail" else "warn")
    return CheckResult(
        run_id=run_id,
        dataset_id=dataset_id,
        check_id=check_id,
        check_type="accepted_values",
        severity=severity,
        status=status,
        table_name=table_name,
        column_name=column_name,
        metric_name="bad_rows",
        metric_value=bad_n,
        threshold=0.0,
        details_json={"allowed": list(allowed)}
    )

def row_count(run_id: str, dataset_id: str, check_id: str, severity: str,
              table_name: str, n_rows: int) -> CheckResult:
    status = "pass" if n_rows > 0 else ("fail" if severity == "fail" else "warn")
    return CheckResult(
        run_id=run_id,
        dataset_id=dataset_id,
        check_id=check_id,
        check_type="row_count",
        severity=severity,
        status=status,
        table_name=table_name,
        column_name=None,
        metric_name="row_count",
        metric_value=float(n_rows),
        threshold=0.0,
        details_json={}
    )
