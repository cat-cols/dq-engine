from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

@dataclass(frozen=True)
class WarehouseCfg:
    target: str
    database: str
    raw_schema: str
    analytics_schema: str
    dq_schema: str
    duckdb_path: Optional[str] = None

@dataclass(frozen=True)
class DbtCfg:
    project_dir: str
    profiles_dir: str

@dataclass(frozen=True)
class ProjectCfg:
    name: str
    dataset_id: str

@dataclass(frozen=True)
class AppCfg:
    project: ProjectCfg
    warehouse: WarehouseCfg
    dbt: DbtCfg
    datasets: Dict[str, Any]
    checks: list[dict[str, Any]]

def load_config(path: str | Path) -> AppCfg:
    p = Path(path)
    obj = yaml.safe_load(p.read_text(encoding="utf-8"))
    return AppCfg(
        project=ProjectCfg(**obj["project"]),
        warehouse=WarehouseCfg(**obj["warehouse"]),
        dbt=DbtCfg(**obj["dbt"]),
        datasets=obj.get("datasets", {}),
        checks=obj.get("checks", []),
    )
