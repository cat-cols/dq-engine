from __future__ import annotations
import uuid
import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional
import pandas as pd

from dq_engine.config import load_config
from dq_engine.warehouse import WarehouseConnCfg, make_warehouse
from dq_engine.dbt_runner import run_dbt_build
from dq_engine.checks import CheckResult, accepted_values, row_count

def ensure_dq_table(wh, database: str, dq_schema: str) -> str:
    schema_fqn = f"{database}.{dq_schema}"
    wh.execute(f"create schema if not exists {schema_fqn}")
    table_fqn = f"{schema_fqn}.DQ_RESULTS"
    wh.execute(f"""
    create table if not exists {table_fqn} (
      run_id string,
      dataset_id string,
      check_id string,
      check_type string,
      severity string,
      status string,
      table_name string,
      column_name string,
      metric_name string,
      metric_value double,
      threshold double,
      details_json variant
    )
    """)
    return table_fqn

def run(config_path: str, skip_dbt: bool = False, run_dir: Optional[str] = None) -> str:
    cfg = load_config(config_path)
    run_id = uuid.uuid4().hex

    wh = make_warehouse(WarehouseConnCfg(
        target=cfg.warehouse.target,
        database=cfg.warehouse.database,
        raw_schema=cfg.warehouse.raw_schema,
        analytics_schema=cfg.warehouse.analytics_schema,
        dq_schema=cfg.warehouse.dq_schema,
        duckdb_path=cfg.warehouse.duckdb_path,
    ))

    if not skip_dbt:
        run_dbt_build(cfg.dbt.project_dir, cfg.dbt.profiles_dir)

    dq_table = ensure_dq_table(wh, cfg.warehouse.database, cfg.warehouse.dq_schema)

    results: List[CheckResult] = []
    for chk in cfg.checks:
        ctype = chk["type"]
        table = chk["table"]
        sev = chk.get("severity", "warn")
        cid = chk["id"]

        if ctype == "accepted_values":
            col = chk["column"]
            allowed = chk["params"]["values"]
            df = wh.read_df(f"select {col} from {table}")
            results.append(accepted_values(run_id, cfg.project.dataset_id, cid, sev, table, col, allowed, df))

        elif ctype == "row_count":
            n = int(wh.read_df(f"select count(*) as n from {table}").iloc[0,0])
            results.append(row_count(run_id, cfg.project.dataset_id, cid, sev, table, n))

        else:
            raise ValueError(f"Unknown check type: {ctype}")

    out_df = pd.DataFrame([asdict(r) for r in results])
    wh.write_df(out_df, dq_table, mode="append")

    if run_dir:
        p = Path(run_dir).resolve()
        p.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(p / "dq_results.csv", index=False)
        (p / "dq_results.json").write_text(json.dumps(out_df.to_dict(orient="records"), indent=2), encoding="utf-8")

    return run_id
