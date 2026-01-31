># Q: AttributeError: partially initialized module 'pandas' has no attribute 'core' (most likely due to a circular import)

```python
# PART 1) imports

from pathlib import Path
from types import MappingProxyType
from datetime import datetime, timezone

import json
import yaml
import pandas as pd
import os
import subprocess
import itertools
import hashlib
import sys
import platform
import numpy as np
import math
import warnings
import textwrap
import shutil
from pandas.errors import EmptyDataError
from pandas.api.types import is_numeric_dtype, is_bool_dtype

# Jupyter/CLI-safe display helper (no new function definition)
try:
    from IPython.display import display
except Exception:
    display = print  #💡 Fallback in pure Python/CLI → alias display → print

# --- Optional libs (enable features; do NOT crash notebook unless truly required)
HAS_SCIPY = False
HAS_MPL   = False
HAS_SM    = False

stats = None
plt   = None
sm    = None
smf   = None
variance_inflation_factor = None

# SciPy (optional unless you decide it is required)
try:
    from scipy import stats as _stats
    stats = _stats
    HAS_SCIPY = True
except Exception:
    pass

# try:
#     from scipy import stats
# except ImportError as e:
#     raise ImportError("❌ SciPy is required for Section 2.7 Part B (correlation / ANOVA / chi-square / point-biserial).") from e

# Matplotlib (optional)
try:
    import matplotlib.pyplot as _plt
    plt = _plt
    HAS_MPL = True
except Exception:
    pass

# # Matplotlib for correlation heatmap
# try:
#     import matplotlib.pyplot as plt
# except ImportError as e:
#     print("   ⚠️ matplotlib not available; 2.7.4 heatmap will be skipped.")
#     plt = None

# Statsmodels (optional OR required depending on your policy)
try:
    import statsmodels.api as _sm
    import statsmodels.formula.api as _smf
    from statsmodels.stats.outliers_influence import variance_inflation_factor as _vif
    sm = _sm
    smf = _smf
    variance_inflation_factor = _vif
    HAS_SM = True
except Exception:
    pass

print(
    "✅ Optional deps:",
    f"SciPy={'ON' if HAS_SCIPY else 'OFF'} |",
    f"Matplotlib={'ON' if HAS_MPL else 'OFF'} |",
    f"Statsmodels={'ON' if HAS_SM else 'OFF'}"
)

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[10], line 9
      7 import json
      8 import yaml
----> 9 import pandas as pd
     10 import os
     11 import subprocess

File ~/DATA/PROJECTS/Telco/.venv/lib/python3.12/site-packages/pandas/__init__.py:139
    121 from pandas.core.reshape.api import (
    122     concat,
    123     lreshape,
   (...)    135     qcut,
    136 )
    138 from pandas import api, arrays, errors, io, plotting, tseries
--> 139 from pandas import testing
    140 from pandas.util._print_versions import show_versions
    142 from pandas.io.api import (
    143     # excel
    144     ExcelFile,
   (...)    172     read_spss,
    173 )

File ~/DATA/PROJECTS/Telco/.venv/lib/python3.12/site-packages/pandas/testing.py:6
      1 """
      2 Public testing utility functions.
      3 """
----> 6 from pandas._testing import (
      7     assert_extension_array_equal,
      8     assert_frame_equal,
      9     assert_index_equal,
     10     assert_series_equal,
     11 )
     13 __all__ = [
     14     "assert_extension_array_equal",
     15     "assert_frame_equal",
     16     "assert_series_equal",
     17     "assert_index_equal",
     18 ]

File ~/DATA/PROJECTS/Telco/.venv/lib/python3.12/site-packages/pandas/_testing/__init__.py:405
    400     import pytest
    402     return pytest.raises(expected_exception, match=None)
--> 405 cython_table = pd.core.common._cython_table.items()
    408 def get_cython_table_params(ndframe, func_names_and_expected):
    409     """
    410     Combine frame, functions from com._cython_table
    411     keys and expected result.
   (...)    423         List of three items (DataFrame, function, expected result)
    424     """

>AttributeError: partially initialized module 'pandas' has no attribute 'core' (most likely due to a circular import)
```

That exact error almost always comes from **a name collision** (something in your project is shadowing the real `pandas` package), or a **corrupted pandas install** in the venv.

## 1) First: check for shadowing (most common)

From your project root (same folder you run Jupyter from), run:

```bash
# show anything that could shadow pandas
ls -la | egrep '^d|^-'
find . -maxdepth 3 -type f -name "pandas.py" -o -type d -name "pandas"
```

If you see **`pandas.py`** or a **`pandas/` folder** anywhere in your repo (especially near the notebook), rename it (e.g., `pandas_utils.py`) and delete caches:

```bash
find . -type d -name "__pycache__" -prune -exec rm -rf {} +
```

Then restart the Jupyter kernel and try `import pandas as pd` again.

## 2) Check where Python *thinks* pandas is (without importing it)

This works even when import is broken:

```bash
python -c "import importlib.util as u; s=u.find_spec('pandas'); print(s); print('origin=', getattr(s,'origin',None)); print('locs=', getattr(s,'submodule_search_locations',None))"
```

* If `origin` points to **your repo** (not `.venv/.../site-packages/...`) → you’re shadowing pandas.

## 3) If no shadowing: reinstall pandas (second most common)

Inside your venv:

```bash
python -m pip uninstall -y pandas
python -m pip install --no-cache-dir -U "pandas>=2.2" numpy
python -m pip check
```

Then restart kernel.

## 4) Jupyter gotcha: kernel using the wrong interpreter

In a notebook cell, run:

```python
import sys
print(sys.executable)
```

Make sure it points to:
`.../Telco/.venv/bin/python`

If you paste the outputs of:

* `find . -maxdepth 3 -name "pandas.py" -o -name "pandas"`
* the `find_spec('pandas')` command output
* `print(sys.executable)`

…I can tell you which of the two (shadowing vs reinstall) is the real cause in your setup.
