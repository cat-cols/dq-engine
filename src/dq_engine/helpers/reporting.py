
# dq_engine/helpers/reporting.py
def emit_section_summary(
    section,
    section_name,
    check,
    status,
    metrics=None,
    detail=None,
    notes=None,
    level="info",
):
    row = {
        "section": section,
        "section_name": section_name,
        "check": check,
        "level": level,
        "status": status,
        "detail": detail,
        "notes": notes,
        "timestamp": pd.Timestamp.utcnow(),
    }
    if metrics:
        row.update(metrics)

    df = pd.DataFrame([row])
    append_sec2(df, SECTION2_REPORT_PATH)
    display(df)
    return df

# Notebooks usage(footer):
emit_section_summary(
    section="2.7.5",
    section_name="Categorical–numeric relationship tests",
    check="Run ANOVA/Kruskal tests for numeric differences across categories",
    status=catnum_status_275,
    metrics={
        "n_tests_run": n_tests_run_275,
        "n_significant": n_significant_275,
    },
    detail=catnum_detail_275,
)