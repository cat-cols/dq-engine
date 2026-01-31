def iter_cat_cols(frame, cat_cols, where: str):
    """
    Yield categorical columns that actually exist in `frame`,
    and warn about any that are missing.
    """
    missing = [c for c in cat_cols if c not in frame.columns]
    if missing:
        print(f"⚠️ {where}: skipping {len(missing)} cat col(s) not in frame:", missing)

    for c in cat_cols:
        if c in frame.columns:
            yield c
