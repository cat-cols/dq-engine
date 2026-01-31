#!/usr/bin/env python3
"""
Aggregate all Python code cells from a Jupyter notebook
into a new notebook with a single combined code cell.

Usage:
    python aggregate_notebook_code.py input.ipynb output.ipynb
"""

import json
import sys
from pathlib import Path


def aggregate_code_cells(input_path: Path, output_path: Path) -> None:
    # --- 1) Load the source notebook ----------------------------------------
    with input_path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    nbformat = nb.get("nbformat", 4)
    nbformat_minor = nb.get("nbformat_minor", 5)

    # --- 2) Collect all code from code cells --------------------------------
    aggregated_source_lines = []

    for idx, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue

        # cell["source"] is usually a list of lines, but can be a single string
        src = cell.get("source", [])
        if isinstance(src, str):
            src_lines = [src]
        else:
            src_lines = src

        # Optional: add a header comment to mark original cell boundaries
        aggregated_source_lines.append(f"# ===== Cell {idx} =====\n")
        aggregated_source_lines.extend(src_lines)

        # Ensure there's a blank line between cells
        if not aggregated_source_lines or not aggregated_source_lines[-1].endswith("\n"):
            aggregated_source_lines.append("\n")
        aggregated_source_lines.append("\n")

    if not aggregated_source_lines:
        print(f"No code cells found in {input_path}", file=sys.stderr)
        # Still write an empty notebook with one empty code cell
        aggregated_source_lines = ["# No code cells found in source notebook.\n"]

    # --- 3) Build the new notebook structure --------------------------------
    aggregated_cell = {
        "cell_type": "code",
        "metadata": {},
        "source": aggregated_source_lines,
        "outputs": [],
        "execution_count": None,
    }

    new_nb = {
        "cells": [aggregated_cell],
        "metadata": {
            "aggregated_from": str(input_path),
        },
        "nbformat": nbformat,
        "nbformat_minor": nbformat_minor,
    }

    # --- 4) Write the new notebook ------------------------------------------
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(new_nb, f, ensure_ascii=False, indent=1)

    print(f"✅ Aggregated notebook written to: {output_path}")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) != 2:
        print(
            "Usage: python aggregate_notebook_code.py input.ipynb output.ipynb",
            file=sys.stderr,
        )
        raise SystemExit(1)

    input_path = Path(argv[0]).expanduser().resolve()
    output_path = Path(argv[1]).expanduser().resolve()

    if not input_path.is_file():
        print(f"❌ Input notebook not found: {input_path}", file=sys.stderr)
        raise SystemExit(1)

    aggregate_code_cells(input_path, output_path)


if __name__ == "__main__":
    main()
