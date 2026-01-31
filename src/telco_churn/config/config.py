# src/utils/config.py
from pathlib import Path
import yaml

def load_config(config_path: str | Path) -> dict:
    """Load YAML config into a dict."""
    config_path = Path(config_path)
    with config_path.open("r") as f:
        return yaml.safe_load(f)

#
def _cfg_path(key: str) -> Path:
    """Small helper: get a relative path from config, fail loudly if missing/None."""
    rel = C(key, None)
    if rel is None or (isinstance(rel, str) and not rel.strip()):
        raise KeyError(
            f"❌ Config key {key!r} is missing or empty. "
            f"Check your CONFIG['PATHS'] block (e.g., PATHS.RAW_DATA)."
        )
    return PROJECT_ROOT / rel


# ACCESS
# # Telco/Level_3/src/telco_churn/config/access.py

# from typing import Any

# _MISSING = object()

# def C(key: str, default: Any = _MISSING) -> Any:
#     from telco_churn.config.state import CONFIG  # or from a global, depending on how you wire it

#     parts = key.split(".")
#     cur: Any = CONFIG
#     for p in parts:
#         if not isinstance(cur, dict) or p not in cur:
#             if default is _MISSING:
#                 raise KeyError(f"CONFIG missing key path: {key}")
#             return default
#         cur = cur[p]
#     return cur
