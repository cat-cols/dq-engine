# Data Quality Engine — Data Product Pipeline

⚠️ **Work in progress (portfolio project).**
This repo is an evolving, **warehouse-ready data quality engine** built to demonstrate analytics engineering practices: reproducible runs, config-driven checks, and audit-friendly outputs.

It started with the IBM Telco Customer Churn dataset as a concrete reference implementation. The goal is a **dataset-agnostic** DQ + observability layer that can plug into modern stacks (dbt + warehouse).

---

## What this is

A **config-driven data quality + validation pipeline** that:
- profiles datasets (numeric + categorical)
- runs integrity and rule checks
- produces **append-only diagnostics** and run-scoped artifacts
- generates **readiness / quality signals** suitable for downstream BI and modeling

This project prioritizes **traceability**:
- run metadata (timestamped runs)
- deterministic outputs
- dataset version/hash logging (provenance)
- repeatable execution driven by YAML configuration

---

## Architecture

**Local / notebook-first today**, evolving toward **warehouse-native** execution:

`RAW data → profiling + checks → diagnostics + artifacts → quality rollups`

Planned/active direction:

`Warehouse RAW → dbt (staging/marts/tests) → DQ Engine (deep diagnostics + scoring) → DQ_RESULTS table + reports`

---

## Quickstart (local)

```bash
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_DIR>

# Create virtual environment
python -m venv .venv

# Make a clean venv using Python 3.12
/usr/local/bin/python3.12 -m venv .venv

source .venv/bin/activate
# Windows: .venv\\Scripts\\activate

pip install -e .

# Upgrade pip
python -m pip install -U pip

# Install your repo + deps from pyproject.toml
pip install -e ".[dev,notebooks,viz,stats,ml,xai,docs]"

# Run the notebook workflow
jupyter lab
