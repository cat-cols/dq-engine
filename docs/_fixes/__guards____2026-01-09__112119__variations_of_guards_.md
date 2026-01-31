
# Guards
assert "df" in globals(), "❌ df not found. Run Section 2.0 first."
assert "CONFIG" in globals(), "❌ CONFIG not found. Run 2.0.1–2.0.2."
assert "SECTION2_REPORT_PATH" in globals(), "❌ SECTION2_REPORT_PATH missing. Run 2.0.1."
assert "SEC2_REPORTS_DIR" in globals(), "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."
assert "SEC2_ARTIFACTS_DIR" in globals(), "❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first.

Can this be written differently without functions

Yep. You can make it cleaner, avoid repetition, and still stay **no-functions** by using a single `missing` list + one raise. Bonus: it fixes your current snippet’s missing quote/paren on the last assert.

Here are two solid patterns.

### Pattern A: Minimal + readable (single failure message)

```python
required = [
    ("df", "❌ df not found. Run Section 2.0 first."),
    ("CONFIG", "❌ CONFIG not found. Run 2.0.1–2.0.2."),
    ("SECTION2_REPORT_PATH", "❌ SECTION2_REPORT_PATH missing. Run 2.0.1."),
    ("SEC2_REPORTS_DIR", "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."),
    ("SEC2_ARTIFACTS_DIR", "❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first."),
]

missing = [msg for name, msg in required if name not in globals() or globals().get(name) is None]

if missing:
    raise RuntimeError("Section preflight failed:\n" + "\n".join(missing))
```

### Pattern B: One-liner style guards (still no functions)

```python
missing = []
if "df" not in globals() or df is None: missing.append("❌ df not found. Run Section 2.0 first.")
if "CONFIG" not in globals() or CONFIG is None: missing.append("❌ CONFIG not found. Run 2.0.1–2.0.2.")
if "SECTION2_REPORT_PATH" not in globals() or SECTION2_REPORT_PATH is None: missing.append("❌ SECTION2_REPORT_PATH missing. Run 2.0.1.")
if "SEC2_REPORTS_DIR" not in globals() or SEC2_REPORTS_DIR is None: missing.append("❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first.")
if "SEC2_ARTIFACTS_DIR" not in globals() or SEC2_ARTIFACTS_DIR is None: missing.append("❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first.")

if missing:
    raise RuntimeError("Section preflight failed:\n" + "\n".join(missing))
```

If you want this to be *extra* Jupyter-friendly, add a quick “✅ preflight OK” print when it passes—but the core structure above is the cleanest no-functions approach.


># is the assert style I gave you (without functions) a better pattern than the two you gave me

Not really. Your **assert-per-line** style is fine for quick notebooks, but it’s *worse* than the two patterns I gave for anything you’ll iterate on or share.

**Why your assert style loses:**

* **Asserts can be silently disabled.** If Python is run with optimizations (`python -O`), `assert` statements don’t execute. That’s a nasty “it worked on my machine” gremlin.
* **Failure mode is one-at-a-time.** You fix one missing global, rerun, hit the next missing global… death by a thousand reruns.
* **Harder to maintain.** Lots of repeated boilerplate, easy to introduce small syntax mistakes (you already had a missing quote/paren).
* **Less control over error type.** `AssertionError` is less semantically helpful than raising `RuntimeError` / `NameError` with a curated message.

**When your assert style *is* better:**

* You’re prototyping fast, you truly want “fail immediately on the first missing thing,” and you’re never running with `-O`.

**Best “no-functions” pattern for your project:**
Use the **single `missing` list + one raise** (Pattern A). It keeps notebook ergonomics but behaves like real software.

If you insist on assert-style but want it safer, the closest upgrade is: **keep one-at-a-time asserts for invariants**, but switch “required globals” checks to the `missing` list approach. That’s the clean split: asserts for “this should never happen,” `missing + raise` for “this environment might not be initialized yet.”

># Should I pick A or B

Pick **A**.

Use **Pattern A (collect `missing` → raise once)** for “required globals / setup not run yet” checks. It’s more maintainable, gives you *one* clean error with the full list, and it won’t quietly disappear if someone runs Python with `-O` (where `assert` gets stripped).

Keep **B-style asserts** only for true **invariants** inside a section (stuff that *should never be false* once the pipeline is properly initialized).

># Do I only need to do Pattern A once at the top of the notebook?

Not only once—**do it once per “entry point”**.

In a perfect linear, “Run All” world, one Pattern A at the top is enough. In the real Jupyter universe (reruns, partial runs, restarting kernels), you want Pattern A at:

1. **The bootstrap cell** (2.0) — the big “make the world exist” check.
2. **The start of each major section** (2.1, 2.2, 2.3, …) — a *small* check for that section’s required globals/dirs/artifacts.
3. **Any cell that is commonly run standalone** (like 2.1.5 feature grouping) — if it depends on earlier outputs (e.g., `id_cols`, `sec21_reports_dir`, `append_sec2`, etc.), guard it.

Think of Pattern A as your “module import guard” for notebooks.

💡💡 Rule of thumb: **Guard at the top of every section notebook cell that you might run out of order.** That keeps the notebook robust without turning every 10 lines into paranoia.

># # Guards
required = [
    ("df", "❌ df not found. Run Section 2.0 first."),
    ("CONFIG", "❌ CONFIG not found. Run 2.0.1–2.0.2."),
    ("SECTION2_REPORT_PATH", "❌ SECTION2_REPORT_PATH missing. Run 2.0.1."),
    ("SEC2_REPORTS_DIR", "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."),
    ("SEC2_ARTIFACTS_DIR", "❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first."),
]

missing = [msg for name, msg in required if name not in globals() or globals().get(name) is None]

if missing:
    raise RuntimeError("Section preflight failed:\n" + "\n".join(missing))

># is this a guard?

Yep — that’s absolutely a guard. ✅

It’s a **preflight guard** that:

* declares the required globals,
* checks they exist **and** aren’t `None`,
* fails fast with a clean, aggregated error message.

Two tiny upgrades to make it more bulletproof (still no functions):

1. **Also catch “empty df”** (exists-but-useless is a classic notebook trap).
2. **Optionally validate types for path-like globals** (Path/str) so you don’t get weird downstream errors.

Here’s a tightened version staying in your style:

```python
# Guards (no functions)
required = [
    ("df", "❌ df not found. Run Section 2.0 first."),
    ("CONFIG", "❌ CONFIG not found. Run 2.0.1–2.0.2."),
    ("SECTION2_REPORT_PATH", "❌ SECTION2_REPORT_PATH missing. Run 2.0.1."),
    ("SEC2_REPORTS_DIR", "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."),
    ("SEC2_ARTIFACTS_DIR", "❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first."),
]

missing = []
for name, msg in required:
    if name not in globals() or globals().get(name) is None:
        missing.append(msg)

# Extra: df must be non-empty
if "df" in globals() and globals().get("df") is not None:
    try:
        if getattr(df, "empty", False) or df.shape[0] == 0 or df.shape[1] == 0:
            missing.append("❌ df is empty (0 rows or 0 cols). Reload data via Section 2.0.")
    except Exception:
        missing.append("❌ df exists but could not be inspected (unexpected type).")

if missing:
    raise RuntimeError("Section preflight failed:\n" + "\n".join(missing))
```

So yes: what you wrote is a guard; this just makes it a slightly more paranoid (and notebook-realistic) guard.

># So what you just gave me is better? is it the best for notebook-realistic guards?


It’s better **for notebook reality**, yeah — because notebooks fail in *weirder* ways than scripts:

* a name exists but is `None`
* `df` exists but is empty because a read silently returned nothing
* `df` exists but got overwritten (string, dict, whatever) two cells ago

Is it “the best”? It’s *near the sweet spot* of **robust + readable + no-functions**. Past this point, “best” starts to mean “more verbose and stricter,” not necessarily more useful.

If you want the **most notebook-realistic guard** (still no functions) I’d add exactly two things:

1. **Type sanity** (df must be a DataFrame; CONFIG must be dict-like)
2. **Path sanity** (dirs/path variables should be Path-ish or str)

Here’s the “max practical” version that’s still not obnoxious:

```python
# Notebook-realistic guards (no functions)

required = [
    ("df", "❌ df not found. Run Section 2.0 first."),
    ("CONFIG", "❌ CONFIG not found. Run 2.0.1–2.0.2."),
    ("SECTION2_REPORT_PATH", "❌ SECTION2_REPORT_PATH missing. Run 2.0.1."),
    ("SEC2_REPORTS_DIR", "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."),
    ("SEC2_ARTIFACTS_DIR", "❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first."),
]

errors = []

# 1) existence / not-None
for name, msg in required:
    if name not in globals() or globals().get(name) is None:
        errors.append(msg)

# 2) df sanity
if "df" in globals() and globals().get("df") is not None:
    if not isinstance(df, pd.DataFrame):
        errors.append(f"❌ df is not a pandas DataFrame (got {type(df)}).")
    else:
        if df.shape[0] == 0 or df.shape[1] == 0:
            errors.append(f"❌ df is empty, shape={df.shape}. Reload data via Section 2.0.")

# 3) CONFIG sanity
if "CONFIG" in globals() and globals().get("CONFIG") is not None:
    if not isinstance(CONFIG, dict):
        errors.append(f"❌ CONFIG must be a dict (got {type(CONFIG)}).")

# 4) Path-ish sanity (don’t require existence here—some paths get created later)
path_vars = ["SEC2_REPORTS_DIR", "SEC2_ARTIFACTS_DIR", "SECTION2_REPORT_PATH"]
for pv in path_vars:
    if pv in globals() and globals().get(pv) is not None:
        v = globals().get(pv)
        if not isinstance(v, (str, Path)):
            errors.append(f"❌ {pv} must be str or Path (got {type(v)}).")

if errors:
    raise RuntimeError("Section preflight failed:\n" + "\n".join(errors))
```

That’s about as “best” as it gets without turning your notebook into a TSA checkpoint.

💡💡 Practical advice:

* Do **Pattern A once** at the top of the notebook for core globals.
* Then in each section, do a **small local guard** for that section’s special requirements (like `id_cols`, `sec21_reports_dir`, etc.).
  That combo gives you safety *and* keeps cells readable.

># # Guards
required = [
    ("df", "❌ df not found. Run Section 2.0 first."),
    ("CONFIG", "❌ CONFIG not found. Run 2.0.1–2.0.2."),
    ("SECTION2_REPORT_PATH", "❌ SECTION2_REPORT_PATH missing. Run 2.0.1."),
    ("SEC2_REPORTS_DIR", "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."),
    ("SEC2_ARTIFACTS_DIR", "❌ SEC2_ARTIFACTS_DIR missing. Run 2.0.0 first."),
]

missing = [msg for name, msg in required if name not in globals() or globals().get(name) is None]

if missing:
    raise RuntimeError("Section preflight failed:\n" + "\n".join(missing))

># Is this one good enough for what I'm doing or should I upgrade the pattern

Yep — **that’s good enough** for what you’re doing **as long as** your goal is: *“fail fast when the upstream bootstrap didn’t run / globals didn’t get created.”* It’s a clean, notebook-friendly **existence + not-None** gate.

Upgrade only if you’re regularly hitting any of these “notebook gremlins”:

* `df` exists but is **not a DataFrame** (got overwritten)
* `df` exists but is **empty** (bad read, filter nuked rows, etc.)
* `CONFIG` exists but is **not a dict**
* `SEC2_REPORTS_DIR` exists but is **not Path/str**
* paths exist but point somewhere **unexpected** and you want to catch that early

If those haven’t been happening, keep your current guard. It’s perfectly reasonable.

If you *do* want the smallest “upgrade” that buys real safety without getting verbose, add just these two checks:

```python
# After your existing missing-check block

# df sanity (common notebook failure mode)
if not isinstance(df, pd.DataFrame):
    raise TypeError(f"❌ df must be a pandas DataFrame, got {type(df)}")

if df.empty:
    raise ValueError(f"❌ df is empty (shape={df.shape}). Re-run Section 2.0 load.")

# CONFIG sanity
if not isinstance(CONFIG, dict):
    raise TypeError(f"❌ CONFIG must be a dict, got {type(CONFIG)}")
```

That’s the sweet-spot upgrade: **still simple**, catches the most common “it exists but it’s wrong” problems.

💡💡 Rule of thumb:

* Use your current pattern for **infrastructure preflight** (did the bootstrap run?).
* Add the tiny type/empty checks only in sections where a bad `df`/`CONFIG` would waste time or write garbage artifacts.
