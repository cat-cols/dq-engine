"""
Data preprocessing functions.
Extracted from Level 2 cleaning and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

def clean_data(df):
    """
    Clean the telco dataset.

    - Ensure tenure numeric
    - Convert TotalCharges to numeric (coerce invalid -> NaN)
    - Set TotalCharges = 0 when tenure == 0 and TotalCharges is NaN
    - Report remaining NaNs (so you can decide how to handle them)
    """
    df = df.copy()

    # Ensure tenure is numeric (handles '0', ' 0', etc.)
    df['tenure'] = pd.to_numeric(df['tenure'], errors='coerce').fillna(0).astype(int)

    # Normalize TotalCharges text and convert to numeric (leave NaN for now)
    df['TotalCharges'] = df['TotalCharges'].astype(str).str.strip()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Set TotalCharges = 0 where tenure == 0 and TotalCharges is missing
    mask = df['TotalCharges'].isna() & (df['tenure'] == 0)
    df.loc[mask, 'TotalCharges'] = 0

    # Report counts for visibility
    remaining_nans = df['TotalCharges'].isna().sum()
    print(f"✓ Fixed {mask.sum()} TotalCharges values where tenure = 0")
    if remaining_nans:
        print(f"⚠️  There are {remaining_nans} remaining NaN(s) in TotalCharges (inspect these rows).")

    return df


def create_features(df):
    """
    Create engineered features.

    From Level 2 feature engineering:
    - Customer value segments
    - Service counts
    - Tenure groups
    """
    df = df.copy()

    # Tenure groups (from Level 2)
    df['TenureGroup'] = pd.cut(
        df['tenure'],
        bins=[0, 12, 24, 36, 48, 72],
        labels=['0-1yr', '1-2yr', '2-3yr', '3-4yr', '4-6yr']
    )

    # Service count (simplified from Level 2)
    service_cols = ['PhoneService', 'InternetService', 'OnlineSecurity', 
                   'OnlineBackup', 'DeviceProtection', 'TechSupport']
    df['ServiceCount'] = (df[service_cols] == 'Yes').sum(axis=1)

    # Customer value (from Level 2)
    df['CustomerValue'] = pd.qcut(
        df['TotalCharges'],
        q=3,
        labels=['Low', 'Medium', 'High']
    )

    print(f"✓ Created 3 engineered features")
    return df

def prepare_for_modeling(df):
    """
    Prepare data for sklearn modeling.

    Handles encoding and feature selection.
    """
    df = df.copy()

    # Convert target to binary
    df['Churn'] = (df['Churn'] == 'Yes').astype(int)

    # Drop ID column
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)

    # Identify column types
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Remove target from feature lists
    if 'Churn' in numeric_cols:
        numeric_cols.remove('Churn')

    return df, numeric_cols, categorical_cols

def split_data(df, target='Churn', test_size=0.2, random_state=42):
    """
    Split data into train and test sets.

    Maintains class balance through stratification.
    """
    X = df.drop(target, axis=1)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Maintain churn ratio
    )

    print(f"✓ Train: {len(X_train)} samples, Test: {len(X_test)} samples")
    print(f"  Train churn rate: {y_train.mean():.2%}")
    print(f"  Test churn rate: {y_test.mean():.2%}")

    return X_train, X_test, y_train, y_test

"""
Basic preprocessing steps.
"""
import pandas as pd

def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = (
            df["TotalCharges"]
            .astype(str)
            .str.replace(r"^\s*$", "", regex=True)
        )
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df

###########

"""
Data Preprocessing Module - Critical for Model Performance

LEARNING NOTES:
- Bad data = bad models, no matter how sophisticated
- Preprocessing decisions affect all downstream analysis
- Document WHY you make certain choices (business logic)

INTERVIEW TALKING POINTS:
- "I handle the TotalCharges issue using business logic"
- "I optimize memory usage for large-scale processing"
- "I separate preprocessing from feature engineering"
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def clean_telco_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Telco dataset with business logic.

    Based on learnings from Level 2:
    - TotalCharges has whitespace for new customers
    - Business logic: tenure=0 & TotalCharges=0
    - For new customers (tenure=0): TotalCharges = 0

    Parameters
    ----------
    df : pd.DataFrame
        Raw Telco data

    Returns
    -------
    pd.DataFrame
        Cleaned data

    REAL-WORLD NOTE: This function would likely be configurable
    for different cleaning strategies per use case.
    """
    df = df.copy()

    # Convert to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Set ALL tenure==0 customers to have TotalCharges = 0
    # (not just the ones with missing values)
    new_customers = df['tenure'] == 0
    df.loc[new_customers, 'TotalCharges'] = 0

    # Handle any other missing values
    remaining_missing = df['TotalCharges'].isna()
    if remaining_missing.any():
        # Handle non-new customers with missing charges differently
        df.loc[remaining_missing, 'TotalCharges'] = df.loc[remaining_missing, 'MonthlyCharges']

    return df

def optimize_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reduce memory footprint of DataFrame.

    INTERVIEW GOLD: This shows you think about production constraints.
    A 50% memory reduction could save thousands in cloud costs.
    """
    initial_memory = df.memory_usage(deep=True).sum() / 1024**2

    # Convert object columns to category if low cardinality
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique
            df[col] = df[col].astype('category')

    # Downcast numerics
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    final_memory = df.memory_usage(deep=True).sum() / 1024**2
    reduction_pct = (initial_memory - final_memory) / initial_memory * 100

    logger.info(f"Memory reduced by {reduction_pct:.1f}% ({initial_memory:.1f}MB → {final_memory:.1f}MB)")

    return df


def prepare_for_modeling(
    df: pd.DataFrame,
    target_col: str = 'Churn',
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Prepare data for machine learning.

    PATTERN: This is where statistical analysis meets ML engineering.
    """
    from sklearn.model_selection import train_test_split

    # Encode target variable
    df[target_col] = df[target_col].map({'Yes': 1, 'No': 0})

    # Separate features and target
    X = df.drop(columns=[target_col, 'customerID'])
    y = df[target_col]

    # Create dummies for categorical variables
    X = pd.get_dummies(X, drop_first=True)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    logger.info(f"Train churn rate: {y_train.mean():.2%}, Test churn rate: {y_test.mean():.2%}")

    return X_train, X_test, y_train, y_test

#########
"""
Data Preprocessing Module - Critical for Model Performance

LEARNING NOTES:
- Bad data = bad models, no matter how sophisticated
- Preprocessing decisions affect all downstream analysis
- Document WHY you make certain choices (business logic)

INTERVIEW TALKING POINTS:
- "I handle the TotalCharges issue using business logic"
- "I optimize memory usage for large-scale processing"
- "I separate preprocessing from feature engineering"
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def clean_telco_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean Telco dataset with business logic.

    Based on learnings from Level 2:
    - TotalCharges has whitespace for new customers
    - New customers (tenure=0) should have TotalCharges=MonthlyCharges

    Parameters
    ----------
    df : pd.DataFrame
        Raw Telco data

    Returns
    -------
    pd.DataFrame
        Cleaned data

    REAL-WORLD NOTE: This function would likely be configurable
    for different cleaning strategies per use case.
    """
    df = df.copy()  # Never modify input data!

    logger.info("Starting data cleaning")

    # Fix TotalCharges (discovered in Level 2)
    # This shows you understand the data, not just running generic cleaning
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Business logic: New customers have TotalCharges = MonthlyCharges
    mask_new_customers = df['TotalCharges'].isna()
    df.loc[mask_new_customers, 'TotalCharges'] = df.loc[mask_new_customers, 'MonthlyCharges']

    logger.info(f"Fixed {mask_new_customers.sum()} TotalCharges values for new customers")

    # Convert SeniorCitizen to string for consistency
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})

    # Optimize memory (shows you think about scalability)
    df = optimize_memory_usage(df)

    return df


def optimize_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reduce memory footprint of DataFrame.

    INTERVIEW GOLD: This shows you think about production constraints.
    A 50% memory reduction could save thousands in cloud costs.
    """
    initial_memory = df.memory_usage(deep=True).sum() / 1024**2

    # Convert object columns to category if low cardinality
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique
            df[col] = df[col].astype('category')

    # Downcast numerics
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    final_memory = df.memory_usage(deep=True).sum() / 1024**2
    reduction_pct = (initial_memory - final_memory) / initial_memory * 100

    logger.info(f"Memory reduced by {reduction_pct:.1f}% ({initial_memory:.1f}MB → {final_memory:.1f}MB)")

    return df


def prepare_for_modeling(
    df: pd.DataFrame,
    target_col: str = 'Churn',
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Prepare data for machine learning.

    PATTERN: This is where statistical analysis meets ML engineering.
    """
    from sklearn.model_selection import train_test_split

    # Encode target variable
    df[target_col] = df[target_col].map({'Yes': 1, 'No': 0})

    # Separate features and target
    X = df.drop(columns=[target_col, 'customerID'])
    y = df[target_col]

    # Create dummies for categorical variables
    X = pd.get_dummies(X, drop_first=True)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    logger.info(f"Train churn rate: {y_train.mean():.2%}, Test churn rate: {y_test.mean():.2%}")

    return X_train, X_test, y_train, y_test

#########
