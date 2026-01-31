
############################
### BOOTSTRAP GRAVEYARD ####
############################


# # #
    # def load_sec2_summary(path: Path) -> pd.DataFrame:
    #     path = Path(path)
    #     if not path.exists():
    #         return pd.DataFrame()
    #     try:
    #         return pd.read_csv(path)
    #     except Exception as e:
    #         print(f"⚠️ Could not read Section 2 summary at {path}: {e}")
    #         return pd.DataFrame()


    #     # Optional: init a few global lists once (only if you really rely on them across cells)
    #     if init_globals_lists:
    #         if "sec2_diagnostics_rows" not in globals():
    #             out["sec2_diagnostics_rows"] = []
    #         if "cleaning_actions_261" not in globals():
    #             out["cleaning_actions_261"] = []

    #     if export_globals:
    #         g = globals()
    #         for k, v in out.items():
    #             g[k] = v

    #     return out

# load_summary
    # def load_summary2(path: Path) -> pd.DataFrame:
    #     if not path.exists():
    #         return pd.DataFrame()
    #     try:
    #         df = pd.read_csv(path)
    #         return df
    #     except Exception as e:
    #         print(f"⚠️ Could not read Section 2 summary at {path}: {e}")
    #         return pd.DataFrame()

# #
    # def bootstrap_section2_paths(project_root=None, verbose=True):
    #     """
    #     Bootstrap shared Section 2 paths and diagnostics helpers.
    #     (Same responsibilities as your current _bootstrap_section2_paths)
    #     """
    #     # same logic, but ideally avoid heavy use of `globals()` here
    #     """
    #     Bootstrap shared Section 2 paths and diagnostics helpers.

    #     Responsibilities:
    #     - Resolve SEC2_REPORTS_DIR (base dir for all Section 2 artifacts)
    #     - Resolve SECTION2_REPORT_PATH (unified Section 2 summary CSV)
    #     - Resolve CATEGORICAL_DIR, FIGURES_DIR, ARTIFACTS_DIR, etc. as needed
    #     - Initialize sec2_diagnostics_rows if used
    #     """
    #     global SEC2_REPORTS_DIR, SECTION2_REPORT_PATH
    #     global CATEGORICAL_DIR, FIGURES_DIR, ARTIFACTS_DIR
    #     global sec2_diagnostics_rows

    #     # Base Section 2 reports dir
    #     if "SEC2_REPORTS_DIR" in globals():
    #         SEC2_REPORTS_DIR = SEC2_REPORTS_DIR.resolve()
    #     elif "sec2_reports_dir" in globals():
    #         SEC2_REPORTS_DIR = Path(sec2_reports_dir).resolve()
    #     elif "REPORTS_DIR" in globals():
    #         SEC2_REPORTS_DIR = (REPORTS_DIR / "section2").resolve()
    #     elif "PROJECT_ROOT" in globals():
    #         SEC2_REPORTS_DIR = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
    #     else:
    #         SEC2_REPORTS_DIR = Path("resources/reports/section2").resolve()
    #     SEC2_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    #     # Unified Section 2 summary
    #     if "SECTION2_REPORT_PATH" not in globals():
    #         if "REPORTS_DIR" in globals():
    #             SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    #         elif "PROJECT_ROOT" in globals():
    #             SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    #         else:
    #             SECTION2_REPORT_PATH = (SEC2_REPORTS_DIR.parent / "section2_summary.csv").resolve()

    #     # Categorical artifacts
    #     if "CATEGORICAL_DIR" not in globals():
    #         CATEGORICAL_DIR = (SEC2_REPORTS_DIR / "categorical").resolve()
    #         CATEGORICAL_DIR.mkdir(parents=True, exist_ok=True)

    #     # Figures
    #     if "FIGURES_DIR" not in globals():
    #         if "PROJECT_ROOT" in globals():
    #             FIGURES_DIR = (PROJECT_ROOT / "resources" / "figures").resolve()
    #         else:
    #             FIGURES_DIR = (SEC2_REPORTS_DIR.parent / "figures").resolve()
    #         FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    #     # Artifacts
    #     if "ARTIFACTS_DIR" not in globals():
    #         if "PROJECT_ROOT" in globals():
    #             ARTIFACTS_DIR = (PROJECT_ROOT / "resources" / "artifacts").resolve()
    #         else:
    #             ARTIFACTS_DIR = SEC2_REPORTS_DIR
    #         ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    #     # Diagnostics collector (legacy / local driver)
    #     if "sec2_diagnostics_rows" not in globals():
    #         sec2_diagnostics_rows = []

    #     print("📁 SEC2_REPORTS_DIR:", SEC2_REPORTS_DIR)
    #     print("🧾 SECTION2_REPORT_PATH:", SECTION2_REPORT_PATH)
