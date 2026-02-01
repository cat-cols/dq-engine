# helpers/config.py

def ensure_config(default: dict = None, label: str = "") -> dict:
    """
    Ensures CONFIG exists in globals(). If not, sets it to a default.

    Args:
        default (dict): Default config to use if CONFIG not present.
        label (str): Optional section label for logging context.

    Returns:
        CONFIG (dict)
    """
    if default is None:
        default = {}

    if "CONFIG" not in globals():
        prefix = f"   ⚠️ {label}:" if label else "   ⚠️"
        print(f"{prefix} CONFIG not found in globals(); using internal defaults.")
        globals()["CONFIG"] = default

    return globals()["CONFIG"]

# -----------------------------
# Global helpers
# -----------------------------
# def ensure_global(name: str, default, *, label: str = ""):
#     """
#     Ensure a global variable exists; if missing, install a default.

#     Notebook-safe: mutates globals() intentionally.

#     Args:
#         name: variable name (e.g. "CONFIG")
#         default: default value if missing
#         label: optional section label for logging

#     Returns:
#         The ensured global value
#     """
#     if name not in globals():
#         prefix = f"   ⚠️ {label}:" if label else "   ⚠️"
#         print(f"{prefix} {name} not found in globals(); using internal defaults.")
#         globals()[name] = default
#     return globals()[name]

def ensure_globals(required: dict, label: str = "") -> dict:
    """
    Ensure required global variables exist.

    Parameters:
    ----------
    required : dict
        Mapping of global variable name → default value.
        Example: { "CONFIG": {}, "RUN_TS": None }

    label : str
        Optional label to prefix warnings (e.g., "2.3")

    Returns:
    -------
    dict
        Mapping of varname → final (possibly default) value
    """
    results = {}
    for name, default in required.items():
        if name not in globals():
            if label:
                print(f"   ⚠️ {label}: {name} not found in globals(); using default.")
            else:
                print(f"   ⚠️ {name} not found in globals(); using default.")
            globals()[name] = default
        results[name] = globals()[name]
    return results

