from __future__ import annotations

import argparse
import os
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(prog="dq", description="dq-engine CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # -----------------------
    # dq init
    # -----------------------
    p_init = sub.add_parser("init", help="Create env/setup_summary.json from template")
    p_init.add_argument("--force", action="store_true", help="Overwrite if exists")
    p_init.add_argument("--raw-data", default=None, help="Override raw_data path (relative or absolute)")
    p_init.add_argument("--config-path", default=None, help="Override config path (relative or absolute)")

    # -----------------------
    # dq run
    # -----------------------
    p_run = sub.add_parser("run", help="Run dbt + DQ checks, write results to warehouse")
    p_run.add_argument("--config", required=True, help="Path to dq config (YAML/JSON)")
    p_run.add_argument("--skip-dbt", action="store_true", help="Skip dbt execution step")
    p_run.add_argument("--run-dir", default=os.environ.get("DQ_RUN_DIR", ""), help="Override run directory")

    args = parser.parse_args()

    if args.cmd == "init":
        # Import only when needed (keeps CLI snappy)
        from dq_engine.init_project import init_project

        init_project(
            force=bool(args.force),
            raw_data=args.raw_data,
            config_path=args.config_path,
        )
        return

    if args.cmd == "run":
        # Import only when needed
        from dq_engine.pipeline import run

        run_dir = args.run_dir.strip() or None
        run_id = run(args.config, skip_dbt=bool(args.skip_dbt), run_dir=run_dir)
        print(run_id)
        return
