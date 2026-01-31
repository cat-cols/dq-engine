"""
src/models/train.py

Model training module for Telco Churn prediction.
Handles training multiple models and hyperparameter tuning.
"""

import pandas as pd
import numpy as np
import logging
import joblib
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score

logger = logging.getLogger(__name__)


class TelcoModelTrainer:
    """
    Trains and manages machine learning models for churn prediction.
    """
    
    def __init__(self, random_state: int = 42):
        """
        Initialize model trainer.
        
        Args:
            random_state (int): Random seed for reproducibility
        """
        self.random_state = random_state
        self.models = {}
        self.scalers = {}
        self.best_model = None
        self.best_model_name = None
        
        # Select best model
        self.best_model_name = max(results, key=lambda x: results[x]['roc_auc'])
        self.best_model = results[self.best_model_name]['model']
        logger.info(f"Best model: {self.best_model_name}")
        
        return results
    
    def save_model(self, model_name: str, save_path: str) -> None:
        """
        Save a trained model to disk.
        
        Args:
            model_name (str): Name of the model to save
            save_path (str): Path where model will be saved
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.models[model_name], save_path)
        logger.info(f"Model saved to {save_path}")
    
    def load_model(self, model_name: str, load_path: str) -> Any:
        """
        Load a trained model from disk.
        
        Args:
            model_name (str): Name to assign to loaded model
            load_path (str): Path to the saved model
            
        Returns:
            Loaded model
        """
        model = joblib.load(load_path)
        self.models[model_name] = model
        logger.info(f"Model loaded from {load_path}")
        return model


def train_churn_models(X: pd.DataFrame, y: pd.Series, 
                       test_size: float = 0.2,
                       tune_hyperparams: bool = False) -> Dict:
    """
    Convenience function to train all models.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target
        test_size (float): Test set proportion
        tune_hyperparams (bool): Whether to tune hyperparameters
        
    Returns:
        Dict: Training results
    """
    trainer = TelcoModelTrainer()
    X_train, X_test, y_train, y_test = trainer.prepare_data(X, y, test_size)
    results = trainer.train_all_models(X_train, X_test, y_train, y_test, 
                                       tune_hyperparams)
    return results


if __name__ == "__main__":
    # Example usage
    from src.data.loader import load_telco_data
    from src.data.preprocessor import TelcoPreprocessor
    from src.features.engineer import TelcoFeatureEngineer
    
    # Load and process data
    df = load_telco_data("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    engineer = TelcoFeatureEngineer()
    df = engineer.engineer_features(df)
    
    preprocessor = TelcoPreprocessor()
    df = preprocessor.preprocess(df)
    X, y = preprocessor.split_features_target(df)
    
    # Train models
    trainer = TelcoModelTrainer()
    X_train, X_test, y_train, y_test = trainer.prepare_data(X, y)
    results = trainer.train_all_models(X_train, X_test, y_train, y_test)
    
    print(f"\nBest model: {trainer.best_model_name}")
    print(f"ROC-AUC: {results[trainer.best_model_name]['roc_auc']:.4f}") Define model configurations
        self.model_configs = {
            'logistic_regression': {
                'model': LogisticRegression(random_state=random_state, max_iter=1000),
                'needs_scaling': True,
                'param_grid': {
                    'C': [0.01, 0.1, 1, 10],
                    'penalty': ['l2'],
                    'solver': ['lbfgs']
                }
            },
            'random_forest': {
                'model': RandomForestClassifier(random_state=random_state),
                'needs_scaling': False,
                'param_grid': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [10, 20, None],
                    'min_samples_split': [2, 5, 10]
                }
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(random_state=random_state),
                'needs_scaling': False,
                'param_grid': {
                    'n_estimators': [50, 100, 150],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7]
                }
            }
        }
    
    def prepare_data(self, X: pd.DataFrame, y: pd.Series, 
                    test_size: float = 0.2) -> Tuple:
        """
        Split and prepare data for training.
        
        Args:
            X (pd.DataFrame): Features
            y (pd.Series): Target variable
            test_size (float): Proportion of data for testing
            
        Returns:
            Tuple: X_train, X_test, y_train, y_test
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        logger.info(f"Data split: train={len(X_train)}, test={len(X_test)}")
        logger.info(f"Train churn rate: {y_train.mean()*100:.2f}%")
        logger.info(f"Test churn rate: {y_test.mean()*100:.2f}%")
        
        return X_train, X_test, y_train, y_test
    
    def scale_features(self, X_train: pd.DataFrame, 
                      X_test: pd.DataFrame,
                      numerical_cols: Optional[list] = None) -> Tuple:
        """
        Scale numerical features using StandardScaler.
        
        Args:
            X_train (pd.DataFrame): Training features
            X_test (pd.DataFrame): Test features
            numerical_cols (list): List of numerical columns to scale
            
        Returns:
            Tuple: Scaled X_train and X_test
        """
        if numerical_cols is None:
            numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges',
                            'total_services', 'avg_charge_per_service',
                            'customer_value_score']
        
        # Only scale columns that exist
        cols_to_scale = [col for col in numerical_cols if col in X_train.columns]
        
        if not cols_to_scale:
            logger.warning("No numerical columns found to scale")
            return X_train, X_test
        
        scaler = StandardScaler()
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        
        X_train_scaled[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
        X_test_scaled[cols_to_scale] = scaler.transform(X_test[cols_to_scale])
        
        self.scalers['standard_scaler'] = scaler
        logger.info(f"Scaled {len(cols_to_scale)} numerical features")
        
        return X_train_scaled, X_test_scaled
    
    def train_model(self, model_name: str, X_train: pd.DataFrame, 
                   y_train: pd.Series, tune_hyperparams: bool = False) -> Any:
        """
        Train a single model.
        
        Args:
            model_name (str): Name of the model to train
            X_train (pd.DataFrame): Training features
            y_train (pd.Series): Training target
            tune_hyperparams (bool): Whether to perform hyperparameter tuning
            
        Returns:
            Trained model
        """
        if model_name not in self.model_configs:
            raise ValueError(f"Model {model_name} not found in configurations")
        
        config = self.model_configs[model_name]
        model = config['model']
        
        logger.info(f"Training {model_name}...")
        
        if tune_hyperparams:
            logger.info(f"Performing hyperparameter tuning for {model_name}...")
            grid_search = GridSearchCV(
                model, config['param_grid'], cv=5, 
                scoring='roc_auc', n_jobs=-1, verbose=0
            )
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            logger.info(f"Best parameters: {grid_search.best_params_}")
        else:
            model.fit(X_train, y_train)
        
        self.models[model_name] = model
        logger.info(f"✓ {model_name} trained successfully")
        
        return model
    
    def train_all_models(self, X_train: pd.DataFrame, X_test: pd.DataFrame,
                        y_train: pd.Series, y_test: pd.Series,
                        tune_hyperparams: bool = False) -> Dict[str, Any]:
        """
        Train all configured models.
        
        Args:
            X_train, X_test (pd.DataFrame): Training and test features
            y_train, y_test (pd.Series): Training and test targets
            tune_hyperparams (bool): Whether to tune hyperparameters
            
        Returns:
            Dict: Dictionary of trained models with results
        """
        results = {}
        
        for model_name, config in self.model_configs.items():
            # Prepare data (scale if needed)
            if config['needs_scaling']:
                X_train_proc, X_test_proc = self.scale_features(X_train, X_test)
            else:
                X_train_proc, X_test_proc = X_train, X_test
            
            # Train model
            model = self.train_model(model_name, X_train_proc, y_train, 
                                   tune_hyperparams)
            
            # Evaluate on test set
            y_pred = model.predict(X_test_proc)
            y_pred_proba = model.predict_proba(X_test_proc)[:, 1]
            
            results[model_name] = {
                'model': model,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'roc_auc': roc_auc_score(y_test, y_pred_proba)
            }
            
            logger.info(f"{model_name} ROC-AUC: {results[model_name]['roc_auc']:.4f}")
        
        #