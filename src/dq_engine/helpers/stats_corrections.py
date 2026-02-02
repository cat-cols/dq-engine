#
import numpy as np

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