
#
"""Sections that use this:
# 2.5
# 3.3?
# 3.4?
# --- 2.5 Part D > Path Resolver
"""

from pathlib import Path

# --- Path Resolver (robust, no strap dependency) ---
def _resolve_anomaly_context_path():
    # 1) Best: explicit global
    if "ANOMALY_CONTEXT_PATH" in globals() and globals()["ANOMALY_CONTEXT_PATH"]:
        return Path(globals()["ANOMALY_CONTEXT_PATH"]).resolve()

    # 2) If your Section 2 dirs dict exists
    if "SEC2_REPORT_DIRS" in globals() and isinstance(SEC2_REPORT_DIRS, dict):
        # Preferred: section 2.5 subdir where you’ve been putting logic outputs
        base = Path(SEC2_REPORT_DIRS.get("2.5", "")).resolve()
        if str(base) != ".":
            return (base / "logic_anomaly_context.parquet").resolve()

    # 3) If you use a generic section2 reports root
    if "sec2_reports_dir" in globals() and globals()["sec2_reports_dir"]:
        base = Path(globals()["sec2_reports_dir"]).resolve()
        return (base / "logic_anomaly_context.parquet").resolve()

    if "REPORTS_DIR" in globals() and globals()["REPORTS_DIR"]:
        base = (Path(globals()["REPORTS_DIR"]).resolve() / "section2")
        return (base / "logic_anomaly_context.parquet").resolve()

    # 4) Final fallback
    return Path("section2_reports/logic_anomaly_context.parquet").resolve()

ANOMALY_CONTEXT_PATH = _resolve_anomaly_context_path()
print("✅ ANOMALY_CONTEXT_PATH =", ANOMALY_CONTEXT_PATH)
