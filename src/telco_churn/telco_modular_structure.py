"""
Telco Churn Analysis - Modularized Project Structure

telco_churn_project/
│
├── data/
│   ├── raw/                    # Original datasets
│   ├── processed/              # Cleaned and processed data
│   └── interim/                # Intermediate data transformations
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/                        # Source code modules
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py          # Data loading functions
│   │   └── preprocessor.py    # Data cleaning and preprocessing
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineer.py        # Feature engineering functions
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py           # Model training functions
│   │   └── evaluate.py        # Model evaluation functions
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── plots.py           # Plotting functions
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_preprocessor.py
│   ├── test_features.py
│   └── test_models.py
│
├── models/                     # Saved model files
│   └── trained_models/
│
├── reports/                    # Generated reports and figures
│   └── figures/
│
├── config/
│   └── config.yaml            # Configuration file
│
├── requirements.txt           # Project dependencies
├── setup.py                   # Package setup
├── README.md                  # Project documentation
└── main.py                    # Main execution script
"""
