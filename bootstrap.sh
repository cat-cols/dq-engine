#!/usr/bin/env bash
# Run in CLI with: bash scripts/bootstrap.sh
set -euo pipefail

PYTHON="${PYTHON:-python3}"

$PYTHON -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev,notebooks]"
python -c "import pandas, duckdb; print('✅ deps ok')"
