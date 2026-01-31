"""
main.py

Main execution script for Telco Customer Churn Analysis.
Orchestrates the entire pipeline from data loading to model evaluation.
"""

import logging
import argparse
from pathlib import Path
import pandas as pd

from src.data.loader import TelcoDataLoader
from src.data.preprocessor import TelcoPreprocessor
from src.features.engineer import TelcoFeatureEngineer
from src.models.train import TelcoModelTrainer
from src.models.evaluate import TelcoModelEvaluator
from src.visualization.plots import TelcoVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Telco Customer Churn Analysis Pipeline'
    )
    parser.add_argument(
        '--data_path',
        type=str,
        default='data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv',
        help='Path to the raw data file'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='reports',
        help='Directory for output files and reports'
    )
    parser.add_argument(
        '--tune_hyperparams',
        action='store_true',
        help='Perform hyperparameter tuning (slower)'
    )
    parser.add_argument(
        '--save_models',
        action='store_true',
        help='Save trained models to disk'
    )
    parser.add_argument(
        '--test_size',
        type=float,
        default=0.2,
        help='Proportion of data for testing (default: 0.2)'
    )
    
    return parser.parse_args()


def run_pipeline(data_path: str, output_dir: str, 
                tune_hyperparams: bool = False,
                save_models: bool = False,
                test_size: float = 0.2) -> dict:
    """
    Execute the complete analysis pipeline.
    
    Args:
        data_path (str): Path to raw data
        output_dir (str): Directory for outputs
        tune_hyperparams (bool): Whether to tune hyperparameters
        save_models (bool): Whether to save trained models
        test_size (float): Test set proportion
        
    Returns:
        dict: Pipeline results
    """
    logger.info("="*60)
    logger.info("TELCO CUSTOMER CHURN ANALYSIS PIPELINE")
    logger.info("="*60)
    
    # Create output directories
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / 'figures').mkdir(exist_ok=True)
    (output_path / 'models').mkdir(exist_ok=True)
    (output_path / 'data').mkdir(exist_ok=True)
    
    # Step 1: Load Data
    logger.info("\n" + "="*60)
    logger.info("STEP 1: LOADING DATA")
    logger.info("="*60)
    
    loader = TelcoDataLoader(data_path)
    df_raw = loader.load_data()
    validation = loader.validate_data()
    summary = loader.get_data_summary()
    
    logger.info(f"Dataset shape: {summary['shape']}")
    logger.info(f"Churn rate: {summary['churn_rate']:.2f}%")
    
    # Step 2: Feature Engineering
    logger.info("\n" + "="*60)
    logger.info("STEP 2: FEATURE ENGINEERING")
    logger.info("="*60)
    
    engineer = TelcoFeatureEngineer()
    df_engineered = engineer.engineer_features(df_raw.copy())
    
    # Step 3: Data Preprocessing
    logger.info("\n" + "="*60)
    logger.info("STEP 3: DATA PREPROCESSING")
    logger.info("="*60)
    
    preprocessor = TelcoPreprocessor()
    df_processed = preprocessor.preprocess(df_engineered)
    
    # Save processed data
    processed_path = output_path / 'data' / 'processed_data.csv'
    df_processed.to_csv(processed_path, index=False)
    logger.info(f"Processed data saved to {processed_path}")
    
    # Split features and target
    X, y = preprocessor.split_features_target(df_processed)
    
    # Step 4: Visualization
    logger.info("\n" + "="*60)
    logger.info("STEP 4: CREATING VISUALIZATIONS")
    logger.info("="*60)
    
    visualizer = TelcoVisualizer()
    
    # Target distribution
    visualizer.plot_target_distribution(
        df_raw, 
        save_path=output_path / 'figures' / 'target_distribution.png'
    )
    
    # Categorical features
    categorical_cols = ['Contract', 'PaymentMethod', 'InternetService']
    visualizer.plot_categorical_churn(
        df_raw, 
        categorical_cols,
        save_path=output_path / 'figures' / 'categorical_churn.png'
    )
    
    # Numerical features
    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    visualizer.plot_numerical_distributions(
        df_raw,
        numerical_cols,
        save_path=output_path / 'figures' / 'numerical_distributions.png'
    )
    
    # Correlation matrix
    visualizer.plot_correlation_matrix(
        df_processed,
        columns=['tenure', 'MonthlyCharges', 'TotalCharges', 
                'total_services', 'Churn'],
        save_path=output_path / 'figures' / 'correlation_matrix.png'
    )
    
    # Step 5: Model Training
    logger.info("\n" + "="*60)
    logger.info("STEP 5: TRAINING MODELS")
    logger.info("="*60)
    
    trainer = TelcoModelTrainer()
    X_train, X_test, y_train, y_test = trainer.prepare_data(X, y, test_size)
    
    results = trainer.train_all_models(
        X_train, X_test, y_train, y_test,
        tune_hyperparams=tune_hyperparams
    )
    
    # Step 6: Model Evaluation
    logger.info("\n" + "="*60)
    logger.info("STEP 6: EVALUATING MODELS")
    logger.info("="*60)
    
    evaluator = TelcoModelEvaluator()
    
    # Evaluate each model
    for model_name, result in results.items():
        eval_results = evaluator.evaluate_model(
            model_name,
            y_test.values,
            result['predictions'],
            result['probabilities']
        )
        results[model_name].update(eval_results)
    
    # Create comparison dataframe
    comparison_df = evaluator.compare_models(results)
    logger.info("\n" + "="*60)
    logger.info("MODEL COMPARISON")
    logger.info("="*60)
    print("\n", comparison_df)
    
    # Save comparison
    comparison_path = output_path / 'model_comparison.csv'
    comparison_df.to_csv(comparison_path)
    logger.info(f"Model comparison saved to {comparison_path}")
    
    # Step 7: Create evaluation visualizations
    logger.info("\n" + "="*60)
    logger.info("STEP 7: CREATING EVALUATION VISUALIZATIONS")
    logger.info("="*60)
    
    visualizer.plot_model_comparison(
        results,
        save_path=output_path / 'figures' / 'model_comparison.png'
    )
    
    visualizer.plot_confusion_matrices(
        results,
        save_path=output_path / 'figures' / 'confusion_matrices.png'
    )
    
    # Feature importance for best model
    best_model_name = trainer.best_model_name
    if 'random_forest' in best_model_name.lower() or 'gradient' in best_model_name.lower():
        importance_df = evaluator.get_feature_importance(
            trainer.best_model,
            X.columns.tolist()
        )
        
        if importance_df is not None:
            visualizer.plot_feature_importance(
                importance_df,
                save_path=output_path / 'figures' / 'feature_importance.png'
            )
            
            # Save feature importance
            importance_path = output_path / 'feature_importance.csv'
            importance_df.to_csv(importance_path, index=False)
            logger.info(f"Feature importance saved to {importance_path}")
    
    # Step 8: Save models (optional)
    if save_models:
        logger.info("\n" + "="*60)
        logger.info("STEP 8: SAVING MODELS")
        logger.info("="*60)
        
        for model_name in results.keys():
            model_path = output_path / 'models' / f'{model_name}.pkl'
            trainer.save_model(model_name, str(model_path))
    
    # Final summary
    logger.info("\n" + "="*60)
    logger.info("PIPELINE COMPLETE")
    logger.info("="*60)
    logger.info(f"Best Model: {trainer.best_model_name}")
    logger.info(f"Best ROC-AUC: {results[trainer.best_model_name]['roc_auc']:.4f}")
    logger.info(f"All outputs saved to: {output_path}")
    
    return {
        'results': results,
        'best_model': trainer.best_model,
        'best_model_name': trainer.best_model_name,
        'comparison': comparison_df
    }


def main():
    """Main entry point."""
    args = parse_arguments()
    
    try:
        pipeline_results = run_pipeline(
            data_path=args.data_path,
            output_dir=args.output_dir,
            tune_hyperparams=args.tune_hyperparams,
            save_models=args.save_models,
            test_size=args.test_size
        )
        
        logger.info("\n✓ Pipeline executed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()