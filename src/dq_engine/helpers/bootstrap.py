#
from pathlib import Path

# 1) Canonical base (single source of truth)
def strap_paths(
    *,
    sec2_dir=None,              # canonical Section 2 base dir override
    project_root=None,          # optional: used only if sec2_dir is not provided
    mkdir=True,
    figures_in_project=True,    # if project_root is given, prefer PROJECT_ROOT/resources/figures
    artifacts_in_project=True,  # if project_root is given, prefer PROJECT_ROOT/resources/artifacts
    export_globals=True,        # if True: write canonical names into globals()
):
    """
    Canonical Section 2 bootstrap: ONE base directory.
    - Defines the canonical base dir + canonical summary path.
    - Defines common subdirs used across 2.x.
    - Optionally exports canonical variables into globals() so 300 cells can rely on them.

    Returns dict[str, Path | dict].
    """

    PROJECT_ROOT = Path(project_root).resolve() if project_root else None

    # 1) Canonical base (single source of truth)
    if sec2_dir is not None:
        SEC2_DIR = Path(sec2_dir).resolve()
    elif PROJECT_ROOT is not None:
        SEC2_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
    else:
        SEC2_DIR = (Path.cwd() / "resources" / "reports" / "section2").resolve()

    # 2) Canonical summary path (single source of truth)
    SECTION2_REPORT_PATH = (SEC2_DIR / "section2_summary.csv").resolve()

    # 3) Shared roots (clear, non-brittle rules)
    if PROJECT_ROOT is not None and figures_in_project:
        FIGURES_DIR = (PROJECT_ROOT / "resources" / "figures").resolve()
    else:
        FIGURES_DIR = (SEC2_DIR.parent / "figures").resolve()

    if PROJECT_ROOT is not None and artifacts_in_project:
        ARTIFACTS_DIR = (PROJECT_ROOT / "resources" / "artifacts").resolve()
    else:
        ARTIFACTS_DIR = (SEC2_DIR.parent / "artifacts").resolve()

    # 4) Section subdirs (generated)
    section_ids = ["2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12"]
    SEC2_SECTION_DIRS = {sid: (SEC2_DIR / sid).resolve() for sid in section_ids}

    # Optional convenience aliases (your existing naming style)
    SEC2_24_DIR  = SEC2_SECTION_DIRS["2.4"]
    SEC2_25_DIR  = SEC2_SECTION_DIRS["2.5"]
    SEC2_26_DIR  = SEC2_SECTION_DIRS["2.6"]
    SEC2_27_DIR  = SEC2_SECTION_DIRS["2.7"]
    SEC2_28_DIR  = SEC2_SECTION_DIRS["2.8"]
    SEC2_29_DIR  = SEC2_SECTION_DIRS["2.9"]
    SEC2_210_DIR = SEC2_SECTION_DIRS["2.10"]
    SEC2_211_DIR = SEC2_SECTION_DIRS["2.11"]
    SEC2_212_DIR = SEC2_SECTION_DIRS["2.12"]

    # 5) Common named dirs you reuse a lot
    CATEGORICAL_DIR = (SEC2_DIR / "categorical").resolve()
    SEC2_27_FOUNDATIONAL_DIR = (SEC2_27_DIR / "sec2_27_foundational_stats").resolve()
    SEC2_28_VALIDATION_DIR   = (SEC2_28_DIR / "sec2_28_statistical_validation").resolve()

    # ---- mkdirs
    if mkdir:
        dirs_to_make = [
            SEC2_DIR, FIGURES_DIR, ARTIFACTS_DIR,
            *SEC2_SECTION_DIRS.values(),
            CATEGORICAL_DIR, SEC2_27_FOUNDATIONAL_DIR, SEC2_28_VALIDATION_DIR,
        ]
        for d in dirs_to_make:
            d.mkdir(parents=True, exist_ok=True)

    out = {
        "PROJECT_ROOT": PROJECT_ROOT,
        "SEC2_DIR": SEC2_DIR,                         # canonical base
        "SEC2_REPORTS_DIR": SEC2_DIR,                 # legacy alias (many of your cells use it)
        "sec2_reports_dir": SEC2_DIR,                 # legacy alias (lowercase pattern appears a lot)

        "SECTION2_REPORT_PATH": SECTION2_REPORT_PATH, # canonical summary path
        "SEC2_SUMMARY_PATH": SECTION2_REPORT_PATH,    # legacy-ish alias

        "FIGURES_DIR": FIGURES_DIR,
        "ARTIFACTS_DIR": ARTIFACTS_DIR,

        "SEC2_SECTION_DIRS": SEC2_SECTION_DIRS,

        "SEC2_24_DIR": SEC2_24_DIR,
        "SEC2_25_DIR": SEC2_25_DIR,
        "SEC2_26_DIR": SEC2_26_DIR,
        "SEC2_27_DIR": SEC2_27_DIR,
        "SEC2_28_DIR": SEC2_28_DIR,
        "SEC2_29_DIR": SEC2_29_DIR,
        "SEC2_210_DIR": SEC2_210_DIR,
        "SEC2_211_DIR": SEC2_211_DIR,
        "SEC2_212_DIR": SEC2_212_DIR,

        "CATEGORICAL_DIR": CATEGORICAL_DIR,
        "SEC2_27_FOUNDATIONAL_DIR": SEC2_27_FOUNDATIONAL_DIR,
        "SEC2_28_VALIDATION_DIR": SEC2_28_VALIDATION_DIR,
    }

    if export_globals:
        g = globals()
        for k, v in out.items():
            g[k] = v

    return out


# 2)
# def strap_paths(
    #     *,
    #     sec2_dir=None,          # canonical Section 2 base dir override
    #     project_root=None,      # optional: used only if sec2_dir is not provided
    #     mkdir=True,
    #     figures_in_project=True,   # if project_root is given, prefer PROJECT_ROOT/resources/figures
    #     artifacts_in_project=True, # if project_root is given, prefer PROJECT_ROOT/resources/artifacts
    # ):
    #     """
    #     Canonical Section 2 bootstrap: ONE base directory.
    #     Returns dict of resolved Paths.
    #     """

    #     PROJECT_ROOT = Path(project_root).resolve() if project_root else None

    #     # 1) Canonical base
    #     if sec2_dir is not None:
    #         SEC2_DIR = Path(sec2_dir).resolve()
    #     elif PROJECT_ROOT is not None:
    #         SEC2_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
    #     else:
    #         raise RuntimeError("❌ Provide sec2_dir or project_root to resolve SEC2_DIR")

    #     # 2) Canonical summary path (always inside SEC2_DIR)
    #     SEC2_SUMMARY_PATH = (SEC2_DIR / "section2_summary.csv").resolve()

    #     # 3) Shared roots (clear, non-brittle rules)
    #     if PROJECT_ROOT is not None and figures_in_project:
    #         FIGURES_DIR = (PROJECT_ROOT / "resources" / "figures").resolve()
    #     else:
    #         FIGURES_DIR = (SEC2_DIR.parent / "figures").resolve()

    #     if PROJECT_ROOT is not None and artifacts_in_project:
    #         ARTIFACTS_DIR = (PROJECT_ROOT / "resources" / "artifacts").resolve()
    #     else:
    #         ARTIFACTS_DIR = (SEC2_DIR.parent / "artifacts").resolve()

    #     # 4) Section subdirs (generated, not hand-written)
    #     section_ids = ["2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12"]
    #     SEC2_SECTION_DIRS = {sid: (SEC2_DIR / sid).resolve() for sid in section_ids}

    #     # Optional: keep your legacy names if you like them
    #     SEC2_24_DIR  = SEC2_SECTION_DIRS["2.4"]
    #     SEC2_25_DIR  = SEC2_SECTION_DIRS["2.5"]
    #     SEC2_26_DIR  = SEC2_SECTION_DIRS["2.6"]
    #     SEC2_27_DIR  = SEC2_SECTION_DIRS["2.7"]
    #     SEC2_28_DIR  = SEC2_SECTION_DIRS["2.8"]
    #     SEC2_29_DIR  = SEC2_SECTION_DIRS["2.9"]
    #     SEC2_210_DIR = SEC2_SECTION_DIRS["2.10"]
    #     SEC2_211_DIR = SEC2_SECTION_DIRS["2.11"]
    #     SEC2_212_DIR = SEC2_SECTION_DIRS["2.12"]

    #     # 5) Common named dirs you reuse
    #     CATEGORICAL_DIR = (SEC2_DIR / "categorical").resolve()
    #     SEC2_27_FOUNDATIONAL_DIR = (SEC2_27_DIR / "sec2_27_foundational_stats").resolve()
    #     SEC2_28_VALIDATION_DIR   = (SEC2_28_DIR / "sec2_28_statistical_validation").resolve()

    #     if mkdir:
    #         dirs_to_make = [
    #             SEC2_DIR, FIGURES_DIR, ARTIFACTS_DIR,
    #             *SEC2_SECTION_DIRS.values(),
    #             CATEGORICAL_DIR, SEC2_27_FOUNDATIONAL_DIR, SEC2_28_VALIDATION_DIR,
    #         ]
    #         for d in dirs_to_make:
    #             d.mkdir(parents=True, exist_ok=True)

    #     return {
    #         "PROJECT_ROOT": PROJECT_ROOT,
    #         "SEC2_DIR": SEC2_DIR,
    #         "SEC2_SUMMARY_PATH": SEC2_SUMMARY_PATH,
    #         "FIGURES_DIR": FIGURES_DIR,
    #         "ARTIFACTS_DIR": ARTIFACTS_DIR,

    #         # nice for loops / generic code
    #         "SEC2_SECTION_DIRS": SEC2_SECTION_DIRS,

    #         # optional “legacy” convenience keys
    #         "SEC2_24_DIR": SEC2_24_DIR,
    #         "SEC2_25_DIR": SEC2_25_DIR,
    #         "SEC2_26_DIR": SEC2_26_DIR,
    #         "SEC2_27_DIR": SEC2_27_DIR,
    #         "SEC2_28_DIR": SEC2_28_DIR,
    #         "SEC2_29_DIR": SEC2_29_DIR,
    #         "SEC2_210_DIR": SEC2_210_DIR,
    #         "SEC2_211_DIR": SEC2_211_DIR,
    #         "SEC2_212_DIR": SEC2_212_DIR,

    #         "CATEGORICAL_DIR": CATEGORICAL_DIR,
    #         "SEC2_27_FOUNDATIONAL_DIR": SEC2_27_FOUNDATIONAL_DIR,
    #         "SEC2_28_VALIDATION_DIR": SEC2_28_VALIDATION_DIR,
    #     }

# 3)
# def strap_paths(
    #     *,
    #     sec2_dir=None,          # the one true base dir
    #     project_root=None,      # optional: used only if sec2_dir is not provided
    #     mkdir=True,
    # ):
    #     """
    #     Canonical Section 2 bootstrap: ONE base directory.
    #     Returns dict of resolved Paths.
    #     """

    #     PROJECT_ROOT = Path(project_root).resolve() if project_root else None

    #     # 1) Canonical base
    #     if sec2_dir is not None:
    #         SEC2_DIR = Path(sec2_dir).resolve()
    #     elif PROJECT_ROOT is not None:
    #         SEC2_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
    #     else:
    #         raise RuntimeError("❌ Provide sec2_dir or project_root to resolve SEC2_DIR")

    #     # 2) Canonical summary path (always inside SEC2_DIR)
    #     SEC2_SUMMARY_PATH = (SEC2_DIR / "section2_summary.csv").resolve()

    #     # 3) Canonical shared roots (choose whether these live inside SEC2_DIR or alongside it)
    #     # Option A (common): alongside reports
    #     FIGURES_DIR = (SEC2_DIR.parent.parent / "figures").resolve() if PROJECT_ROOT is None else (PROJECT_ROOT / "resources" / "figures").resolve()
    #     ARTIFACTS_DIR = (SEC2_DIR.parent.parent / "artifacts").resolve() if PROJECT_ROOT is None else (PROJECT_ROOT / "resources" / "artifacts").resolve()

    #     # 4) Section subdirs (your standardization point)
    #     SEC2_24_DIR  = (SEC2_DIR / "2.4").resolve()
    #     SEC2_25_DIR  = (SEC2_DIR / "2.5").resolve()
    #     SEC2_26_DIR  = (SEC2_DIR / "2.6").resolve()
    #     SEC2_27_DIR  = (SEC2_DIR / "2.7").resolve()
    #     SEC2_28_DIR  = (SEC2_DIR / "2.8").resolve()
    #     SEC2_29_DIR  = (SEC2_DIR / "2.9").resolve()
    #     SEC2_210_DIR = (SEC2_DIR / "2.10").resolve()
    #     SEC2_211_DIR = (SEC2_DIR / "2.11").resolve()
    #     SEC2_212_DIR = (SEC2_DIR / "2.12").resolve()

    #     # 5) Common “named” dirs you keep reusing
    #     CATEGORICAL_DIR = (SEC2_DIR / "categorical").resolve()
    #     SEC2_27_FOUNDATIONAL_DIR = (SEC2_27_DIR / "sec2_27_foundational_stats").resolve()
    #     SEC2_28_VALIDATION_DIR   = (SEC2_28_DIR / "sec2_28_statistical_validation").resolve()

    #     if mkdir:
    #         for d in [
    #             SEC2_DIR, FIGURES_DIR, ARTIFACTS_DIR,
    #             SEC2_24_DIR, SEC2_25_DIR, SEC2_26_DIR, SEC2_27_DIR, SEC2_28_DIR, SEC2_29_DIR,
    #             SEC2_210_DIR, SEC2_211_DIR, SEC2_212_DIR,
    #             CATEGORICAL_DIR, SEC2_27_FOUNDATIONAL_DIR, SEC2_28_VALIDATION_DIR
    #         ]:
    #             d.mkdir(parents=True, exist_ok=True)

    #     return {
    #         "SEC2_DIR": SEC2_DIR,
    #         "SEC2_SUMMARY_PATH": SEC2_SUMMARY_PATH,
    #         "FIGURES_DIR": FIGURES_DIR,
    #         "ARTIFACTS_DIR": ARTIFACTS_DIR,

    #         "SEC2_24_DIR": SEC2_24_DIR,
    #         "SEC2_25_DIR": SEC2_25_DIR,
    #         "SEC2_26_DIR": SEC2_26_DIR,
    #         "SEC2_27_DIR": SEC2_27_DIR,
    #         "SEC2_28_DIR": SEC2_28_DIR,
    #         "SEC2_29_DIR": SEC2_29_DIR,
    #         "SEC2_210_DIR": SEC2_210_DIR,
    #         "SEC2_211_DIR": SEC2_211_DIR,
    #         "SEC2_212_DIR": SEC2_212_DIR,

    #         "CATEGORICAL_DIR": CATEGORICAL_DIR,
    #         "SEC2_27_FOUNDATIONAL_DIR": SEC2_27_FOUNDATIONAL_DIR,
    #         "SEC2_28_VALIDATION_DIR": SEC2_28_VALIDATION_DIR,
    #     }

def strap_into_globals(**kwargs):
    """
    Notebook convenience wrapper: resolves paths then injects canonical + legacy aliases into globals().
    """
    paths = bootstrap_sec2_paths(**kwargs)
    g = globals()
    g.update(paths)

    # Legacy aliases (remove gradually)
    g["SEC2_REPORTS_DIR"] = paths["SEC2_DIR"]
    g["SECTION2_REPORT_PATH"] = paths["SEC2_SUMMARY_PATH"]
    g["sec2_reports_dir"] = paths["SEC2_DIR"]

    # Your common legacy per-section names
    g["section2_reports_dir_24D"] = paths["SEC2_24_DIR"]
    g["section2_reports_dir_25D"] = paths["SEC2_25_DIR"]
    g["sec2_reports_dir_26"] = paths["SEC2_26_DIR"]
    g["sec2_reports_dir_27"] = paths["SEC2_27_DIR"]
    g["sec2_reports_dir_28"] = paths["SEC2_28_DIR"]
    g["sec2_27_dir"] = paths["SEC2_27_FOUNDATIONAL_DIR"]
    g["sec2_28_dir"] = paths["SEC2_28_VALIDATION_DIR"]
    g["section2_summary_path_26"] = (paths["SEC2_26_DIR"] / "section2_summary.csv").resolve()

    # common containers
    if "sec2_diagnostics_rows" not in g:
        g["sec2_diagnostics_rows"] = []

    return paths








############ 🪦🪦 GRAVEYARD 🪦🧟‍♂️ #####################

# def strap_paths(
    #     *,
    #     project_root=None,
    #     reports_dir=None,
    #     sec2_dir=None,
    #     figures_dir=None,
    #     artifacts_dir=None,
    #     summary_path=None,
    #     mkdir=True,
    # ):
    #     """
    #     Resolve canonical Section 2 paths (dirs + summary path).
    #     Returns a dict of Paths. Does NOT depend on globals().
    #     """

    #     # project root
    #     PROJECT_ROOT = Path(project_root).resolve() if project_root else Path.cwd().resolve()

    #     # base sec2 dir
    #     if sec2_dir:
    #         SEC2_DIR = Path(sec2_dir).resolve()
    #     elif reports_dir:
    #         SEC2_DIR = (Path(reports_dir).resolve() / "section2").resolve()
    #     else:
    #         SEC2_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()

    #     # summary path
    #     if summary_path:
    #         SEC2_SUMMARY_PATH = Path(summary_path).resolve()
    #     else:
    #         SEC2_SUMMARY_PATH = (SEC2_DIR / "section2_summary.csv").resolve()

    #     # figures + artifacts roots
    #     FIGURES_DIR = Path(figures_dir).resolve() if figures_dir else (PROJECT_ROOT / "resources" / "figures").resolve()
    #     ARTIFACTS_DIR = Path(artifacts_dir).resolve() if artifacts_dir else (PROJECT_ROOT / "resources" / "artifacts").resolve()

    #     # section subdirs
    #     SEC2_24_DIR  = (SEC2_DIR / "2.4").resolve()
    #     SEC2_25_DIR  = (SEC2_DIR / "2.5").resolve()
    #     SEC2_26_DIR  = (SEC2_DIR / "2.6").resolve()
    #     SEC2_27_DIR  = (SEC2_DIR / "2.7").resolve()
    #     SEC2_28_DIR  = (SEC2_DIR / "2.8").resolve()
    #     SEC2_29_DIR  = (SEC2_DIR / "2.9").resolve()
    #     SEC2_210_DIR = (SEC2_DIR / "2.10").resolve()
    #     SEC2_211_DIR = (SEC2_DIR / "2.11").resolve()
    #     SEC2_212_DIR = (SEC2_DIR / "2.12").resolve()

    #     # common special dirs
    #     CATEGORICAL_DIR = (SEC2_DIR / "categorical").resolve()
    #     SEC2_27_FOUNDATIONAL_DIR = (SEC2_27_DIR / "sec2_27_foundational_stats").resolve()
    #     SEC2_28_VALIDATION_DIR   = (SEC2_28_DIR / "sec2_28_statistical_validation").resolve()

    #     if mkdir:
    #         for d in [
    #             SEC2_DIR, FIGURES_DIR, ARTIFACTS_DIR,
    #             SEC2_24_DIR, SEC2_25_DIR, SEC2_26_DIR, SEC2_27_DIR, SEC2_28_DIR, SEC2_29_DIR,
    #             SEC2_210_DIR, SEC2_211_DIR, SEC2_212_DIR,
    #             CATEGORICAL_DIR, SEC2_27_FOUNDATIONAL_DIR, SEC2_28_VALIDATION_DIR
    #         ]:
    #             d.mkdir(parents=True, exist_ok=True)

    #     return {
    #         "PROJECT_ROOT": PROJECT_ROOT,
    #         "SEC2_DIR": SEC2_DIR,
    #         "SEC2_SUMMARY_PATH": SEC2_SUMMARY_PATH,
    #         "FIGURES_DIR": FIGURES_DIR,
    #         "ARTIFACTS_DIR": ARTIFACTS_DIR,

    #         "SEC2_24_DIR": SEC2_24_DIR,
    #         "SEC2_25_DIR": SEC2_25_DIR,
    #         "SEC2_26_DIR": SEC2_26_DIR,
    #         "SEC2_27_DIR": SEC2_27_DIR,
    #         "SEC2_28_DIR": SEC2_28_DIR,
    #         "SEC2_29_DIR": SEC2_29_DIR,
    #         "SEC2_210_DIR": SEC2_210_DIR,
    #         "SEC2_211_DIR": SEC2_211_DIR,
    #         "SEC2_212_DIR": SEC2_212_DIR,

    #         "CATEGORICAL_DIR": CATEGORICAL_DIR,
    #         "SEC2_27_FOUNDATIONAL_DIR": SEC2_27_FOUNDATIONAL_DIR,
    #         "SEC2_28_VALIDATION_DIR": SEC2_28_VALIDATION_DIR,
    #     }

# # 2.0.0 | Bootstrap Section 2 paths (canonical, idempotent)

# from pathlib import Path

# def bootstrap_section2_paths():
#     global PROJECT_ROOT
#     global SEC2_REPORTS_DIR, FIGURES_DIR, ARTIFACTS_DIR
#     global SECTION2_REPORT_PATH, SEC2_SUMMARY_PATH
#     global sec2_diagnostics_rows

#     # -----------------------------
#     # 0) Project root (optional)
#     # -----------------------------
#     # If you already define PROJECT_ROOT elsewhere, keep it.
#     if "PROJECT_ROOT" in globals() and PROJECT_ROOT is not None:
#         PROJECT_ROOT = Path(PROJECT_ROOT).resolve()
#     else:
#         # conservative fallback: current working directory
#         PROJECT_ROOT = Path.cwd().resolve()

#     # -----------------------------
#     # 1) Canonical base: SEC2_REPORTS_DIR
#     # -----------------------------
#     # Priority:
#     #   A) existing SEC2_REPORTS_DIR (already set)
#     #   B) REPORTS_DIR/section2
#     #   C) PROJECT_ROOT/resources/reports/section2
#     #   D) resources/reports/section2 (relative)
#     if "SEC2_REPORTS_DIR" in globals() and SEC2_REPORTS_DIR is not None:
#         SEC2_REPORTS_DIR = Path(SEC2_REPORTS_DIR).resolve()
#     elif "REPORTS_DIR" in globals() and REPORTS_DIR is not None:
#         SEC2_REPORTS_DIR = (Path(REPORTS_DIR) / "section2").resolve()
#     else:
#         SEC2_REPORTS_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()

#     SEC2_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

#     # -----------------------------
#     # 2) Canonical summary path
#     # -----------------------------
#     # Keep the unified summary *inside* SEC2_REPORTS_DIR to avoid scattering.
#     if "SECTION2_REPORT_PATH" in globals() and SECTION2_REPORT_PATH is not None:
#         SECTION2_REPORT_PATH = Path(SECTION2_REPORT_PATH).resolve()
#     else:
#         SECTION2_REPORT_PATH = (SEC2_REPORTS_DIR / "section2_summary.csv").resolve()

#     # Optional short alias
#     SEC2_SUMMARY_PATH = SECTION2_REPORT_PATH

#     # -----------------------------
#     # 3) Figures root
#     # -----------------------------
#     if "FIGURES_DIR" in globals() and FIGURES_DIR is not None:
#         FIGURES_DIR = Path(FIGURES_DIR).resolve()
#     else:
#         FIGURES_DIR = (PROJECT_ROOT / "resources" / "figures").resolve()
#     FIGURES_DIR.mkdir(parents=True, exist_ok=True)

#     # -----------------------------
#     # 4) Artifacts root (optional)
#     # -----------------------------
#     if "ARTIFACTS_DIR" in globals() and ARTIFACTS_DIR is not None:
#         ARTIFACTS_DIR = Path(ARTIFACTS_DIR).resolve()
#     else:
#         ARTIFACTS_DIR = (PROJECT_ROOT / "resources" / "artifacts").resolve()
#     ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

#     # -----------------------------
#     # 5) Shared collector
#     # -----------------------------
#     if "sec2_diagnostics_rows" not in globals() or sec2_diagnostics_rows is None:
#         sec2_diagnostics_rows = []

#     return {
#         "PROJECT_ROOT": str(PROJECT_ROOT),
#         "SEC2_REPORTS_DIR": str(SEC2_REPORTS_DIR),
#         "SECTION2_REPORT_PATH": str(SECTION2_REPORT_PATH),
#         "FIGURES_DIR": str(FIGURES_DIR),
#         "ARTIFACTS_DIR": str(ARTIFACTS_DIR),
#         "sec2_diagnostics_rows_init": True,
#     }

# _boot = bootstrap_section2_paths()
# print("✅ Section 2 bootstrap:")
# for k, v in _boot.items():
#     print(f"  • {k}: {v}")
