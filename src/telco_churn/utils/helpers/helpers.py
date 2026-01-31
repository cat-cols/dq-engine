# DEFINE HELPERS
# Help find a file in multiple directories
    # Why:
    # Many later sections will need “search these known roots for a filename.”
    # Centralizing prevents copy paste drift.
    # Naming:
    # If you intend other modules to use it, drop the underscore: find_file_in_dirs.
    # If it is internal notebook glue only, keep _find_file_in_dirs.
    # Also make it consistent with your project roots.

# Helper: find file in candidate dirs
def find_file_in_dirs(fname, dirs):
    for d in dirs:
        p = Path(d) / fname
        if p.exists():
            return p
    p = Path.cwd() / fname
    return p if p.exists() else None

# Helper: find file in candidate dirs
if "_find_file_in_dirs" not in globals():
    def _find_file_in_dirs(fname, dirs):
        for d in dirs:
            if d is None:
                continue
            p = Path(d) / fname
            if p.exists():
                return p
        p = Path.cwd() / fname
        if p.exists():
            return p
        return None

# def _find_file_in_dirs(fname, dirs):
#     """Return first existing Path for fname in given dirs, else None."""
#     for d in dirs:
#         if d is None:
#             continue
#         p = Path(d) / fname
#         if p.exists():
#             return p
#     # also check CWD as absolute fallback
#     p = Path.cwd() / fname
#     if p.exists():
#         return p
#     return None


# def _find_file_in_dirs(fname, dirs):
#     """Return first existing Path for fname in given dirs, else None."""
#     for d in dirs:
#         if d is None:
#             continue
#         p = Path(d) / fname
#         if p.exists():
#             return p
#     p = Path.cwd() / fname
#     if p.exists():
#         return p
#     return None

# helper: Benjamini–Hochberg
def bh_fdr(pvals: np.ndarray):
    n = len(pvals)
    if n == 0:
        return np.array([], dtype=float)
    order = np.argsort(pvals)
    ranked = np.arange(1, n + 1)
    adj = pvals.copy().astype(float)
    adj[order] = pvals[order] * n / ranked
    # enforce monotone decreasing from largest rank
    adj[order] = np.minimum.accumulate(adj[order][::-1])[::-1]
    return np.clip(adj, 0.0, 1.0)

# helper: Benjamini–Yekutieli
def by_fdr(pvals: np.ndarray):
    n = len(pvals)
    if n == 0:
        return np.array([], dtype=float)
    # harmonic series factor
    c_n = np.sum(1.0 / np.arange(1, n + 1))
    order = np.argsort(pvals)
    ranked = np.arange(1, n + 1)
    adj = pvals.copy().astype(float)
    adj[order] = pvals[order] * n * c_n / ranked
    adj[order] = np.minimum.accumulate(adj[order][::-1])[::-1]
    return np.clip(adj, 0.0, 1.0)

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
