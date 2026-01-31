# scripts/run_analysis.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.data.loader import DataLoader
from src.utils.config import load_config

def main():
    config = load_config(PROJECT_ROOT / "config" / "config.yaml")
    loader = DataLoader(config)
    df = loader.load_telco_data(PROJECT_ROOT / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    print(df.head())

if __name__ == "__main__":
    main()
