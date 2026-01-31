"""
Feature Engineering Module - Where Domain Knowledge Meets Data

LEARNING NOTES:
- Good features > Complex models
- Domain knowledge drives feature creation
- Always validate new features statistically

INTERVIEW TALKING POINTS:
- "I create features based on business understanding"
- "I validate feature importance before adding complexity"
- "I document the business logic behind each feature"
"""

import pandas as pd
import numpy as np
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered features for Telco dataset.

    Each feature has a business justification:
    1. tenure_group: Customer lifecycle stage
    2. avg_charges_per_tenure: Value efficiency
    3. services_count: Engagement level
    4. has_streaming: Entertainment package indicator
    5. has_protection: Security conscious indicator
    6. payment_type_risk: Based on churn analysis

    Returns
    -------
    pd.DataFrame
        Original dataframe with new features added
    """
    df = df.copy()

    logger.info("Creating engineered features")

    # 1. Customer lifecycle stage
    df['tenure_group'] = pd.cut(
        df['tenure'],
        bins=[0, 12, 24, 48, 72],
        labels=['0-1yr', '1-2yr', '2-4yr', '4-6yr'],
        include_lowest=True
    )

    # 2. Average charges per month of tenure (customer value)
    df['avg_charges_per_tenure'] = df['TotalCharges'] / (df['tenure'] + 1)

    # 3. Service adoption count (engagement)
    service_columns = [
        'PhoneService', 'InternetService', 'OnlineSecurity',
        'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies'
    ]

    df['services_count'] = 0
    for col in service_columns:
        if col in df.columns:
            # Count 'Yes' or specific service types
            df['services_count'] += df[col].isin(['Yes', 'DSL', 'Fiber optic']).astype(int)

    # 4. Has streaming services (lifestyle indicator)
    df['has_streaming'] = (
        (df['StreamingTV'] == 'Yes') | (df['StreamingMovies'] == 'Yes')
    ).astype(int)

    # 5. Has protection services (risk-averse indicator)
    df['has_protection'] = (
        (df['OnlineSecurity'] == 'Yes') | 
        (df['OnlineBackup'] == 'Yes') | 
        (df['DeviceProtection'] == 'Yes')
    ).astype(int)

    # 6. Payment method risk score (from historical analysis)
    payment_risk_map = {
        'Electronic check': 3,  # Highest churn
        'Mailed check': 2,
        'Bank transfer (automatic)': 1,
        'Credit card (automatic)': 1
    }
    df['payment_risk_score'] = df['PaymentMethod'].map(payment_risk_map)

    # 7. Contract commitment level
    contract_score_map = {
        'Month-to-month': 0,
        'One year': 1,
        'Two year': 2
    }
    df['contract_commitment'] = df['Contract'].map(contract_score_map)

    logger.info(f"Created {7} engineered features")

    return df


def select_features_for_modeling(
    df: pd.DataFrame,
    target_col: str = 'Churn',
    exclude_cols: Optional[List[str]] = None
) -> List[str]:
    """
    Select features for modeling based on data types and business logic.

    PATTERN: Feature selection as a separate concern from feature creation
    """
    exclude_cols = exclude_cols or ['customerID']

    # Start with all columns
    features = list(df.columns)

    # Remove target and excluded columns
    features = [f for f in features if f not in exclude_cols + [target_col]]

    # Identify high-cardinality categoricals to potentially exclude
    high_cardinality = []
    for col in features:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            if df[col].nunique() > 10:
                high_cardinality.append(col)
                logger.warning(f"High cardinality categorical: {col} ({df[col].nunique()} unique values)")
    
    logger.info(f"Selected {len(features)} features for modeling")
    
    return features