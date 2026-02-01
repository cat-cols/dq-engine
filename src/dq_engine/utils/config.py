# /Users/b/DATA/PROJECTS/Telco/_T2/Level_3/src/dq_engine/utils/config.py

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import yaml

# Bound config lives here (not notebook globals)
_BOUND_CONFIG: Dict[str, Any] = {}
_BOUND_CONFIG_PATH: Optional[str] = None

def load_config_yaml(path: str | Path) -> Dict[str, Any]:
    """Load YAML into a dict."""
    p = Path(path).expanduser().resolve()
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config YAML root must be a mapping/dict: {p}")
    return data

def bind_config(cfg: Dict[str, Any], *, path: str | Path | None = None, force: bool = False) -> None:
    global _BOUND_CONFIG, _BOUND_CONFIG_PATH
    if not force and (not isinstance(cfg, dict) or not cfg):
        raise ValueError("Refusing to bind empty config dict (use force=True if intentional)")
    _BOUND_CONFIG = cfg
    _BOUND_CONFIG_PATH = str(Path(path).expanduser().resolve()) if path else None

def load_and_bind_config(path: str | Path) -> Dict[str, Any]:
    """Convenience: load YAML and bind it in one step."""
    cfg = load_config_yaml(path)
    bind_config(cfg, path=path)
    return cfg

def C(
    key: str,
    default: Any = None,
    *,
    required: bool = False,
    config: Optional[Dict[str, Any]] = None,
    roots: Optional[Iterable[str]] = None,
) -> Any:
    """
    Safe access into config using dotted keys, e.g. C("RANGES.tenure.max").
    Reads from:
      - explicit `config` argument if provided
      - else bound config (_BOUND_CONFIG)

    Optional `roots` lets you try prefixes, e.g. roots=["DATA_QUALITY.", "NUMERIC_CHECKS."].
    """
    cfg = config if isinstance(config, dict) else _BOUND_CONFIG
    if not isinstance(cfg, dict) or not cfg:
        if required:
            raise KeyError(f"CONFIG not bound/empty. Missing key: {key}")
        return default

    if not isinstance(key, str) or not key.strip():
        if required:
            raise KeyError("Empty config key")
        return default

    prefixes = [""] + list(roots or [])
    for prefix in prefixes:
        cur: Any = cfg
        parts = (prefix + key).strip(".").split(".")
        ok = True
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                ok = False
                break
        if ok:
            return cur

    if required:
        src = _BOUND_CONFIG_PATH or "(unbound)"
        raise KeyError(f"Missing CONFIG key: {key} (config source: {src})")
    return default


def config_source() -> str:
    """Debug helper: where did the bound config come from?"""
    return _BOUND_CONFIG_PATH or "(unbound)"
