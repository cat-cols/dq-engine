from __future__ import annotations
import subprocess
from typing import Optional

def run_dbt_build(project_dir: str, profiles_dir: str, target: Optional[str] = None) -> None:
    cmd = ["dbt", "build", "--project-dir", project_dir, "--profiles-dir", profiles_dir]
    if target:
        cmd += ["--target", target]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            "dbt build failed\n"
            f"STDERR:\n{p.stderr[-4000:]}\n"
            f"STDOUT:\n{p.stdout[-4000:]}"
        )
