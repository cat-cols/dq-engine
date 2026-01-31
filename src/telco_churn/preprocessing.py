#!/usr/bin/env python3
"""
TotalCharges Data Quality Detective Script
=========================================
This script systematically investigates the TotalCharges column to identify
and display problematic entries that can't be converted to numeric values.
"""

import pandas as pd
import numpy as np

def investigate_totalcharges(csv_file_path):
    """
    Investigate TotalCharges column for data quality issues
    
    Args:
        csv_file_path (str): Path to the telco.csv file
    """
    
    print("🔍 TOTALCHARGES DATA QUALITY INVESTIGATION")
    print("=" * 55)
    
    # Load the data
    try:
        df = pd.read_csv(csv_file_path)
        print(f"✅ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    print("\n" + "="*55)
    
    # Step 1: Check the data type
    print("STEP 1: DATA TYPE INVESTIGATION")
    print("-" * 30)
    print(f"TotalCharges data type: {df['TotalCharges'].dtype}")
    
    if df['TotalCharges'].dtype == 'object':
        print("🚨 RED FLAG: TotalCharges should be numeric but is stored as text!")
    else:
        print("✅ Data type looks correct")
    
    print("\n" + "="*55)
    
    # Step 2: Show sample values
    print("STEP 2: SAMPLE VALUES INSPECTION")
    print("-" * 32)
    print("First 10 TotalCharges values:")
    for i, val in enumerate(df['TotalCharges'].head(10)):
        print(f"  Row {i}: '{val}' (type: {type(val).__name__})")
    
    print("\n" + "="*55)
    
    # Step 3: Test numeric conversion
    print("STEP 3: NUMERIC CONVERSION TEST")
    print("-" * 31)
    
    # Try conversion with error catching
    df['TotalCharges_numeric'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Count conversion issues
    original_nulls = df['TotalCharges'].isnull().sum()
    converted_nulls = df['TotalCharges_numeric'].isnull().sum()
    conversion_failures = converted_nulls - original_nulls
    
    print(f"Original null values: {original_nulls}")
    print(f"Nulls after conversion: {converted_nulls}")
    print(f"Values that failed conversion: {conversion_failures}")
    
    if conversion_failures > 0:
        print(f"🚨 PROBLEM DETECTED: {conversion_failures} values couldn't be converted!")
    else:
        print("✅ All values converted successfully")
    
    print("\n" + "="*55)
    
    # Step 4: Identify and display problem entries
    if conversion_failures > 0:
        print("STEP 4: PROBLEM ENTRIES ANALYSIS")
        print("-" * 32)
        
        # Find rows where conversion failed
        problem_mask = (df['TotalCharges_numeric'].isnull()) & (df['TotalCharges'].notnull())
        problem_rows = df[problem_mask]
        
        print(f"Found {len(problem_rows)} problematic rows:")
        print("\nPROBLEMATIC VALUES:")
        
        # Show unique problematic values
        problem_values = problem_rows['TotalCharges'].unique()
        for val in problem_values:
            count = (problem_rows['TotalCharges'] == val).sum()
            print(f"  Value: '{val}' | Count: {count} | Length: {len(str(val))} characters")
            
            # Show character analysis for weird values
            if val.strip() != val or len(val.strip()) == 0:
                print(f"    🔍 Special analysis: repr='{repr(val)}'")
        
        print("\nSAMPLE PROBLEM ROWS:")
        # Show a few complete rows for context
        display_cols = ['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges']
        sample_problems = problem_rows[display_cols].head(5)
        print(sample_problems.to_string(index=False))
        
        print("\n" + "="*55)
        
        # Step 5: Business logic check
        print("STEP 5: BUSINESS LOGIC ANALYSIS")
        print("-" * 31)
        
        # Check if these customers have zero tenure (might explain empty TotalCharges)
        zero_tenure_problems = problem_rows[problem_rows['tenure'] == 0]
        print(f"Problem entries with zero tenure: {len(zero_tenure_problems)}")
        
        if len(zero_tenure_problems) > 0:
            print("💡 INSIGHT: Customers with zero tenure might legitimately have no total charges")
            print("Sample zero tenure customers:")
            print(zero_tenure_problems[['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges']].head(3).to_string(index=False))
    
    print("\n" + "="*55)
    
    # Step 6: Summary and recommendations
    print("STEP 6: SUMMARY & RECOMMENDATIONS")
    print("-" * 34)
    
    if conversion_failures > 0:
        print("🔧 DATA CLEANING NEEDED:")
        print("  1. Convert problematic values to NaN or 0")
        print("  2. Investigate business rules for empty values") 
        print("  3. Consider if zero tenure customers should have TotalCharges = 0")
        
        print("\n💻 SUGGESTED CLEANING CODE:")
        print("  # Replace problematic values with NaN")
        print("  df['TotalCharges_clean'] = pd.to_numeric(df['TotalCharges'], errors='coerce')")
        print("  ")
        print("  # Or replace with 0 for zero tenure customers")
        print("  df['TotalCharges_clean'] = df['TotalCharges_clean'].fillna(0)")
    else:
        print("✅ NO CLEANING NEEDED - All values are numeric!")
    
    return df

def main():
    """Main function to run the investigation"""
    
    # File path - adjust this to your actual file location
    csv_file_path = 'data/telco.csv'  # Adjust path as needed
    
    print("TotalCharges Data Quality Detective")
    print("=" * 35)
    print("This script will investigate the TotalCharges column for data quality issues.")
    print(f"Looking for file: {csv_file_path}")
    print()
    
    # Run the investigation
    df = investigate_totalcharges(csv_file_path)
    
    if df is not None:
        print("\n🎯 INVESTIGATION COMPLETE!")
        print("Review the findings above to understand what data cleaning is needed.")

if __name__ == "__main__":
    main()


# """
# Data Preprocessing Module - Critical for Model Performance

# LEARNING NOTES:
# - Bad data = bad models, no matter how sophisticated
# - Preprocessing decisions affect all downstream analysis
# - Document WHY you make certain choices (business logic)

# INTERVIEW TALKING POINTS:
# - "I handle the TotalCharges issue using business logic"
# - "I optimize memory usage for large-scale processing"
# - "I separate preprocessing from feature engineering"
# """

# import pandas as pd
# import numpy as np
# import logging
# from typing import Optional, Tuple

# logger = logging.getLogger(__name__)


# def clean_telco_data(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Clean Telco dataset with business logic.

#     Based on learnings from Level 2:
#     - TotalCharges has whitespace for new customers
#     - New customers (tenure=0) should have TotalCharges=MonthlyCharges

#     Parameters
#     ----------
#     df : pd.DataFrame
#         Raw Telco data

#     Returns
#     -------
#     pd.DataFrame
#         Cleaned data

#     REAL-WORLD NOTE: This function would likely be configurable
#     for different cleaning strategies per use case.
#     """
#     df = df.copy()
#     logger.info("Starting data cleaning")

#     # --- Normalize & coerce TotalCharges safely ---
#     # 1) ensure string, 2) strip spaces, 3) blank -> NaN, 4) to numeric
#     tc = (df['TotalCharges']
#             .astype('string')
#             .str.strip()
#             .replace('', np.nan))
#     df['TotalCharges'] = pd.to_numeric(tc, errors='coerce')

#     # --- Apply Telco-specific business rule ONLY to new customers ---
#     mask_new = (df['tenure'].astype('int', errors='ignore') == 0) & (df['TotalCharges'].isna())
#     fixed_count = int(mask_new.sum())
#     df.loc[mask_new, 'TotalCharges'] = 0.0
#     logger.info(f"Set TotalCharges=0 for {fixed_count} rows (tenure==0 & blank TotalCharges).")

#     # Convert SeniorCitizen to friendly labels
#     df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})

#     # Optional: fail fast if any TotalCharges still NaN
#     remaining_nans = int(df['TotalCharges'].isna().sum())
#     if remaining_nans:
#         logger.warning(f"{remaining_nans} rows still have NaN TotalCharges after cleaning.")

#     # Memory optimization
#     df = optimize_memory_usage(df)
#     return df


# def optimize_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Reduce memory footprint of DataFrame.

#     INTERVIEW GOLD: This shows you think about production constraints.
#     A 50% memory reduction could save thousands in cloud costs.
#     """
#     initial_memory = df.memory_usage(deep=True).sum() / 1024**2

#     # Convert object columns to category if low cardinality
#     for col in df.select_dtypes(include=['object']).columns:
#         if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique
#             df[col] = df[col].astype('category')

#     # Downcast numerics
#     for col in df.select_dtypes(include=['float']).columns:
#         df[col] = pd.to_numeric(df[col], downcast='float')

#     for col in df.select_dtypes(include=['int']).columns:
#         df[col] = pd.to_numeric(df[col], downcast='integer')

#     final_memory = df.memory_usage(deep=True).sum() / 1024**2
#     reduction_pct = (initial_memory - final_memory) / initial_memory * 100

#     logger.info(f"Memory reduced by {reduction_pct:.1f}% ({initial_memory:.1f}MB → {final_memory:.1f}MB)")

#     return df


# def prepare_for_modeling(
#     df: pd.DataFrame,
#     target_col: str = 'Churn',
#     test_size: float = 0.2,
#     random_state: int = 42
# ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
#     """
#     Prepare data for ML
#     PATTERN: This is where statistical analysis meets ML engineering.
#     """
#     from sklearn.model_selection import train_test_split

#     # Encode target variable
#     df[target_col] = df[target_col].map({'Yes': 1, 'No': 0})

#     # Separate features and target
#     X = df.drop(columns=[target_col, 'customerID'])
#     y = df[target_col]

#     # Create dummies for categorical variables
#     X = pd.get_dummies(X, drop_first=True)

#     # Split data
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=test_size, random_state=random_state, stratify=y
#     )

#     logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
#     logger.info(f"Train churn rate: {y_train.mean():.2%}, Test churn rate: {y_test.mean():.2%}")

#     return X_train, X_test, y_train, y_test


# """
# Basic preprocessing steps.
# """
# import pandas as pd

# def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
#     for c in cols:
#         df[c] = pd.to_numeric(df[c], errors="coerce")
#     return df

# def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
#     if "TotalCharges" in df.columns:
#         df["TotalCharges"] = (
#             df["TotalCharges"]
#             .astype(str)
#             .str.replace(r"^\s*$", "", regex=True)
#         )
#         df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
#     return df


"""
# src/data/preprocessor.py

# Data preprocessing module for Telco Churn dataset.
# Handles cleaning, encoding, and transformation of raw data.
# """

# import pandas as pd
# import numpy as np
# import logging
# from typing import Tuple, List, Optional

# logger = logging.getLogger(__name__)


# class TelcoPreprocessor:
#     """
#     Preprocesses Telco customer data for modeling.
    
#     Handles missing values, type conversions, encoding, and data cleaning.
#     """
    
#     def __init__(self):
#         """Initialize the preprocessor with default settings."""
#         self.binary_columns = ['gender', 'Partner', 'Dependents', 
#                                'PhoneService', 'PaperlessBilling']
#         self.columns_to_drop = ['customerID']
#         self.target_column = 'Churn'
        
#     def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Handle missing values in the dataset.
        
#         Args:
#             df (pd.DataFrame): Input dataframe
            
#         Returns:
#             pd.DataFrame: Dataframe with missing values handled
#         """
#         df = df.copy()
        
#         # Convert TotalCharges to numeric (handles spaces)
#         df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        
#         # Fill missing TotalCharges with 0 (likely new customers)
#         missing_count = df['TotalCharges'].isnull().sum()
#         if missing_count > 0:
#             logger.info(f"Filling {missing_count} missing TotalCharges values with 0")
#             df['TotalCharges'].fillna(0, inplace=True)
        
#         return df
    
#     def drop_unnecessary_columns(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Drop columns not needed for modeling.
        
#         Args:
#             df (pd.DataFrame): Input dataframe
            
#         Returns:
#             pd.DataFrame: Dataframe with unnecessary columns removed
#         """
#         df = df.copy()
#         existing_cols = [col for col in self.columns_to_drop if col in df.columns]
        
#         if existing_cols:
#             logger.info(f"Dropping columns: {existing_cols}")
#             df = df.drop(columns=existing_cols)
        
#         return df
    
#     def encode_target(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Encode target variable to binary.
        
#         Args:
#             df (pd.DataFrame): Input dataframe
            
#         Returns:
#             pd.DataFrame: Dataframe with encoded target
#         """
#         df = df.copy()
        
#         if self.target_column in df.columns:
#             df[self.target_column] = df[self.target_column].map({'Yes': 1, 'No': 0})
#             logger.info("Target variable encoded: Yes=1, No=0")
        
#         return df
    
#     def encode_binary_features(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Encode binary categorical features.
        
#         Args:
#             df (pd.DataFrame): Input dataframe
            
#         Returns:
#             pd.DataFrame: Dataframe with encoded binary features
#         """
#         df = df.copy()
        
#         for col in self.binary_columns:
#             if col in df.columns:
#                 if col == 'gender':
#                     df[col] = df[col].map({'Male': 1, 'Female': 0})
#                 else:
#                     df[col] = df[col].map({'Yes': 1, 'No': 0})
        
#         logger.info(f"Binary features encoded: {self.binary_columns}")
#         return df
    
#     def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Apply one-hot encoding to multi-class categorical features.
        
#         Args:
#             df (pd.DataFrame): Input dataframe
            
#         Returns:
#             pd.DataFrame: Dataframe with one-hot encoded features
#         """
#         df = df.copy()
        
#         # Identify remaining categorical columns
#         categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
#         if categorical_cols:
#             logger.info(f"One-hot encoding columns: {categorical_cols}")
#             df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
#         return df
    
#     def preprocess(self, df: pd.DataFrame, 
#                    encode_categorical: bool = True) -> pd.DataFrame:
#         """
#         Execute full preprocessing pipeline.
        
#         Args:
#             df (pd.DataFrame): Raw input dataframe
#             encode_categorical (bool): Whether to one-hot encode categorical features
            
#         Returns:
#             pd.DataFrame: Fully preprocessed dataframe
#         """
#         logger.info("Starting preprocessing pipeline")
        
#         df = self.handle_missing_values(df)
#         df = self.drop_unnecessary_columns(df)
#         df = self.encode_target(df)
#         df = self.encode_binary_features(df)
        
#         if encode_categorical:
#             df = self.encode_categorical_features(df)
        
#         logger.info(f"Preprocessing complete. Final shape: {df.shape}")
#         return df
    
#     def split_features_target(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
#         """
#         Split dataframe into features and target.
        
#         Args:
#             df (pd.DataFrame): Preprocessed dataframe
            
#         Returns:
#             Tuple[pd.DataFrame, pd.Series]: Features (X) and target (y)
#         """
#         if self.target_column not in df.columns:
#             raise ValueError(f"Target column '{self.target_column}' not found")
        
#         X = df.drop(self.target_column, axis=1)
#         y = df[self.target_column]
        
#         logger.info(f"Split data: X shape {X.shape}, y shape {y.shape}")
#         return X, y


# def preprocess_telco_data(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Convenience function for quick preprocessing.
    
#     Args:
#         df (pd.DataFrame): Raw dataframe
        
#     Returns:
#         pd.DataFrame: Preprocessed dataframe
#     """
#     preprocessor = TelcoPreprocessor()
#     return preprocessor.preprocess(df)


# if __name__ == "__main__":
#     # Example usage
#     from src.data.loader import load_telco_data
    
#     df_raw = load_telco_data("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
#     preprocessor = TelcoPreprocessor()
#     df_processed = preprocessor.preprocess(df_raw)
#     X, y = preprocessor.split_features_target(df_processed)
    
#     print(f"Processed data shape: {df_processed.shape}")
#     print(f"Features: {X.shape}, Target: {y.shape}")
