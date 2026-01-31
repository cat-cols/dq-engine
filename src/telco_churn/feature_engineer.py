"""
src/features/engineer.py

Feature engineering module for Telco Churn dataset.
Creates new features from existing data to improve model performance.
"""

import pandas as pd
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)


class TelcoFeatureEngineer:
    """
    Creates engineered features for Telco customer churn prediction.
    """
    
    def __init__(self):
        """Initialize feature engineer with service column definitions."""
        self.service_columns = [
            'PhoneService', 'MultipleLines', 'InternetService',
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
            'TechSupport', 'StreamingTV', 'StreamingMovies'
        ]
    
    def create_tenure_groups(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create categorical tenure groups.
        
        Args:
            df (pd.DataFrame): Input dataframe with 'tenure' column
            
        Returns:
            pd.DataFrame: Dataframe with added 'tenure_group' column
        """
        df = df.copy()
        
        df['tenure_group'] = pd.cut(
            df['tenure'],
            bins=[0, 12, 24, 48, 72],
            labels=['0-1 year', '1-2 years', '2-4 years', '4+ years']
        )
        
        logger.info("Created tenure groups")
        return df
    
    def create_charge_groups(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create categorical monthly charge groups.
        
        Args:
            df (pd.DataFrame): Input dataframe with 'MonthlyCharges' column
            
        Returns:
            pd.DataFrame: Dataframe with added 'monthly_charges_group' column
        """
        df = df.copy()
        
        df['monthly_charges_group'] = pd.cut(
            df['MonthlyCharges'],
            bins=[0, 35, 65, 90, 120],
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        logger.info("Created monthly charge groups")
        return df
    
    def calculate_total_services(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate total number of services per customer.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with added 'total_services' column
        """
        df = df.copy()
        df['total_services'] = 0
        
        for col in self.service_columns:
            if col in df.columns:
                # Count as service if not 'No' or 'No internet/phone service'
                df['total_services'] += (
                    (df[col] != 'No') &
                    (df[col] != 'No internet service') &
                    (df[col] != 'No phone service')
                ).astype(int)
        
        logger.info("Calculated total services per customer")
        return df
    
    def calculate_avg_charge_per_service(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate average monthly charge per service.
        
        Args:
            df (pd.DataFrame): Input dataframe with 'MonthlyCharges' and 'total_services'
            
        Returns:
            pd.DataFrame: Dataframe with added 'avg_charge_per_service' column
        """
        df = df.copy()
        
        # Add 1 to avoid division by zero
        df['avg_charge_per_service'] = (
            df['MonthlyCharges'] / (df['total_services'] + 1)
        )
        
        logger.info("Calculated average charge per service")
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between important variables.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with added interaction features
        """
        df = df.copy()
        
        # Contract and payment method interaction
        if 'Contract' in df.columns and 'PaymentMethod' in df.columns:
            df['contract_payment'] = df['Contract'] + '_' + df['PaymentMethod']
            logger.info("Created contract-payment interaction feature")
        
        # Tenure and contract interaction (if still categorical)
        if 'tenure_group' in df.columns and 'Contract' in df.columns:
            df['tenure_contract'] = (
                df['tenure_group'].astype(str) + '_' + df['Contract']
            )
            logger.info("Created tenure-contract interaction feature")
        
        return df
    
    def create_customer_value_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a customer value score based on tenure and charges.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with added 'customer_value_score' column
        """
        df = df.copy()
        
        # Normalize tenure and total charges
        tenure_norm = (df['tenure'] - df['tenure'].min()) / (
            df['tenure'].max() - df['tenure'].min()
        )
        charges_norm = (df['TotalCharges'] - df['TotalCharges'].min()) / (
            df['TotalCharges'].max() - df['TotalCharges'].min()
        )
        
        # Simple weighted score
        df['customer_value_score'] = 0.4 * tenure_norm + 0.6 * charges_norm
        
        logger.info("Created customer value score")
        return df
    
    def engineer_features(self, df: pd.DataFrame, 
                         include_interactions: bool = True) -> pd.DataFrame:
        """
        Execute full feature engineering pipeline.
        
        Args:
            df (pd.DataFrame): Input dataframe
            include_interactions (bool): Whether to create interaction features
            
        Returns:
            pd.DataFrame: Dataframe with engineered features
        """
        logger.info("Starting feature engineering pipeline")
        
        df = self.create_tenure_groups(df)
        df = self.create_charge_groups(df)
        df = self.calculate_total_services(df)
        df = self.calculate_avg_charge_per_service(df)
        df = self.create_customer_value_score(df)
        
        if include_interactions:
            df = self.create_interaction_features(df)
        
        logger.info(f"Feature engineering complete. Final shape: {df.shape}")
        return df


def engineer_telco_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function for quick feature engineering.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with engineered features
    """
    engineer = TelcoFeatureEngineer()
    return engineer.engineer_features(df)


if __name__ == "__main__":
    # Example usage
    from src.data.loader import load_telco_data
    
    df = load_telco_data("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    engineer = TelcoFeatureEngineer()
    df_engineered = engineer.engineer_features(df)
    
    print(f"Original shape: {df.shape}")
    print(f"Engineered shape: {df_engineered.shape}")
    print(f"New features added: {df_engineered.shape[1] - df.shape[1]}")
