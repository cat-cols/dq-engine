"""
Utilities for Data Quality Engine
"""
from pathlib import Path
import pandas as pd
import yaml

def load_config(path: str | Path = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_raw_csv(cfg: dict) -> pd.DataFrame:
    csv_path = Path(cfg["paths"]["data_raw"])
    return pd.read_csv(csv_path)

def save_processed(df: pd.DataFrame, cfg: dict) -> None:
    out = Path(cfg["paths"]["data_processed"])
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
