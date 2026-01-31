# Pattern 02 – Dtype bucketing (pandas → semantic groups)

**Context:** Telco Section 2 (Data Quality).  
**Goal:** Bucket `df[col].dtype` into semantic groups for reporting and checks.

## v1 – Inline loop per section

Used in early 2.0.x cells, duplicated in 2.0.4 and 2.0.6.

```python
type_groups = []
for col in df.columns:
    dtype_str = str(df[col].dtype)
    s = dtype_str.lower()
    if ("int" in s) or ("float" in s):
        type_group = "numeric"
    elif "bool" in s:
        type_group = "boolean"
    elif ("datetime" in s) or ("date" in s):
        type_group = "datetime"
    elif "category" in s:
        type_group = "categorical"
    else:
        type_group = "string_like"

    type_groups.append(type_group)



#########

Short answer: **keep only v2 in your production library**, and document v1 vs v2 in **docs/snippets**, not inline in the core code.

Here’s a concrete way to do it that fits your Telco/Level vibe.

---

## 1. In the actual code library: only v2, clearly labeled

In your `telco_churn/dq/types.py` (or similar), just keep the helper-based pattern and document the intent + provenance:

```python
# telco_churn/dq/types.py

def classify_dtype(dtype_str: str) -> str:
    """
    Telco DQ pattern: map pandas dtype → semantic type_group.

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
```

And the call site in 02_DQ just becomes:

```python
from telco_churn.dq.types import classify_dtype

type_groups = []
for col in df.columns:
    dtype_str = str(df[col].dtype)
    type_groups.append(classify_dtype(dtype_str))
```

💡💡 *Learning / library tip:* Always expose the *helper-based v2* at the library boundary, but mention in the docstring that it’s the evolution of an inline v1. That’s enough breadcrumb for future-you without cluttering the code.

---

## 2. In a “patterns” doc: show **v1 vs v2** side-by-side

Instead of keeping both in the code, capture the evolution in a Markdown doc like:

`docs/patterns/02_dtype_bucketing.md`:

````markdown
# Pattern 02 – Dtype bucketing (pandas → semantic groups)

**Context:** Telco Section 2 (Data Quality).  
**Goal:** Bucket `df[col].dtype` into semantic groups for reporting and checks.

## v1 – Inline loop per section

Used in early 2.0.x cells, duplicated in 2.0.4 and 2.0.6.

```python
type_groups = []
for col in df.columns:
    dtype_str = str(df[col].dtype)
    s = dtype_str.lower()
    if ("int" in s) or ("float" in s):
        type_group = "numeric"
    elif "bool" in s:
        type_group = "boolean"
    elif ("datetime" in s) or ("date" in s):
        type_group = "datetime"
    elif "category" in s:
        type_group = "categorical"
    else:
        type_group = "string_like"

    type_groups.append(type_group)
````

**Pros:**

* Extremely explicit; easy for a reader to follow.
* Nice for teaching notebooks.

**Cons:**

* Copy-pasted in multiple sections.
* Harder to unit test and keep in sync.

---

## v2 – Helper-based, DRY

Refactored into a reusable helper in the Telco library.

```python
def classify_dtype(dtype_str: str) -> str:
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

type_groups = []
for col in df.columns:
    dtype_str = str(df[col].dtype)
    type_groups.append(classify_dtype(dtype_str))
```

**Pros:**

* Single source of truth for the mapping.
* Reused across 2.0.4, 2.0.5, 2.0.6.
* Easy to unit test (`test_classify_dtype.py`).

**Cons:**

* Slightly less “inline readable” if you’re brand-new to the pattern.

---

## When to use which

* **Teaching / exploratory notebooks (Level_1 / early Level_2):** it’s fine to show the v1 inline once to introduce the concept.
* **Telco project core (Level_3+ / Stage-D):** always use **v2** from the library and reference this doc if you want to talk about the evolution.

````

💡💡 *Learning / portfolio tip:* This kind of “Pattern card” is gold for recruiters: it shows you can (1) design a pattern, (2) recognize duplication, (3) refactor to a helper, and (4) document trade-offs.

---

## 3. Optional: a tiny “pattern index” in your repo

At the top of `docs/patterns/README.md`:

```markdown
# Telco Churn Pattern Library

This directory records reusable patterns used across the Telco project.

- 02 – Dtype bucketing (pandas → semantic groups)
  - v1: inline per-section loop (02_DQ notebook, early prototype)
  - v2: `telco_churn.dq.types.classify_dtype` helper (current standard)
````

You can then point to this in your main project README as “Pattern Library (how I think about refactors).”

---

## 4. What to do **inside** 02_DQ.ipynb

Inside the notebook, I’d keep it minimal:

```python
# 2.0.x helper: dtype → semantic type_group
# Pattern 02 – Dtype bucketing (see docs/patterns/02_dtype_bucketing.md)
from telco_churn.dq.types import classify_dtype
```

No giant v1 block in comments — that lives in `docs/patterns`. Cleaner code, but your learning trail is still preserved.

---

If you want, I can draft a full `docs/patterns/02_dtype_bucketing.md` with your Level_2/Level_3 language and little 🎯/⚠️ badges baked in so you can just drop it into the repo.
