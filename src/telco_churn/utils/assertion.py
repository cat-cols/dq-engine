# Short answer:
# You **don’t** need a separate function for every single `assert`, but it *is* worth pulling repeated patterns into a few small helpers. The goal isn’t “fewer lines at all costs” — it’s **less copy-paste with *more* clarity.**

# Let’s talk trade-offs and then I’ll show you a pattern that fits your Section-2 vibe.

# ---

# ## When to keep asserts inline

# Inline `assert`s are fine when:

# * The check is **one-off** and self-explanatory:

# ```python
# assert "df_clean" in globals(), "❌ df_clean not found; run 2.9 first."
# assert df_clean.shape[0] > 0, "❌ df_clean is empty."
# ```

# These are good because:

# * You see the precondition right where the cell’s logic starts.
# * There’s no indirection — you don’t have to jump to another function to understand it.

# If a check happens **in only one place**, or only twice with small variation, keep it inline.

# ---

# ## When repetition means “make a helper”

# Where it starts to hurt:

# * You’re repeating the *same structure* in lots of cells:

# ```python
# assert "df_clean" in globals(), "❌ df_clean not found."
# assert "df_before_clean" in globals(), "❌ df_before_clean not found."
# missing = [c for c in needed_cols if c not in df_clean.columns]
# assert not missing, f"❌ Missing columns: {missing}"
# ```

# …and this same chunk appears in 5–10 places, slightly modified each time.

# That’s a classic “factor this out” signal.

# ### 💡💡 Pattern: tiny precondition helpers

# At the **top of the notebook** (or in a shared utils file), define:

# ```python
# def require_globals(names, where="this step"):
#     missing = [name for name in names if name not in globals()]
#     if missing:
#         raise RuntimeError(f"❌ Missing globals for {where}: {missing}")

# def require_columns(df, cols, df_name="df", where="this step"):
#     missing = [c for c in cols if c not in df.columns]
#     if missing:
#         raise RuntimeError(
#             f"❌ {df_name} missing columns for {where}: {missing}"
#         )
# ```

# Then each cell becomes:

# ```python
# # 2.10A preconditions
# require_globals(["df_clean"], where="2.10A — univariate overview")
# require_columns(df_clean, ["MonthlyCharges", "tenure"], df_name="df_clean",
#                 where="2.10A — fair price & residual")
# ```

# Benefits:

# * You only write the error formatting once.
# * Errors are consistent, with section labels.
# * Each cell’s “preconditions” block stays super readable.

# ---

# ## Don’t overdo the abstraction

# What I would *not* do:

# * A **separate function per `assert`**, like:

# ```python
# def assert_df_clean_exists(): ...
# def assert_df_before_exists(): ...
# def assert_monthly_charges_column(): ...
# ```

# That explodes the number of little functions and makes it harder to see what a cell needs. A few *generic* helpers are better than dozens of hyper-specific ones.

# Good rule of thumb:

# > If you can express the variation with parameters, keep it **one helper**, not many.

# ---

# ## A structure that fits your pipeline

# Here’s a concrete layout that I think will feel good in your Section-2 notebooks:

# ### 1. One “safety helpers” cell near the top

# ```python
# # 2.0.x — Safety helpers

# def require_globals(names, where):
#     missing = [n for n in names if n not in globals()]
#     if missing:
#         raise RuntimeError(f"❌ Missing globals in {where}: {missing}")

# def require_df(name, where):
#     if name not in globals():
#         raise RuntimeError(f"❌ {name} not found in globals() for {where}")
#     df = globals()[name]
#     if getattr(df, "empty", False):
#         raise RuntimeError(f"❌ {name} is empty in {where}")
#     return df

# def require_columns(df, cols, df_name, where):
#     missing = [c for c in cols if c not in df.columns]
#     if missing:
#         raise RuntimeError(
#             f"❌ {df_name} missing columns in {where}: {missing}"
#         )
# ```

# ### 2. Each section cell uses those in 2–3 lines max

# ```python
# print("\n2.9.8 🧮 Distribution drift verification")

# df_clean = require_df("df_clean", where="2.9.8 — drift check")
# require_columns(df_clean,
#                 ["MonthlyCharges", "tenure"],
#                 df_name="df_clean",
#                 where="2.9.8 — drift check")

# # ... core logic continues ...
# ```

# Now you’ve got:

# * Very little repetition.
# * Very *readable* intent at the top of each cell.
# * One place to tweak behavior (e.g., change how errors are formatted, or log instead of raise).

# ---

# ## How this relates to “minimize lines of code”

# You asked earlier if it should be a goal to use as few lines as possible. Here’s the practical heuristic:

# * **Primary goals:** clarity, correctness, and easy changes.
# * **Secondary goal:** less duplication.
# * **Lines of code** only really matter when:

#   * Duplication makes changes painful,
#   * Or noise makes it hard to see the real work.

# So: **don’t chase fewer lines**; chase fewer *repeated concepts* and clearer preconditions.

# ---

# If you want, you can paste a sample of one of your cells with a bunch of repeated asserts, and I can refactor it into this helper style so you can just copy-paste it into your notebook.
