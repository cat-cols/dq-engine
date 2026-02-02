# -atomic
"""
Keywords: logging, diagnostics, csv_append, atomic_write
That keeps: * Section 2 logic **semantic** (_append_sec2) * Implementation **reusable** (atomic_append_csv in your library) 
--- ## How to tag it in your snippet library 
💡💡 I’d store this as something like:
* **Category:** Data Quality / Reporting
* **Name:** atomic_csv_append_schema_union 
* **Keywords:** logging, diagnostics, csv_append, atomic_write 
And **delete** this old inline block from your notebook, or at least:
You recently suggested this style pattern and categorize it like: 
* **Category:** Data Quality / Reporting 
* **Name:** atomic_csv_append_schema_union 
* **Keywords:** logging, diagnostics, csv_append, atomic_write
"""
from pathlib import Path
import os
import pandas as pd

def atomic_append_csv(path: Path, chunk_df: pd.DataFrame) -> None:
    """
    Append rows to a CSV file with schema union and atomic replace.

    - path: Path to the CSV file (not a directory).
    - chunk_df: DataFrame with one or more rows to append.
    """
    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    # Ensure folder exists
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        existing = pd.read_csv(path)
        all_cols = pd.Index(existing.columns).union(chunk_df.columns)
        out = pd.concat(
            [
                existing.reindex(columns=all_cols),
                chunk_df.reindex(columns=all_cols),
            ],
            ignore_index=True,
        )
    else:
        out = chunk_df.copy()

    out.to_csv(tmp_path, index=False)
    os.replace(tmp_path, path)

from telco_churn.utils.io import atomic_append_csv  # for example

# -append
def _append_sec2(sec2_chunk: pd.DataFrame) -> None:
    atomic_append_csv(SECTION2_REPORT_PATH, sec2_chunk)


###
from pathlib import Path
import os
import pandas as pd

def atomic_append_csv(path: Path, chunk_df: pd.DataFrame) -> None:
    """
    Append rows to a CSV file with schema union and atomic replace.

    Parameters
    ----------
    path : Path or str
        Target CSV file path.
    chunk_df : pd.DataFrame
        One or more rows to append.
    """
    path = Path(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        existing = pd.read_csv(path)
        all_cols = pd.Index(existing.columns).union(chunk_df.columns)
        out = pd.concat(
            [
                existing.reindex(columns=all_cols),
                chunk_df.reindex(columns=all_cols),
            ],
            ignore_index=True,
        )
    else:
        out = chunk_df.copy()

    out.to_csv(tmp_path, index=False)
    os.replace(tmp_path, path)

###
from pathlib import Path
import pandas as pd
from atomic_csv_append_schema_union import atomic_append_csv

SECTION2_REPORT_PATH = Path("section2_data_quality_example.csv")

def _append_sec2(sec2_chunk: pd.DataFrame) -> None:
    atomic_append_csv(SECTION2_REPORT_PATH, sec2_chunk)
