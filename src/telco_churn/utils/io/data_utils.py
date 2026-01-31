"""
Data utilities for Telco Churn.
"""

"""
Data loading and validation utilities.
Extracted from Level 1-2 notebooks.
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

def load_data(filepath='data/raw/telco_customer_churn.csv'):
    """
    Load the telco churn dataset.

    Parameters
    ----------
    filepath : str
        Path to the CSV file

    Returns
    -------
    pd.DataFrame
        Loaded dataset
    """
    # Implementation from your Level 1 notebook
    df = pd.read_csv(filepath)
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def validate_schema(df):
    """
    Validate that dataframe has expected columns.

    Extracted from Level 2 data quality checks.
    """
    required_columns = [
        'customerID', 'gender', 'SeniorCitizen', 'Partner', 
        'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn'
    ]

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    print("✓ Schema validation passed")
    return True

def get_data_info(df):
    """
    Get comprehensive data information.

    Consolidates various .info() and .describe() calls from notebooks.
    """
    info = {
        'shape': df.shape,
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
        'missing_values': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.value_counts().to_dict()
    }
    return info
