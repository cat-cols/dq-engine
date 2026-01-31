# dtype utils
def _norm_dtype(x):
    if x is None:
        return None
    s = str(x)
    return _dtype_alias.get(s, s)