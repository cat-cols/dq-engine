
from pathlib import Path
import os

# locate setup_summary.json
def locate_setup_summary(start: Path) -> Path:
    # try direct upwards walk
    for parent in [start] + list(start.parents):
        candidate = parent / "setup_summary.json"
        if candidate.exists():
            return candidate

    # fallback: repo root via .git
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            repo_root = parent
            break
    else:
        raise FileNotFoundError("❌ .git root not found")

    _tier = os.getenv("TIER_LEVEL") or "_T2"
    _level = os.getenv("LEVEL_NAME") or "Level_3"
    level_guess = repo_root / _tier / _level / "resources"

    candidates = [
        repo_root / "setup_summary.json",
        level_guess / "env" / "setup_summary.json",
        repo_root / _tier / _level / "env" / "setup_summary.json",
    ]

    for cand in candidates:
        if cand.exists():
            return cand

    raise FileNotFoundError("❌ setup_summary.json not found")

# Then in notebook it becomes
# if setup_summary is None:
#     setup_summary_path = locate_setup_summary(CURRENT_PATH)
#     with setup_summary_path.open("r", encoding="utf-8") as f:
#         setup_summary = json.load(f)