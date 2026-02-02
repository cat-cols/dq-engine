# DEFINE HELPERS
# Help find a file in multiple directories
    # Why:
    # Many later sections will need “search these known roots for a filename.”
    # Centralizing prevents copy paste drift.
    # Naming:
    # If you intend other modules to use it, drop the underscore: find_file_in_dirs.
    # If it is internal notebook glue only, keep _find_file_in_dirs.
    # Also make it consistent with your project roots.

from pathlib import Path

# find file in candidate dirs
def find_file_in_dirs(fname, dirs):
    """
    Search for a file `fname` in a list of directories `dirs`.
    Returns the first Path where the file exists, or None if not found.
    """
    for d in dirs:
        p = Path(d) / fname
        if p.exists():
            return p
    p = Path.cwd() / fname
    return p if p.exists() else None

# scripts/check_paths.py
from pathlib import Path
for p in ["data/raw","data/processed","outputs/figures","outputs/reports","models"]:
    abs_p = Path(p).resolve()
    print(f"{abs_p} :: {'✓' if abs_p.exists() else '✗'}")


##################################################
# 🧰 PHASE 0) Bring in setup (dev) with robust fallbacks
from pathlib import Path

# -- Adjust only if you move the notebooks directory --
SETUP_IPYNB = Path("/Users/b/DATA/PROJECTS/Telco/Level_3/notebooks/00_Setup.ipynb")
SETUP_PY    = SETUP_IPYNB.with_suffix(".py")  # optional: if you export a .py

def inline_fallback():
    """Minimal, portfolio-safe setup so EDA always runs."""
    global PROJECT_ROOT, DATA_ROOT, DATA_RAW_DIR, DATA_PROCESSED_DIR
    global RAW_FILENAME, CLEAN_FILENAME, RAW_PATH, CLEAN_PATH

    # Find repo root named "Telco"
    cur = Path.cwd().resolve()
    for parent in [cur] + list(cur.parents):
        if parent.name == "Telco":
            PROJECT_ROOT = parent
            break
    else:
        raise FileNotFoundError("❌ 'Telco' repo root not found.")

    DATA_ROOT = PROJECT_ROOT / "resources" / "data"
    DATA_RAW_DIR = DATA_ROOT / "raw"
    DATA_PROCESSED_DIR = DATA_ROOT / "processed"

    RAW_FILENAME = "telco_customer_churn.csv"
    CLEAN_FILENAME = "telco_clean.csv"
    RAW_PATH = DATA_RAW_DIR / RAW_FILENAME
    CLEAN_PATH = DATA_PROCESSED_DIR / CLEAN_FILENAME

try:
    if not SETUP_IPYNB.exists() or SETUP_IPYNB.stat().st_size < 200:
        # If file missing or suspiciously small, skip trying to run it
        raise ValueError(f"Setup notebook missing or invalid (exists={SETUP_IPYNB.exists()}, size={SETUP_IPYNB.stat().st_size if SETUP_IPYNB.exists() else 'NA'})")

    # Run the notebook, injecting its variables into this namespace
    # (quotes are important when path has spaces)
    get_ipython().run_line_magic("run", f'-i "{SETUP_IPYNB}"')
    print(f"✅ Loaded environment via {SETUP_IPYNB}")
except Exception as e_nb:
    print(f"⚠️ Could not %run {SETUP_IPYNB.name} ({e_nb}). Trying {SETUP_PY.name} …")
    try:
        if SETUP_PY.exists():
            get_ipython().run_line_magic("run", f'-i "{SETUP_PY}"')
            print(f"✅ Loaded environment via {SETUP_PY}")
        else:
            raise FileNotFoundError(f"{SETUP_PY} not found")
    except Exception as e_py:
        print(f"⚠️ Could not %run {SETUP_PY.name} either ({e_py}). Falling back inline.")
        inline_fallback()
        print("✅ Environment initialized via inline fallback.")
