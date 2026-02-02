# telco_churn/dq/types.py

def classify_dtype(dtype_str: str) -> str:
    """
    Telco DQ pattern: map pandas dtype → semantic type_group.

    Map pandas dtype string to a semantic type group.
    See docs/patterns/02_dtype_bucketing.md for v1 vs v2 history.

    This is the *v2 (helper-based, DRY)* version of the dtype bucketing pattern
    originally written inline in Section 2 (v1).

    Used by:
        - 2.0.4 Dataset snapshot
        - 2.0.5 Baseline summary
        - 2.0.6 ID/protected column checks

    Parameters
    ----------
    dtype_str : str
        String representation of a pandas dtype (e.g. 'int64', 'float64', 'object').

    Returns
    -------
    str
        One of {'numeric', 'boolean', 'datetime', 'categorical', 'string_like'}.
    """
    s = dtype_str.lower()
    if "int" in s or "float" in s:
        return "numeric"
    if "bool" in s:
        return "boolean"
    if "datetime" in s or "date" in s:
        return "datetime"
    if "category" in s:
        return "categorical"
    return "string_like"

# - the call site in 02_DQ just becomes:
from telco_churn.dq.types import classify_dtype

type_groups = []
for col in df.columns:
    dtype_str = str(df[col].dtype)
    type_groups.append(classify_dtype(dtype_str))

# library tip:
# Always expose the helper-based v2 at the library boundary,
# but mention in the docstring that it’s the evolution of an inline v1.
# That’s enough breadcrumb for future-you without cluttering the code.
