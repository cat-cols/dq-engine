
#
def make_sec2_summary(
    section: str,
    section_name: str,
    check: str,
    level: str = "info",
    status: str = "OK",
    detail: str | None = None,
    metrics: dict | None = None,
    use_utc: bool = True,
) -> pd.DataFrame:
    """
    Build a single-row Section 2 summary DataFrame
    with consistent schema & ordering.
    """
    metrics = metrics or {}
    ts = pd.Timestamp.utcnow() if use_utc else pd.Timestamp.now()

    base = {
        "section":      section,
        "section_name": section_name,
        "check":        check,
        "level":        level,
        "status":       status,
        **metrics,
        "timestamp":    ts,
        "detail":       detail,
    }
    return pd.DataFrame([base])

# usage
summary_223 = make_sec2_summary(
    section="2.2.3",
    section_name="Binary field detection",
    check="Detect binary-like columns and flag semantics",
    status="OK",
    detail=(
        "Binary catalog → binary_field_report.csv; "
        "feeds downstream numeric/categorical checks"
    ),
    metrics={
        "n_columns":           int(binary_df.shape[0]),
        "n_binary_candidates": n_binary_candidates,
        "n_binary_features":   n_binary_features,
    },
)

def make_sec2_summary(
    section: str,
    section_name: str,
    check: str,
    status,
    detail_path=None,
    level: str = "info",
    metrics: dict | None = None,
):
    """
    Build a 1-row DataFrame for a Section 2 summary entry.

    metrics: dict of extra metric_name -> value
    """
    base = {
        "section": section,
        "section_name": section_name,
        "check": check,
        "level": level,
        "status": status,
        "detail": getattr(detail_path, "name", None),
        "timestamp": pd.Timestamp.utcnow(),
    }

    if metrics:
        # Optionally coerce obvious ints (you can skip this if you prefer)
        for k, v in metrics.items():
            try:
                base[k] = int(v)
            except (TypeError, ValueError):
                base[k] = v

    return pd.DataFrame([base])
