from pathlib import Path
from src.data.loader import DataLoader
from src.utils.config import load_config

def test_required_columns(tmp_path: Path):
    project_root = Path(__file__).resolve().parents[1]
    config = load_config(project_root / "config" / "config.yaml")
    loader = DataLoader(config)
    # e.g., assert config keys exist
    assert "required_columns" in config