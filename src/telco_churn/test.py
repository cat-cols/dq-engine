"""
tests/test_preprocessor.py

Unit tests for the TelcoPreprocessor class.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.preprocessor import TelcoPreprocessor


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    data = {
        'customerID': ['C001', 'C002', 'C003'],
        'gender': ['Male', 'Female', 'Male'],
        'SeniorCitizen': [0, 1, 0],
        'Partner': ['Yes', 'No', 'Yes'],
        'Dependents': ['No', 'Yes', 'No'],
        'tenure': [12, 24, 6],
        'PhoneService': ['Yes', 'No', 'Yes'],
        'MonthlyCharges': [50.0, 75.5, 30.25],
        'TotalCharges': ['600.0', '1810.0', '181.5'],
        'Churn': ['No', 'Yes', 'No']
    }
    return pd.DataFrame(data)


@pytest.fixture
def preprocessor():
    """Create preprocessor instance."""
    return TelcoPreprocessor()


class TestTelcoPreprocessor:
    """Test cases for TelcoPreprocessor."""
    
    def test_handle_missing_values(self, preprocessor, sample_data):
        """Test missing value handling."""
        # Add missing value
        sample_data.loc[0, 'TotalCharges'] = ' '
        
        result = preprocessor.handle_missing_values(sample_data)
        
        # Check that missing values are filled
        assert result['TotalCharges'].isnull().sum() == 0
        assert result.loc[0, 'TotalCharges'] == 0
    
    def test_drop_unnecessary_columns(self, preprocessor, sample_data):
        """Test dropping unnecessary columns."""
        result = preprocessor.drop_unnecessary_columns(sample_data)
        
        # customerID should be dropped
        assert 'customerID' not in result.columns
        assert len(result.columns) == len(sample_data.columns) - 1
    
    def test_encode_target(self, preprocessor, sample_data):
        """Test target variable encoding."""
        result = preprocessor.encode_target(sample_data)
        
        # Check encoding
        assert result['Churn'].dtype in [np.int64, np.int32]
        assert set(result['Churn'].unique()) == {0, 1}
        assert result.loc[0, 'Churn'] == 0  # 'No' -> 0
        assert result.loc[1, 'Churn'] == 1  # 'Yes' -> 1
    
    def test_encode_binary_features(self, preprocessor, sample_data):
        """Test binary feature encoding."""
        result = preprocessor.encode_binary_features(sample_data)
        
        # Check gender encoding
        assert result.loc[0, 'gender'] == 1  # Male -> 1
        assert result.loc[1, 'gender'] == 0  # Female -> 0
        
        # Check Partner encoding
        assert result.loc[0, 'Partner'] == 1  # Yes -> 1
        assert result.loc[1, 'Partner'] == 0  # No -> 0
    
    def test_preprocess_pipeline(self, preprocessor, sample_data):
        """Test full preprocessing pipeline."""
        result = preprocessor.preprocess(sample_data)
        
        # Check that customerID is dropped
        assert 'customerID' not in result.columns
        
        # Check that target is encoded
        assert result['Churn'].dtype in [np.int64, np.int32]
        
        # Check that there are more columns (one-hot encoding)
        assert len(result.columns) >= len(sample_data.columns) - 1
        
        # Check no missing values
        assert result.isnull().sum().sum() == 0
    
    def test_split_features_target(self, preprocessor, sample_data):
        """Test splitting features and target."""
        processed = preprocessor.preprocess(sample_data)
        X, y = preprocessor.split_features_target(processed)
        
        # Check shapes
        assert len(X) == len(sample_data)
        assert len(y) == len(sample_data)
        
        # Check that target is not in features
        assert 'Churn' not in X.columns
        
        # Check target values
        assert y.name == 'Churn'
    
    def test_preprocess_with_no_encoding(self, preprocessor, sample_data):
        """Test preprocessing without categorical encoding."""
        result = preprocessor.preprocess(sample_data, encode_categorical=False)
        
        # Should have fewer columns (no one-hot encoding)
        full_result = preprocessor.preprocess(sample_data, encode_categorical=True)
        assert len(result.columns) < len(full_result.columns)


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_dataframe(self, preprocessor):
        """Test with empty dataframe."""
        empty_df = pd.DataFrame()
        
        # Should handle gracefully
        result = preprocessor.handle_missing_values(empty_df)
        assert len(result) == 0
    
    def test_missing_target_column(self, preprocessor, sample_data):
        """Test error when target column is missing."""
        sample_data = sample_data.drop('Churn', axis=1)
        processed = preprocessor.preprocess(sample_data)
        
        with pytest.raises(ValueError):
            preprocessor.split_features_target(processed)
    
    def test_all_missing_total_charges(self, preprocessor, sample_data):
        """Test when all TotalCharges are missing."""
        sample_data['TotalCharges'] = ' '
        
        result = preprocessor.handle_missing_values(sample_data)
        
        # All should be filled with 0
        assert (result['TotalCharges'] == 0).all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])