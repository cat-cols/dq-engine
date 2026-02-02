# 2.4.x helper
def get_cat_frame_and_cols(where: str = "2.4.x"):
    """
    Return (frame, cat_cols_filtered) for 2.4.x audits.

    * Prefer df_clean if available, else df
    * Drops meta/non-feature columns
    * Warns about catalog columns not present in the frame
    """
    if "df_clean" in globals():
        frame = df_clean
    else:
        frame = df

    all_cat = list(cat_cols)

    # remove meta/internal cols
    all_cat = [c for c in all_cat if c not in META_NONFEATURE_COLS_24]

    missing = [c for c in all_cat if c not in frame.columns]
    valid   = [c for c in all_cat if c in frame.columns]

    if missing:
        print(f"   ⚠️ {where}: skipping {len(missing)} cat col(s) not in frame:", missing)

    return frame, valid