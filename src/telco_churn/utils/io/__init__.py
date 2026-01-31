"""
Telco Customer Churn Analysis Package
Level 3: First modular implementation
"""

__version__ = "0.3.0"

# Make key functions easily accessible
from .data_utils import load_data, validate_schema
from .preprocessing import clean_data, create_features, split_data
from .modeling import train_baseline, evaluate_model, save_pipeline

__all__ = [
    'load_data',
    'clean_data', 
    'create_features',
    'split_data',
    'train_baseline',
    'evaluate_model',
    'save_pipeline'
]
