# bootstrap

from pathlib import Path
from typing import Any, Dict
import inspect
import pandas as pd

def strap(
    *,
    sec2_dir=None,              # canonical Section 2 base dir override
    project_root=None,          # optional: if provided, used to derive defaults
    mkdir=True,

    # where shared roots should live
    figures_in_project=True,
    artifacts_in_project=True,
    processed_in_project=True,
    clean_in_project=True,

    # optional structure conventions
    include_section_subdirs=True,
    include_figure_roots=True,
    include_common_files=True,
    include_quality_dir=True,

    # convenience behavior for notebooks
    export_globals=True,
    init_globals_lists=True,
):
    """
    Canonical Section 2 bootstrap: ONE base directory.

    Does:
      - resolve canonical dirs + canonical file paths
      - mkdir them (optional)
      - optionally export into globals() for 300-cell notebooks

    Does NOT:
      - read/write any data files (keep that in per-section cells)
    """

    PROJECT_ROOT = Path(project_root).resolve() if project_root else None

    # -- 1) Canonical base
    if sec2_dir is not None:
        SEC2_DIR = Path(sec2_dir).resolve()
    elif PROJECT_ROOT is not None:
        SEC2_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
    else:
        SEC2_DIR = (Path.cwd() / "resources" / "reports" / "section2").resolve()

    # -- 2) Canonical unified summary
    SECTION2_REPORT_PATH = (SEC2_DIR / "section2_summary.csv").resolve()

    # -- 3) Shared roots (figures / artifacts / processed / clean)
    FIGURES_DIR = (
        (PROJECT_ROOT / "resources" / "figures").resolve()
        if (PROJECT_ROOT is not None and figures_in_project)
        else (SEC2_DIR.parent / "figures").resolve()
    )

    ARTIFACTS_DIR = (
        (PROJECT_ROOT / "resources" / "artifacts").resolve()
        if (PROJECT_ROOT is not None and artifacts_in_project)
        else (SEC2_DIR.parent / "artifacts").resolve()
    )

    PROCESSED_DIR = (
        (PROJECT_ROOT / "resources" / "data" / "processed").resolve()
        if (PROJECT_ROOT is not None and processed_in_project)
        else (SEC2_DIR.parent / "data" / "processed").resolve()
    )

    CLEAN_DIR = (
        (PROJECT_ROOT / "resources" / "clean").resolve()
        if (PROJECT_ROOT is not None and clean_in_project)
        else (SEC2_DIR.parent / "clean").resolve()
    )

    # -- 4) Section subdirs (optional but recommended)
    SEC2_SECTION_DIRS = {}
    if include_section_subdirs:
        section_ids = ["2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12"]
        SEC2_SECTION_DIRS = {sid: (SEC2_DIR / sid).resolve() for sid in section_ids}

    # convenience aliases if you want them
    SEC2_23_DIR  = SEC2_SECTION_DIRS.get("2.3", (SEC2_DIR / "2.3").resolve())
    SEC2_24_DIR  = SEC2_SECTION_DIRS.get("2.4", (SEC2_DIR / "2.4").resolve())
    SEC2_25_DIR  = SEC2_SECTION_DIRS.get("2.5", (SEC2_DIR / "2.5").resolve())
    SEC2_26_DIR  = SEC2_SECTION_DIRS.get("2.6", (SEC2_DIR / "2.6").resolve())
    SEC2_27_DIR  = SEC2_SECTION_DIRS.get("2.7", (SEC2_DIR / "2.7").resolve())
    SEC2_28_DIR  = SEC2_SECTION_DIRS.get("2.8", (SEC2_DIR / "2.8").resolve())
    SEC2_29_DIR  = SEC2_SECTION_DIRS.get("2.9", (SEC2_DIR / "2.9").resolve())
    SEC2_210_DIR = SEC2_SECTION_DIRS.get("2.10", (SEC2_DIR / "2.10").resolve())
    SEC2_211_DIR = SEC2_SECTION_DIRS.get("2.11", (SEC2_DIR / "2.11").resolve())
    SEC2_212_DIR = SEC2_SECTION_DIRS.get("2.12", (SEC2_DIR / "2.12").resolve())

    # -- 5) Common named report dirs
    # You’ve been using NUMERIC_DIR heavily (2.3.*). Give it a stable home:
    NUMERIC_DIR = (SEC2_DIR / "numeric").resolve()
    CATEGORICAL_DIR = (SEC2_DIR / "categorical").resolve()

    # section-specific “named” dirs you already use
    FOUNDATIONAL_DIR = (SEC2_27_DIR / "sec2_27_foundational_stats").resolve()
    VALIDATION_DIR   = (SEC2_28_DIR / "sec2_28_statistical_validation").resolve()

    # 2.9 “quality” dir you keep guarding
    QUALITY_DIR = (SEC2_DIR / "quality").resolve() if include_quality_dir else None

    # -- 6) Figure roots (2.10 / 2.11 patterns you repeat)
    FIG_ROOTS = {}
    if include_figure_roots:
        FIG_ROOTS = {
            "FIG_2_10_UNIVARIATE_DIR": (FIGURES_DIR / "2_10_univariate").resolve(),
            "FIG_2_10_BIVARIATE_DIR": (FIGURES_DIR / "2_10_bivariate").resolve(),
            "FIG_2_11_DIR": (FIGURES_DIR / "2_11").resolve(),
            "FIG_2_11_STRUCTURE_DIR": (FIGURES_DIR / "2_11_structure").resolve(),
            "FIG_2_11_INTERACTIONS_DIR": (FIGURES_DIR / "2_11_interactions").resolve(),
            "FIG_2_10_NUMERIC_DIR": (FIGURES_DIR / "2_10_univariate" / "numeric").resolve(),
            "FIG_2_10_CATEGORICAL_DIR": (FIGURES_DIR / "2_10_univariate" / "categorical").resolve(),
        }

    # -- 7) Canonical “new” file paths (the stuff your cells keep re-deriving)
    COMMON_FILES = {}
    if include_common_files:
        # 2.3.* run-health inputs/outputs (live in NUMERIC_DIR per your current code)
        COMMON_FILES.update({
            "CONTRACTS_VIOLATIONS_PATH": (NUMERIC_DIR / "data_contract_violations.json").resolve(),
            "DRIFT_METRICS_PATH": (NUMERIC_DIR / "data_drift_metrics.csv").resolve(),
            "PERFORMANCE_PROFILE_PATH": (NUMERIC_DIR / "performance_profile.csv").resolve(),
            "RUN_HEALTH_SUMMARY_PATH": (NUMERIC_DIR / "run_health_summary.csv").resolve(),
        })

        # 2.5.* logic integrity artifacts (put them in SEC2_25_DIR by default)
        COMMON_FILES.update({
            "INTEGRITY_INDEX_PATH": (SEC2_25_DIR / "data_integrity_index.csv").resolve(),
            "ANOMALY_CONTEXT_PATH": (SEC2_25_DIR / "logic_anomaly_context.parquet").resolve(),
            "LOGIC_DASHBOARD_PATH": (SEC2_25_DIR / "logic_integrity_dashboard.html").resolve(),
        })

        # temps for atomic writes
        COMMON_FILES["INTEGRITY_INDEX_TMP"] = COMMON_FILES["INTEGRITY_INDEX_PATH"].with_suffix(".tmp.csv")
        COMMON_FILES["LOGIC_DASHBOARD_TMP"] = COMMON_FILES["LOGIC_DASHBOARD_PATH"].with_suffix(".tmp.html")

    # -- 8) mkdir in ONE place
    if mkdir:
        dirs_to_make = [
            SEC2_DIR, FIGURES_DIR, ARTIFACTS_DIR, PROCESSED_DIR, CLEAN_DIR,
            NUMERIC_DIR, CATEGORICAL_DIR,
            SEC2_23_DIR, SEC2_24_DIR, SEC2_25_DIR, SEC2_26_DIR, SEC2_27_DIR, SEC2_28_DIR, SEC2_29_DIR,
            SEC2_210_DIR, SEC2_211_DIR, SEC2_212_DIR,
            FOUNDATIONAL_DIR, VALIDATION_DIR,
        ]
        if QUALITY_DIR is not None:
            dirs_to_make.append(QUALITY_DIR)
        dirs_to_make.extend(FIG_ROOTS.values())
        dirs_to_make.extend(SEC2_SECTION_DIRS.values())

        # de-dupe + create
        seen = set()
        for d in dirs_to_make:
            if d is None:
                continue
            d = Path(d)
            if d not in seen:
                seen.add(d)
                d.mkdir(parents=True, exist_ok=True)

    out = {
        "PROJECT_ROOT": PROJECT_ROOT,

        # canonical base
        "SEC2_DIR": SEC2_DIR,

        # canonical summary path + legacy-ish alias
        "SECTION2_REPORT_PATH": SECTION2_REPORT_PATH,
        "SEC2_SUMMARY_PATH": SECTION2_REPORT_PATH,

        # shared roots
        "FIGURES_DIR": FIGURES_DIR,
        "ARTIFACTS_DIR": ARTIFACTS_DIR,
        "PROCESSED_DIR": PROCESSED_DIR,
        "CLEAN_DIR": CLEAN_DIR,

        # section dirs
        "SEC2_SECTION_DIRS": SEC2_SECTION_DIRS,
        "SEC2_23_DIR": SEC2_23_DIR,
        "SEC2_24_DIR": SEC2_24_DIR,
        "SEC2_25_DIR": SEC2_25_DIR,
        "SEC2_26_DIR": SEC2_26_DIR,
        "SEC2_27_DIR": SEC2_27_DIR,
        "SEC2_28_DIR": SEC2_28_DIR,
        "SEC2_29_DIR": SEC2_29_DIR,
        "SEC2_210_DIR": SEC2_210_DIR,
        "SEC2_211_DIR": SEC2_211_DIR,
        "SEC2_212_DIR": SEC2_212_DIR,

        # report dirs
        "NUMERIC_DIR": NUMERIC_DIR,
        "CATEGORICAL_DIR": CATEGORICAL_DIR,
        "FOUNDATIONAL_DIR": FOUNDATIONAL_DIR,
        "VALIDATION_DIR": VALIDATION_DIR,
        "QUALITY_DIR": QUALITY_DIR,
    }

    out.update(FIG_ROOTS)
    out.update(COMMON_FILES)

    if export_globals:
        global_caller = inspect.currentframe().f_back.f_globals
        for k, v in out.items():
            if v is not None:
                global_caller[k] = v
    """
    export_globals behavior: export_globals (bt.py)

    Purpose
    - Convenience “injector” that copies values produced by a helper/bootstrap function into the
    caller’s notebook/global namespace.

    What it does
    - Gets the caller frame’s globals dict:
        global_caller = inspect.currentframe().f_back.f_globals
    - Iterates through `out` (a dict of computed objects/paths/config):
        for k, v in out.items():
            if v is not None:
                global_caller[k] = v
    - Net effect: after the bootstrap call, the notebook can refer to variables like PROJECT_ROOT,
    NUMERIC_DIR, SECTION2_REPORT_PATH, etc. without manual assignment.

    Why it’s useful
    - Reduces boilerplate in notebooks (no repeated “X = out['X']”).
    - Makes “bootstrap once, use everywhere” workflows smoother.

    Important constraints / caveats
    - It mutates the caller’s global namespace (side effect). That’s convenient, but it can make
    debugging harder if you accidentally overwrite names.
    - It skips None values (v is not None). If something fails to compute and remains None, the
    variable may never be created in the notebook.
    - It does not validate that the environment is complete/correct; it only attempts to populate it.
    """

    # optional: init global lists once (ONLY if you truly rely on them across cells)
    if init_globals_lists:
        if "sec2_diagnostics_rows" not in globals():
            out["sec2_diagnostics_rows"] = []
        if "cleaning_actions_261" not in globals():
            out["cleaning_actions_261"] = []


    return out
