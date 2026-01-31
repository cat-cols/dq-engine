"""
src/models/evaluate.py

Model evaluation module for Telco Churn prediction.
Provides comprehensive evaluation metrics and analysis.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Tuple
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)

logger = logging.getLogger(__name__)


class TelcoModelEvaluator:
    """
    Evaluates trained models for churn prediction.
    """
    
    def __init__(self):
        """Initialize the evaluator."""
        self.evaluation_results = {}
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray,
                         y_pred_proba: np.ndarray) -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true (np.ndarray): True labels
            y_pred (np.ndarray): Predicted labels
            y_pred_proba (np.ndarray): Predicted probabilities
            
        Returns:
            Dict: Dictionary of metric names and values
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_pred_proba)
        }
        
        return metrics
    
    def get_confusion_matrix(self, y_true: np.ndarray, 
                           y_pred: np.ndarray) -> np.ndarray:
        """
        Calculate confusion matrix.
        
        Args:
            y_true (np.ndarray): True labels
            y_pred (np.ndarray): Predicted labels
            
        Returns:
            np.ndarray: Confusion matrix
        """
        return confusion_matrix(y_true, y_pred)
    
    def get_classification_report(self, y_true: np.ndarray,
                                 y_pred: np.ndarray) -> str:
        """
        Generate detailed classification report.
        
        Args:
            y_true (np.ndarray): True labels
            y_pred (np.ndarray): Predicted labels
            
        Returns:
            str: Classification report
        """
        return classification_report(y_true, y_pred, 
                                    target_names=['No Churn', 'Churn'])
    
    def calculate_roc_curve(self, y_true: np.ndarray,
                          y_pred_proba: np.ndarray) -> Tuple:
        """
        Calculate ROC curve data.
        
        Args:
            y_true (np.ndarray): True labels
            y_pred_proba (np.ndarray): Predicted probabilities
            
        Returns:
            Tuple: (fpr, tpr, thresholds)
        """
        return roc_curve(y_true, y_pred_proba)
    
    def calculate_precision_recall_curve(self, y_true: np.ndarray,
                                        y_pred_proba: np.ndarray) -> Tuple:
        """
        Calculate precision-recall curve data.
        
        Args:
            y_true (np.ndarray): True labels
            y_pred_proba (np.ndarray): Predicted probabilities
            
        Returns:
            Tuple: (precision, recall, thresholds)
        """
        return precision_recall_curve(y_true, y_pred_proba)
    
    def evaluate_model(self, model_name: str, y_true: np.ndarray,
                      y_pred: np.ndarray, y_pred_proba: np.ndarray) -> Dict:
        """
        Perform comprehensive evaluation of a single model.
        
        Args:
            model_name (str): Name of the model
            y_true (np.ndarray): True labels
            y_pred (np.ndarray): Predicted labels
            y_pred_proba (np.ndarray): Predicted probabilities
            
        Returns:
            Dict: Comprehensive evaluation results
        """
        logger.info(f"Evaluating {model_name}...")
        
        metrics = self.calculate_metrics(y_true, y_pred, y_pred_proba)
        cm = self.get_confusion_matrix(y_true, y_pred)
        report = self.get_classification_report(y_true, y_pred)
        fpr, tpr, roc_thresholds = self.calculate_roc_curve(y_true, y_pred_proba)
        precision, recall, pr_thresholds = self.calculate_precision_recall_curve(
            y_true, y_pred_proba
        )
        
        results = {
            'metrics': metrics,
            'confusion_matrix': cm,
            'classification_report': report,
            'roc_curve': {'fpr': fpr, 'tpr': tpr, 'thresholds': roc_thresholds},
            'pr_curve': {'precision': precision, 'recall': recall, 
                        'thresholds': pr_thresholds}
        }
        
        self.evaluation_results[model_name] = results
        logger.info(f"✓ {model_name} evaluation complete")
        
        return results
    
    def compare_models(self, results_dict: Dict[str, Dict]) -> pd.DataFrame:
        """
        Compare multiple models side by side.
        
        Args:
            results_dict (Dict): Dictionary of model results
            
        Returns:
            pd.DataFrame: Comparison dataframe
        """
        comparison_data = {}
        
        for model_name, results in results_dict.items():
            if 'metrics' in results:
                metrics = results['metrics']
            else:
                # Assume results dict has predictions
                metrics = self.calculate_metrics(
                    results.get('y_true'),
                    results.get('predictions'),
                    results.get('probabilities')
                )
            
            comparison_data[model_name] = metrics
        
        df = pd.DataFrame(comparison_data).T
        df = df.round(4)
        
        logger.info("Model comparison complete")
        return df
    
    def get_feature_importance(self, model: Any, 
                              feature_names: list,
                              top_n: int = 20) -> pd.DataFrame:
        """
        Extract feature importance from tree-based models.
        
        Args:
            model: Trained model with feature_importances_ attribute
            feature_names (list): List of feature names
            top_n (int): Number of top features to return
            
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if not hasattr(model, 'feature_importances_'):
            logger.warning("Model does not have feature_importances_ attribute")
            return None
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False).head(top_n)
        
        logger.info(f"Extracted top {top_n} feature importances")
        return importance_df
    
    def print_evaluation_summary(self, model_name: str) -> None:
        """
        Print formatted evaluation summary for a model.
        
        Args:
            model_name (str): Name of the model
        """
        if model_name not in self.evaluation_results:
            logger.error(f"No evaluation results found for {model_name}")
            return
        
        results = self.evaluation_results[model_name]
        metrics = results['metrics']
        cm = results['confusion_matrix']
        
        print("\n" + "="*50)
        print(f"EVALUATION SUMMARY: {model_name}")
        print("="*50)
        
        print("\nPerformance Metrics:")
        for metric_name, value in metrics.items():
            print(f"  {metric_name.replace('_', ' ').title()}: {value:.4f}")
        
        print("\nConfusion Matrix:")
        print(f"  TN: {cm[0,0]}  FP: {cm[0,1]}")
        print(f"  FN: {cm[1,0]}  TP: {cm[1,1]}")
        
        print("\nClassification Report:")
        print(results['classification_report'])


def evaluate_churn_model(model, X_test: pd.DataFrame, 
                        y_test: pd.Series) -> Dict:
    """
    Convenience function to evaluate a single model.
    
    Args:
        model: Trained model
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): Test target
        
    Returns:
        Dict: Evaluation results
    """
    evaluator = TelcoModelEvaluator()
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    results = evaluator.evaluate_model(
        'model', y_test.values, y_pred, y_pred_proba
    )
    
    return results


if __name__ == "__main__":
    # Example usage
    from src.models.train import TelcoModelTrainer
    from src.data.loader import load_telco_data
    from src.data.preprocessor import TelcoPreprocessor
    
    # Load and prepare data
    df = load_telco_data("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    preprocessor = TelcoPreprocessor()
    df = preprocessor.preprocess(df)
    X, y = preprocessor.split_features_target(df)
    
    # Train models
    trainer = TelcoModelTrainer()
    X_train, X_test, y_train, y_test = trainer.prepare_data(X, y)
    results = trainer.train_all_models(X_train, X_test, y_train, y_test)
    
    # Evaluate models
    evaluator = TelcoModelEvaluator()
    
    for model_name, result in results.items():
        evaluator.evaluate_model(
            model_name, y_test.values,
            result['predictions'], result['probabilities']
        )
        evaluator.print_evaluation_summary(model_name)
    
    # Compare all models
    comparison = evaluator.compare_models(results)
    print("\n" + "="*50)
    print("MODEL COMPARISON")
    print("="*50)
    print(comparison)