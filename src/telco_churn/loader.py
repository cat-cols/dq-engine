"""
Data Loading Module - The Foundation of Any Data Pipeline

LEARNING NOTES:
- In production, data rarely comes from CSV files
- This module would connect to databases, APIs, or data lakes
- Validation at load time prevents downstream errors
- Type hints show you understand modern Python

INTERVIEW TALKING POINTS:
- "I separate data loading from processing for maintainability"
- "I validate data at ingestion to fail fast"
- "I use logging instead of print for production debugging"
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# Professional logging setup (not print statements!)
logger = logging.getLogger(__name__)

class DataLoader:
    """
    Professional data loading with validation.

    In real jobs, this might inherit from an abstract base class
    or implement an interface for different data sources.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize with configuration dictionary.

        PATTERN: Dependency injection - config is passed in, not hardcoded
        """
        self.config = config
        self.required_columns = [
            'customerID', 'gender', 'SeniorCitizen', 'Partner',
            'Dependents', 'tenure', 'PhoneService', 'MultipleLines',
            'InternetService', 'OnlineSecurity', 'OnlineBackup',
            'DeviceProtection', 'TechSupport', 'StreamingTV',
            'StreamingMovies', 'Contract', 'PaperlessBilling',
            'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
        ]

    def load_data(
        self,
        filepath: Optional[str] = None,
        validate: bool = True
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load and validate Telco customer data.

        Parameters
        ----------
        filepath : Optional[str]
            Path to data file. If None, uses config default
        validate : bool
            Whether to run validation checks

        Returns
        -------
        Tuple[pd.DataFrame, Dict[str, Any]]
            Loaded dataframe and validation report

        Raises
        ------
        FileNotFoundError
            If data file doesn't exist
        ValueError
            If validation fails

        Examples
        --------
        >>> loader = DataLoader(config)
        >>> df, report = loader.load_data('data/telco.csv')
        >>> print(f"Loaded {len(df)} records")

        INTERVIEW NOTE: Tuple returns show you think about metadata
        """
        filepath = filepath or self.config.get('data_path')
        filepath = Path(filepath)

        if not filepath.exists():
            logger.error(f"Data file not found: {filepath}")
            raise FileNotFoundError(f"Data file not found: {filepath}")

        logger.info(f"Loading data from {filepath}")

        # Load data
        df = pd.read_csv(filepath)

        # Create validation report (shows attention to data quality)
        report = {
            'rows_loaded': len(df),
            'columns_loaded': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        }

        if validate:
            validation_results = self._validate_data(df)
            report.update(validation_results)

        logger.info(f"Successfully loaded {report['rows_loaded']} rows")

        return df, report

    def _validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive data validation.

        PATTERN: Private method (underscore prefix) for internal use
        """
        results = {}

        # Check for missing columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            logger.warning(f"Missing columns: {missing_cols}")
        results['missing_columns'] = list(missing_cols)

        # Check for duplicates (data quality issue)
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Found {duplicates} duplicate rows")
        results['duplicate_rows'] = duplicates

        # Check for missing values
        missing_values = df.isnull().sum()
        columns_with_missing = missing_values[missing_values > 0].to_dict()
        if columns_with_missing:
            logger.warning(f"Columns with missing values: {columns_with_missing}")
        results['missing_values'] = columns_with_missing

        # Data type validation
        results['dtypes'] = df.dtypes.to_dict()

        return results

#
def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """
    Convenience function for quick loading and cleaning.

    PATTERN: Facade pattern - simple interface to complex operations
    This is what most users would actually call.
    """
    from telco_analysis.data.preprocessor import clean_telco_data

    config = {'data_path': filepath}
    loader = DataLoader(config)
    df, _ = loader.load_data()
    df_clean = clean_telco_data(df)

    return df_clean

# src/data/loader.py
"""Data loading module."""
import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Handle data loading operations.

    Parameters
    ----------
    config : dict
        Configuration dictionary. Expected keys:
        - 'required_columns' (list[str]): Columns that must exist in the dataset.
    """
    def __init__(self, config: dict):
        self.config = config

    def load_telco_data(self, filepath: str) -> pd.DataFrame:
        """Load and validate Telco dataset."""
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        self._validate_columns(df)
        return df

    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Validate required columns exist."""
        required = self.config['required_columns']
        missing = set(required) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    # def _optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
    #     """Downcast numeric columns to save memory."""
    #     for col in df.select_dtypes(include=["int", "float"]).columns:
    #         df[col] = pd.to_numeric(df[col], downcast="unsigned") if df[col].min() >= 0 else pd.to_numeric(df[col], downcast="integer")
    #     return df

    # def _clean_total_charges(self, df: pd.DataFrame) -> pd.DataFrame:
    #     """Coerce TotalCharges to numeric, filling blanks with 0."""
    #     if "TotalCharges" in df.columns:
    #         df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", 0), errors="coerce")
    #     return df

"""
# src/data/loader.py

# Data loading module for Telco Churn dataset.
# Handles reading and initial validation of raw data.
# """

# import pandas as pd
# import logging
# from pathlib import Path
# from typing import Optional

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# class TelcoDataLoader:
#     """
#     Handles loading and basic validation of Telco customer data.
    
#     Attributes:
#         data_path (Path): Path to the raw data file
#         df (pd.DataFrame): Loaded dataframe
#     """
    
#     def __init__(self, data_path: str):
#         """
#         Initialize the data loader.
        
#         Args:
#             data_path (str): Path to the CSV file
#         """
#         self.data_path = Path(data_path)
#         self.df: Optional[pd.DataFrame] = None
        
#     def load_data(self) -> pd.DataFrame:
#         """
#         Load data from CSV file.
        
#         Returns:
#             pd.DataFrame: Loaded dataframe
            
#         Raises:
#             FileNotFoundError: If data file doesn't exist
#         """
#         if not self.data_path.exists():
#             raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
#         logger.info(f"Loading data from {self.data_path}")
#         self.df = pd.read_csv(self.data_path)
#         logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        
#         return self.df
    
#     def validate_data(self) -> dict:
#         """
#         Perform basic data validation checks.
        
#         Returns:
#             dict: Validation results with checks and their status
#         """
#         if self.df is None:
#             raise ValueError("No data loaded. Call load_data() first.")
        
#         validation_results = {
#             'total_rows': len(self.df),
#             'total_columns': len(self.df.columns),
#             'duplicate_rows': self.df.duplicated().sum(),
#             'missing_values': self.df.isnull().sum().to_dict(),
#             'column_types': self.df.dtypes.to_dict()
#         }
        
#         logger.info("Data validation complete")
#         return validation_results
    
#     def get_data_summary(self) -> dict:
#         """
#         Get comprehensive summary of the dataset.
        
#         Returns:
#             dict: Summary statistics and information
#         """
#         if self.df is None:
#             raise ValueError("No data loaded. Call load_data() first.")
        
#         summary = {
#             'shape': self.df.shape,
#             'churn_rate': (self.df['Churn'] == 'Yes').mean() * 100,
#             'numeric_summary': self.df.describe().to_dict(),
#             'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist(),
#             'numeric_columns': self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
#         }
        
#         return summary


# def load_telco_data(file_path: str) -> pd.DataFrame:
#     """
#     Convenience function to quickly load Telco data.
    
#     Args:
#         file_path (str): Path to the CSV file
        
#     Returns:
#         pd.DataFrame: Loaded dataframe
#     """
#     loader = TelcoDataLoader(file_path)
#     return loader.load_data()


# if __name__ == "__main__":
#     # Example usage
#     loader = TelcoDataLoader("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
#     df = loader.load_data()
#     validation = loader.validate_data()
#     summary = loader.get_data_summary()
    
#     print(f"Loaded dataset with shape: {summary['shape']}")
#     print(f"Churn rate: {summary['churn_rate']:.2f}%")
