# 💡💡 Suggested automation (worth adding soon)

# Create a reusable function for future fixes:

def safe_read(path, empty_ok=True, **kwargs):
    """Read CSV safely — avoids EmptyDataError, returns empty DF if needed."""
    from pandas.errors import EmptyDataError
    try:
        return pd.read_csv(path, **kwargs)
    except (FileNotFoundError, EmptyDataError, ValueError):
        return pd.DataFrame() if empty_ok else None


# Replace every risky pd.read_csv() with:

# df = safe_read(NUMERIC_DIR / "rule_confidence_scores.csv")

# Then you’ll never fight this class of issue again.