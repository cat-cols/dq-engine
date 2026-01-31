# Telco/Level_3/src/telco_churn/utils/dev_tools.py

from importlib import import_module, reload
from types import ModuleType
from typing import Iterable, Optional

def debug_import(module_path: str, attrs: Optional[Iterable[str]] = None) -> ModuleType:
    """
    Quick import debugger.

    - Imports (or reloads) `module_path`
    - Prints the module file path
    - Optionally checks for specific attributes

    Example:
        from telco_churn.utils.dev_tools import debug_import
        rep = debug_import("telco_churn.utils.reporting", ["append_sec2", "log_section_completion"])
    """
    print(f"\n🔍 Importing module: {module_path}")
    mod = import_module(module_path)
    mod = reload(mod)

    print(f"📁 Module file: {getattr(mod, '__file__', '<no __file__>')}")

    if attrs:
        for name in attrs:
            has = hasattr(mod, name)
            print(f"   • has {name!r}? {has}")
    return mod

# no notebooks version
# def debug_import(module_path: str, attrs: Optional[Iterable[str]] = None) -> ModuleType:
#     """
#     Quick import debugger.

#     Example:
#         rep = debug_import("telco_churn.utils.reporting",
#                            ["append_sec2", "log_section_completion"])
#     """
#     print(f"\n🔍 Importing module: {module_path}")
#     mod = import_module(module_path)
#     mod = reload(mod)

#     print(f"📁 Module file: {getattr(mod, '__file__', '<no __file__>')}")

#     if attrs:
#         for name in attrs:
#             has = hasattr(mod, name)
#             print(f"   • has {name!r}? {has}")
#     return mod

# toolkit/module_debug.py

from importlib import reload
import inspect

def debug_module(mod, test_funcs=None):
    """
    Quick helper to:
      - reload a module
      - print where it's loaded from
      - list key attributes
      - optionally execute some test functions
    """
    mod = reload(mod)
    print("✅ Reloaded:", mod.__name__)
    print("   File   :", getattr(mod, "__file__", "<no file>"))

    if test_funcs:
        for name, fn in test_funcs.items():
            try:
                print(f"\n— Running smoke test: {name}()")
                fn()
                print(f"   ✔ {name} ok")
            except Exception as e:
                print(f"   ⚠ {name} failed: {e}")

    return mod

# # Use this part in a notebook or script:
# import telco_churn.utils.reporting as reporting
# from toolkit.module_debug import debug_module  # wherever you store it

# def _test_log_section():
#     reporting.log_section_completion("X.Y.Z", "OK", checked=1, mismatched=0)

# reporting = debug_module(
#     reporting,
#     test_funcs={"log_section_completion": _test_log_section},
# )
