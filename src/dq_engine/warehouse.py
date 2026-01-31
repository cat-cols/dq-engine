from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import pandas as pd

@dataclass(frozen=True)
class WarehouseConnCfg:
    target: str
    database: str
    raw_schema: str
    analytics_schema: str
    dq_schema: str
    duckdb_path: Optional[str] = None

class Warehouse:
    def read_df(self, sql: str) -> pd.DataFrame: ...
    def execute(self, sql: str) -> None: ...
    def write_df(self, df: pd.DataFrame, table_fqn: str, mode: str = "append") -> None: ...

def make_warehouse(cfg: WarehouseConnCfg) -> Warehouse:
    t = cfg.target.lower()
    if t == "duckdb":
        return DuckDBWarehouse(path=cfg.duckdb_path or "data/warehouse/dq_warehouse.duckdb")
    if t == "snowflake":
        return SnowflakeWarehouse()
    raise ValueError(f"Unknown warehouse target: {cfg.target}")

class DuckDBWarehouse(Warehouse):
    def __init__(self, path: str):
        import duckdb
        self.path = path
        self.con = duckdb.connect(path)

    def read_df(self, sql: str) -> pd.DataFrame:
        return self.con.execute(sql).df()

    def execute(self, sql: str) -> None:
        self.con.execute(sql)

    def write_df(self, df: pd.DataFrame, table_fqn: str, mode: str = "append") -> None:
        self.con.register("_dq_tmp", df)
        if mode == "replace":
            self.con.execute(f"create or replace table {table_fqn} as select * from _dq_tmp")
        else:
            self.con.execute(f"insert into {table_fqn} select * from _dq_tmp")

class SnowflakeWarehouse(Warehouse):
    def __init__(self):
        import os
        import snowflake.connector
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend

        key_path = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH")
        key_pass = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE", "")
        if not key_path:
            raise RuntimeError("SNOWFLAKE_PRIVATE_KEY_PATH is required (key-pair auth).")

        pem_bytes = open(key_path, "rb").read()
        password_bytes = key_pass.encode("utf-8") if key_pass else None

        pkey = serialization.load_pem_private_key(
            pem_bytes,
            password=password_bytes,
            backend=default_backend(),
        )

        private_key_der = pkey.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        self.ctx = snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            role=os.environ.get("SNOWFLAKE_ROLE"),
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
            database=os.environ.get("SNOWFLAKE_DATABASE"),
            schema=os.environ.get("SNOWFLAKE_SCHEMA"),
            private_key=private_key_der,
        )

    def read_df(self, sql: str) -> pd.DataFrame:
        cur = self.ctx.cursor()
        try:
            cur.execute(sql)
            return cur.fetch_pandas_all()
        finally:
            cur.close()

    def execute(self, sql: str) -> None:
        cur = self.ctx.cursor()
        try:
            cur.execute(sql)
        finally:
            cur.close()

    def write_df(self, df: pd.DataFrame, table_fqn: str, mode: str = "append") -> None:
        from snowflake.connector.pandas_tools import write_pandas

        db, schema, table = table_fqn.split(".", 2)
        ok, _, _, _ = write_pandas(
            conn=self.ctx,
            df=df,
            table_name=table,
            database=db,
            schema=schema,
            auto_create_table=True,
        )
        if not ok:
            raise RuntimeError(f"write_pandas failed for {table_fqn}")
