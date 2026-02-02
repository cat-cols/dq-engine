# src/telco_churn/utils/guards.py

def require_globals(globs, required, section_label: str = ""):
    """
    Ensure required names exist in the given globals() mapping.

    Parameters
    ----------
    globs:
        Usually call with `globals()` from the notebook.
    required:
        Iterable of variable names that must be present in globs.
    section_label:
        Optional label like "2.1.11" for nicer error messages.

    Function behavior: require_globals(globs, required, section_label="") (guards.py)

    Purpose
    - Safety “guard” that enforces run order and prerequisites by ensuring required names exist
    before a section/cell continues.

    What it does
    - Accepts a globals mapping (usually call with `globals()` from the notebook).
    - Accepts an iterable of required variable names (strings).
    - Computes which names are missing:
        missing = [name for name in required if name not in globs]
    - If anything is missing, raises a RuntimeError with a clear, section-tagged message indicating
    which variables are absent and suggesting the earlier bootstrap cells be run first.

    Why it’s useful
    - Fails fast and loudly when the notebook is in a bad state (kernel restart, out-of-order execution,
    partial runs, or accidental overwrites).
    - Produces cleaner errors than downstream NameError/KeyError cascades.
    - Documents dependencies for each section by listing required names explicitly.

    What it does NOT do
    - It does not create or “fix” missing variables. It only checks and raises if the environment
    is incomplete.
    """

    missing = [name for name in required if name not in globs]
    if missing:
        sec = f"[{section_label}] " if section_label else ""
        missing_str = ", ".join(missing)
        raise RuntimeError(
            f"❌ {sec}Missing required globals: {missing_str}. "
            "Run the earlier Section 2 bootstrap cells first."
        )
