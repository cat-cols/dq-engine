# dq_engine/helpers/baseline.py

import shutil
from pathlib import Path
import pandas as pd

# V1
# def promote_baseline_artifacts(
#     metadata_path: Path,
#     dataset_overview_path: Path,
#     artifacts_dir: Path,
#     baseline_enabled: bool = False,
#     verbose: bool = True,
# ):
#     if not baseline_enabled:
#         return

#     baseline_dir = artifacts_dir / "baseline"
#     baseline_dir.mkdir(parents=True, exist_ok=True)

#     baseline_meta = baseline_dir / "baseline_metadata.json"
#     baseline_overview = baseline_dir / "baseline_dataset_overview.csv"

#     shutil.copy2(metadata_path, baseline_meta)
#     shutil.copy2(dataset_overview_path, baseline_overview)

#     if verbose:
#         print(f"📌 Promoted to baseline → {baseline_meta.name}, {baseline_overview.name}")

# V2
def promote_baseline_artifacts(
    metadata_path: Path,
    dataset_overview_path: Path,
    artifacts_dir: Path,
    baseline_enabled: bool = False,
    section_label: str = "2.0.6",  # customize if needed
    report_path: Path = None,
    verbose: bool = True,
    append_fn=None,  # expects callable like: append_sec2(df, report_path)
):
    if not baseline_enabled:
        return

    baseline_dir = artifacts_dir / "baseline"
    baseline_dir.mkdir(parents=True, exist_ok=True)

    baseline_meta = baseline_dir / "baseline_metadata.json"
    baseline_overview = baseline_dir / "baseline_dataset_overview.csv"

    shutil.copy2(metadata_path, baseline_meta)
    shutil.copy2(dataset_overview_path, baseline_overview)

    if verbose:
        print(f"📌 Promoted to baseline → {baseline_meta.name}, {baseline_overview.name}")

    # Emit report row (optional)
    if append_fn and report_path:
        summary_baseline = pd.DataFrame([{
            "section": section_label,
            "section_name": "Promote artifacts to baseline",
            "check": "Copy metadata and overview to artifacts/baseline/",
            "level": "info",
            "status": "promoted",
            "detail": f"{baseline_meta.name}, {baseline_overview.name}",
            "timestamp": pd.Timestamp.utcnow().isoformat(),
        }])
        append_fn(summary_baseline, report_path)
