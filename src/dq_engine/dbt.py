from __future__ import annotations
from typing import Optional
import os, sys, shutil, subprocess, textwrap
from pathlib import Path

def run_dbt(project_dir: Path, profiles_dir: Path, args=None):
    """
    Runs dbt via:
      1) `dbt` if present on PATH
      2) `python -m dbt` fallback (uses current kernel's Python env)
    """
    if args is None:
        args = ["build"]

    project_dir = Path(project_dir).resolve()
    profiles_dir = Path(profiles_dir).resolve()

    # Prefer dbt on PATH
    dbt_exe = shutil.which("dbt")

    if dbt_exe:
        cmd = [dbt_exe] + args + ["--project-dir", str(project_dir), "--profiles-dir", str(profiles_dir)]
        mode = f"dbt executable: {dbt_exe}"
    else:
        # Fallback: use the notebook's Python environment
        cmd = [sys.executable, "-m", "dbt"] + args + ["--project-dir", str(project_dir), "--profiles-dir", str(profiles_dir)]
        mode = f"python -m dbt (sys.executable: {sys.executable})"

    print("🧰 dbt run mode:", mode)
    print("▶️ cmd:", " ".join(cmd))

    p = subprocess.run(cmd, capture_output=True, text=True)
    print("returncode:", p.returncode)

    if p.stdout:
        print("\n--- stdout (tail) ---")
        print(p.stdout[-2000:])

    if p.stderr:
        print("\n--- stderr (tail) ---")
        print(p.stderr[-2000:])

    return p

# --- Diagnostic prints before running ---
print("PYTHON:", sys.executable)
print("DBT on PATH?:", shutil.which("dbt"))
print("DBT_PROFILES_DIR:", os.environ.get("DBT_PROFILES_DIR"))

# Run dbt
p = run_dbt(DBT_PROJECT_DIR, DBT_PROFILES_DIR, args=["build"])

def build(project_dir: str, profiles_dir: str, target: Optional[str] = None) -> None:
    cmd = ["dbt", "build", "--project-dir", project_dir, "--profiles-dir", profiles_dir]
    """
    build
    """
    if target:
        cmd += ["--target", target]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            "dbt build failed\n"
            f"STDERR:\n{p.stderr[-4000:]}\n"
            f"STDOUT:\n{p.stdout[-4000:]}"
        )