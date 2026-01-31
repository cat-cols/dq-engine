# this is a Level 3 skill level bootstrapping function
#

from pathlib import Path
import pandas as pd

def bootstrap_run_dirs(level_root, use_runs=True, run_id=None):
    """
    Level-3 safe run isolation.
    - If use_runs=False: returns Nones (caller can stick with resources/section2)
    - If use_runs=True: creates Level_3/runs/<RUN_ID>/... and returns the scoped dirs.
    """

    level_root = Path(level_root).resolve()
    runs_root = (level_root / "runs").resolve()
    runs_root.mkdir(parents=True, exist_ok=True)

    if not use_runs:
        return {
            "RUNS_ROOT": runs_root,
            "RUN_ID": None,
            "RUN_DIR": None,
            "RUN_REPORTS_DIR": None,
            "RUN_ARTIFACTS_DIR": None,
            "RUN_FIGURES_DIR": None,
            "RUN_LOGS_DIR": None,
        }

    if run_id is None:
        run_id = pd.Timestamp.utcnow().strftime("%Y%m%d_%H%M%S")

    run_dir = (runs_root / run_id).resolve()
    run_reports_dir   = (run_dir / "reports").resolve()
    run_artifacts_dir = (run_dir / "artifacts").resolve()
    run_figures_dir   = (run_dir / "figures").resolve()
    run_logs_dir      = (run_dir / "logs").resolve()

    for d in [run_dir, run_reports_dir, run_artifacts_dir, run_figures_dir, run_logs_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # handy pointer
    (runs_root / "latest.txt").write_text(run_id, encoding="utf-8")

    return {
        "RUNS_ROOT": runs_root,
        "RUN_ID": run_id,
        "RUN_DIR": run_dir,
        "RUN_REPORTS_DIR": run_reports_dir,
        "RUN_ARTIFACTS_DIR": run_artifacts_dir,
        "RUN_FIGURES_DIR": run_figures_dir,
        "RUN_LOGS_DIR": run_logs_dir,
    }