"""
Model training and evaluation functions.
New for Level 3 - your first modeling utilities!
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)
import joblib
import json

def create_preprocessor(numeric_cols, categorical_cols):
    """
    Create preprocessing pipeline for mixed data types.
    """
    # Numeric: standardize
    numeric_transformer = StandardScaler()

    # Categorical: one-hot encode
    categorical_transformer = OneHotEncoder(
        drop='first',  # Avoid dummy variable trap
        sparse_output=False,
        handle_unknown='ignore'
    )

    # Combine
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    return preprocessor

def train_baseline(X_train, y_train, numeric_cols, categorical_cols):
    """
    Train baseline logistic regression model.

    Returns complete pipeline including preprocessing.
    """
    # Create preprocessing pipeline
    preprocessor = create_preprocessor(numeric_cols, categorical_cols)

    # Create full pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            random_state=42,
            max_iter=1000
        ))
    ])

    # Train
    pipeline.fit(X_train, y_train)
    print("✓ Baseline model trained")

    return pipeline

def evaluate_model(pipeline, X_test, y_test):
    """
    Evaluate model performance.

    Returns dictionary of metrics.
    """
    # Get predictions
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_prob)
    }

    # Print summary
    print("\n📊 Model Performance:")
    print(f"  Accuracy:  {metrics['accuracy']:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall:    {metrics['recall']:.3f}")
    print(f"  F1-Score:  {metrics['f1']:.3f}")
    print(f"  ROC-AUC:   {metrics['roc_auc']:.3f}")

    return metrics

def save_pipeline(pipeline, metrics, model_path='models/baseline_logistic.pkl',
                 metrics_path='models/model_metrics.json'):
    """
    Save trained pipeline and metrics.
    """
    from pathlib import Path

    # Create directory
    Path(model_path).parent.mkdir(exist_ok=True)

    # Save model
    joblib.dump(pipeline, model_path)
    print(f"✓ Model saved to {model_path}")

    # Save metrics
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Metrics saved to {metrics_path}")

def load_pipeline(model_path='models/baseline_logistic.pkl'):
    """
    Load saved pipeline for predictions.
    """
    pipeline = joblib.load(model_path)
    print(f"✓ Model loaded from {model_path}")
    return pipeline
