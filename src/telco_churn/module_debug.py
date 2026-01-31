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


# In a notebook or script:
import telco_churn.utils.reporting as reporting
from toolkit.module_debug import debug_module  # wherever you store it

def _test_log_section():
    reporting.log_section_completion("X.Y.Z", "OK", checked=1, mismatched=0)

reporting = debug_module(
    reporting,
    test_funcs={"log_section_completion": _test_log_section},
)
