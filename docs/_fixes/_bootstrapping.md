Yes — **move blocks 1 and the “core” of 2 into your centralized Section 2 bootstrap**, and keep **2.5.15** mostly as **blocks 3–6** (plus a tiny “ensure bootstrap ran” precondition).

### What goes where

#### ✅ Centralized (bootstrap / shared helpers)

**Block 1** (all directory + `SECTION2_REPORT_PATH` resolution)
**Block 2 (shared part)** = “load Section 2 summary safely” as a reusable helper (or a cached global)

Reason: every section eventually wants the same *single source of truth* for:

* where artifacts live (`SEC2_REPORTS_DIR`)
* where the unified summary lives (`SECTION2_REPORT_PATH`)
* how we read it (robust read, consistent dtypes)

#### ✅ Keep in 2.5.15

* The *filter* `2.5.*` rows (that part is specific to 2.5.15)
* Blocks **3–6**: manifest creation, persistence, summary row, console UX

---

## Minimal 2.5.15 shape (what it should look like)

Replace blocks 1–2 with something like this:

```python
# 0) Preconditions: bootstrap + append helper
if "_bootstrap_section2_paths" in globals() and callable(_bootstrap_section2_paths):
    _bootstrap_section2_paths()
else:
    raise RuntimeError("❌ Run Section 2 bootstrap first (missing _bootstrap_section2_paths).")

if "append_sec2" not in globals() or not callable(append_sec2):
    raise RuntimeError("❌ append_sec2 not available. Define it in bootstrap/shared helpers.")

section2_reports_dir_2515 = SEC2_REPORTS_DIR  # single source of truth
```

Then keep your existing logic, but reading the summary via a shared loader (see next section).

---

## 💡💡 Strong recommendation: centralize “read section2 summary” too

Create **one** helper near bootstrap:

```python
def load_sec2_summary(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"⚠️ Could not read Section 2 summary at {path}: {e}")
        return pd.DataFrame()
```

Then 2.5.15 becomes:

```python
sec2_summary_df_2515 = load_sec2_summary(SECTION2_REPORT_PATH)

if not sec2_summary_df_2515.empty and "section" in sec2_summary_df_2515.columns:
    sec25_df_2515 = sec2_summary_df_2515[
        sec2_summary_df_2515["section"].astype("string").str.startswith("2.5.")
    ].copy()
else:
    sec25_df_2515 = pd.DataFrame()
```

---

## One more tiny fix (important)

Right now you do:

```python
if "SECTION2_REPORT_PATH" not in globals():
    SECTION2_REPORT_PATH = ...
```

That’s exactly the kind of thing that causes “why is it writing somewhere else?” later.
Centralize it, set it once, and everywhere else **only reads it**.

---

### Bottom line

✅ **Yes:** move blocks **1 + shared read logic from 2** into the central bootstrap/shared area.
✅ **Yes:** keep **3–6** in 2.5.15 (plus a short precondition).

If you paste your current `_bootstrap_section2_paths()` and whether you want the summary CSV to live in:

* `resources/reports/section2_summary.csv` (top-level), or
* `resources/reports/section2/section2_summary.csv` (inside the section folder)

…I’ll rewrite the bootstrap so it becomes the one authoritative place and your 2.5.15 cell shrinks cleanly.

---
---

># 2.5.12:

Move only the **reusable wiring** into bootstrap/earlier cells; keep the **2.5.12-specific computation + writes** in 2.5.12.

### Move out of 2.5.12 (into bootstrap / shared helpers)

**A) Path + directory resolution (Block 1)**

* `section2_reports_dir_2512 = section2_reports_dir_25D`
* `anomaly_path_2512 = .../logic_anomaly_context.parquet`

What to do instead in 2.5.12:

* rely on one authoritative `SEC2_REPORTS_DIR` (or a `LOGIC_DIR`) and build paths from it
* or define a single “2.5 reports dir” once (e.g., `section2_reports_dir_25D`) in a shared 2.5 setup cell

**B) Config resolution for scoring (Block 3)**
This is classic “shared config parsing” and will repeat in 2.5.13–2.5.15.

Move into a helper like:

* `get_anomaly_score_config(CONFIG)` → returns weights, defaults, cap (normalized + validated)

💡💡 bonus: you can unit-test this helper easily.

**C) Type-weight mapping function**
`_map_type_weight_inline_2512` should become a reusable helper (or replaced with a map + `fillna(default)` pattern).

**D) Severity rank mapping**
`sev_rank_2512 = {"info":0,...}` belongs in shared constants (used anywhere you need max severity).

**E) Safe “load parquet if exists” utility (Block 2 pattern)**
Not strictly required, but it’s a nice shared helper because you keep doing this everywhere:

* `safe_read_parquet(path) -> df`
* prints consistent messages, returns empty df on failure

---

### Keep in 2.5.12 (don’t move)

**Block 4: Compute per-row scores**
This is the actual “2.5.12 work product.” Keep it local.

**Block 5: Persist `row_anomaly_scores.*`**
These filenames + formats are specific to this section.

**Block 6: Summary row + append_sec2**
Section-specific reporting should stay.

**Block 7: Console UX / display**
Keep.

---

## The “ideal” 2.5.12 after refactor (shape)

At the top of 2.5.12, you want something like:

```python
_bootstrap_section2_paths()          # sets SEC2_REPORTS_DIR, SECTION2_REPORT_PATH, etc.
_bootstrap_logic_paths_if_any()      # sets section2_reports_dir_25D or LOGIC_DIR (optional)

cfg = get_anomaly_score_config(CONFIG)   # shared parsing/validation
anomaly_df = safe_read_parquet(anomaly_context_path)  # shared loader
# ... compute + write + append summary ...
```

---

## 💡💡 One extra move I’d do

Create a single **“2.5 shared setup”** cell that runs once before 2.5.11–2.5.15, which defines:

* `section2_reports_dir_25D` (or better: `SEC2_LOGIC_DIR`)
* common artifact paths:

  * `logic_anomaly_context.parquet`
  * `row_anomaly_scores.parquet/csv`
  * `logic_violation_edges.csv`
* common config getters:

  * `get_anomaly_score_config()`

That keeps bootstrap generic (“Section 2 overall”), and keeps “2.5 logic layer” wiring grouped.

---

If you paste your current `_bootstrap_section2_paths()` and how you define `section2_reports_dir_25D`, I’ll rewrite them into:

1. a clean **global Section 2 bootstrap**
2. a clean **2.5 shared setup**
   …and then show the shortened 2.5.12 header that uses them.


># Q: How many different styles are going on there? Should I resolve it to one style/ pattern? Help me untangle this mess by describing each style in order of section they belong to. Is there one style that is supreme to the others?

You’ve basically got **~8 distinct “directory resolution styles”** mixed together, plus a bunch of near-duplicates of the same style.

Yes: you should **converge to one dominant pattern** (with a couple intentional “special-case” variants), because right now you’re paying a big tax in confusion, bugs, and accidental divergence.

## The styles you currently have (grouped in order of the Section 2 flow)

### 1) **Hard-guard “bootstrap must have run” style** (2.0.x → used again in 2.4.x / some 2.5.x)

**Pattern:** assert/raise if `SEC2_REPORTS_DIR` and/or `SECTION2_REPORT_PATH` missing; then reuse them.

* Example vibe:

  * `assert "SEC2_REPORTS_DIR" in globals()`
  * `section2_reports_dir_24D = SEC2_REPORTS_DIR`
* Strength: **most reliable** when you truly require a prior bootstrap.
* Weakness: not notebook-friendly if you want cells to be runnable standalone.

✅ Belongs to: **2.0.x as the canonical initialization**, and any later section that *must* depend on it.

---

### 2) **Global shared base dir resolver with fallback chain** (2.0-ish / repeated everywhere)

**Pattern:** `sec2_reports_dir = ...` via globals/REPORTS_DIR/PROJECT_ROOT/fallback.

* Example vibe:

  * `if "sec2_reports_dir" in globals(): ...`
  * `elif "REPORTS_DIR" in globals(): ...`
  * `elif "PROJECT_ROOT" in globals(): ...`
  * `else: Path("resources/reports/section2")`
* Strength: good “run anywhere” flexibility.
* Weakness: this is **the #1 source of duplication**, because you repeat it in every section with minor name changes.

✅ Belongs to: **bootstrap cell only**, then everything else should reuse the global(s).

---

### 3) **Duplicate “ensure SECTION2_REPORT_PATH exists” resolver** (2.0.x / repeated everywhere)

**Pattern:** if not set, derive it from REPORTS_DIR / PROJECT_ROOT / fallback.

* Strength: fine as part of bootstrap.
* Weakness: repeated 20+ times; sometimes uses `sec2_reports_dir.parent`, sometimes absolute `resources/reports`.

✅ Belongs to: **bootstrap only**.

---

### 4) **“Specialized subdir builders”** (2.4 categorical, 2.9 quality, 2.10 figures, 2.11 interactions, 2.27/2.28 subfolders)

**Pattern:** resolve a known base dir, then create predictable subfolders.

* Example vibe:

  * `CATEGORICAL_DIR = SEC2_REPORTS_DIR / "categorical"`
  * `figures_root_210 = FIGURES_DIR / "2_10_univariate"`
  * `sec2_29_dir = SEC2_REPORTS_DIR / "sec2_29_postapply_verification"`
* Strength: this is the **good kind** of repetition—each section *should* own its subdir layout.
* Weakness: you sometimes derive these subdirs from different bases (some from `FIGURES_DIR`, some from `sec2_reports_dir.parent`, etc.) which makes folder structure drift.

✅ Belongs to: each section, **but** should be anchored consistently (one canonical base).

---

### 5) **“Section-local variable naming fork” style** (2.5.* and 2.6.* especially)

**Pattern:** same resolver as style #2, but assigned into section-specific vars:

* `section2_reports_dir_2501`, `_2502`, `_25A`, `_25B`, `_25C`, `_25D`…
* Strength: makes it explicit what section is using which directory var.
* Weakness: it’s mostly redundant if all sections share the same base dir. It’s also easy for one of these to accidentally point somewhere else and you won’t notice.

✅ Belongs to: only where the section truly has a distinct directory root.
Otherwise: prefer **one global base** + section subdirs.

---

### 6) **“Ambiguous / conflicting base paths” style** (2.6A shows this hard)

**Pattern:** sometimes Section 2 reports dir is:

* `(PROJECT_ROOT / "resources" / "reports" / "section2")`
  …but elsewhere it’s:
* `(PROJECT_ROOT / "reports" / "section2")`  ✅ this is a different tree
  …and sometimes fallback is:
* `Path.cwd() / "resources" / "reports" / "sec2"` ✅ different naming: `sec2` vs `section2`

This isn’t just style—it’s **semantic divergence**.

* Strength: none (unless you intentionally support legacy layouts).
* Weakness: silent file scattering.

✅ Belongs to: nowhere. Pick one canonical tree and migrate.

---

### 7) **“Overwriting global names” style** (notebook foot-gun)

**Pattern:** `sec2_reports_dir = sec2_reports_dir.resolve()` inside a cell that also checks `if "sec2_reports_dir" in globals()`.

* Strength: keeps the global tidy.
* Weakness: if the global is already correct, fine; if it’s wrong, you keep reinforcing wrongness. Also, reassigning globals deep in the notebook makes debugging harder.

✅ Belongs to: bootstrap only.

---

### 8) **“Non-directory stuff mixed into directory blocks” style**

**Pattern:** SciPy imports, df guards, diagnostics collector initialization mixed into “resolve directories.”

* Strength: none (conceptually).
* Weakness: makes it harder to see what is truly “bootstrap”.

✅ Belongs to: split out into “imports/guards” vs “paths” cells.

---

## Should you resolve to one pattern?

Yes.

### The “supreme” style (best default)

**Supreme default = Style #1 + #2/#3 centralized into bootstrap:**

* **One bootstrap cell/function** resolves:

  * `SEC2_REPORTS_DIR` (canonical)
  * `SECTION2_REPORT_PATH`
  * `FIGURES_DIR`
  * any other *global bases* (ARTIFACTS_DIR, PROCESSED_DATA_DIR if you want)
* Then every other section does **either**:

  1. **Hard guard + reuse** (Style #1) if it depends on bootstrap
  2. Create **only its section subdirs** (Style #4)

That combo is “supreme” because it:

* prevents path drift
* eliminates duplication
* keeps sections readable
* preserves notebook safety (you can decide which sections require bootstrap vs can run standalone)

## The untangling plan (practical, no extra ceremony)

* **Bootstrap (2.0.x)**: the only place you resolve base dirs and global paths.
* **Every section**:

  * start with: `assert "SEC2_REPORTS_DIR" in globals()` (or soft fallback if you want)
  * define section subdir(s) from `SEC2_REPORTS_DIR` and `FIGURES_DIR`
  * never re-derive `SECTION2_REPORT_PATH` again

💡💡 If you want standalone cells sometimes: allow a *single* fallback bootstrap snippet (tiny) that runs only if globals are missing—but keep it identical everywhere (copy/paste one canonical mini-bootstrap).

If you paste your current bootstrap cell/function (2.0.0/2.0.1), I can point to **exactly which duplicated resolver blocks become dead weight** and which section subdir blocks should remain.

># TIGHTEN THE EXPLAIN:

Yep — here’s the tight version.

## What’s going on

You’ve mixed **8 patterns** for “where do I write/read Section 2 stuff?” and you repeat them all over the notebook. That’s why it feels tangled.

## The 8 patterns (super short)

1. **Hard-guard reuse (best for later sections)**
   “Bootstrap must have run.”
   `assert SEC2_REPORTS_DIR and SECTION2_REPORT_PATH exist → reuse them`

2. **Fallback chain resolver (good only in bootstrap)**
   `sec2_reports_dir = globals → REPORTS_DIR → PROJECT_ROOT → Path(...)`

3. **Repeat SECTION2_REPORT_PATH resolver (should be bootstrap only)**
   “if not defined, derive it” — repeated tons of times.

4. **Section-specific subdir builder (good, keep per section)**
   `sec2_29_dir = SEC2_REPORTS_DIR / "sec2_29_postapply_verification"`
   `figures_root_210 = FIGURES_DIR / "2_10_univariate"` etc.

5. **Section-local base var names (mostly unnecessary)**
   `section2_reports_dir_2501`, `_2502`, `_25D`… all usually point to same place.

6. **Conflicting base trees (bad)**
   Sometimes: `PROJECT_ROOT/resources/reports/section2`
   Sometimes: `PROJECT_ROOT/reports/section2`
   Sometimes: `.../sec2` vs `.../section2`
   → this *scatters files into different folders*.

7. **Reassigning globals deep in the notebook (foot-gun)**
   Overwriting `sec2_reports_dir`/`FIGURES_DIR` in random sections.

8. **Non-directory stuff mixed into “resolve dirs” blocks (noise)**
   Imports, df guards, diagnostics list init mixed into path code.

---

## What to do (the simple rule)

**One “supreme” approach:**

### A) Bootstrap (2.0.x) does ALL base resolution ONCE:

* `SEC2_REPORTS_DIR`
* `SECTION2_REPORT_PATH`
* `FIGURES_DIR`
* (optionally `ARTIFACTS_DIR`, processed data dir)

### B) Every later section does ONLY:

1. **Hard-guard + reuse** (Pattern #1)
2. **Create its own subfolders** (Pattern #4)

That’s it.

---

## What you keep vs move

* **Move to bootstrap:** anything that resolves `sec2_reports_dir` / `SEC2_REPORTS_DIR` / `SECTION2_REPORT_PATH` / `FIGURES_DIR` (patterns **#2, #3, #6, #7**).
* **Keep inside sections:** only the section’s specific subdirs (pattern **#4**), plus any real section logic.

💡💡 If you want “run-anywhere” cells: make **one tiny shared fallback snippet** that runs only if globals are missing — and reuse that exact snippet everywhere (don’t invent new variants).

If you tell me which single directory tree you want as canonical (`resources/reports/section2` vs `reports/section2`), I’ll state the exact “one pattern” in 5–10 lines and map each of your repeated blocks to “delete/move/keep.”

># Q: Which PATTERN is the most redundant?

The **single most redundant statement block** (by far) is this one:

> **“Ensure `SECTION2_REPORT_PATH` exists / is defined”**
> (the `if "SECTION2_REPORT_PATH" not in globals(): ...` chain)

You repeat that **over and over** in nearly every section (2.3.x, 2.4.x, 2.5.x, 2.6.x, 2.10.x, 2.11.x…), and it’s almost always identical.

**Runner-up (also extremely redundant):** the repeated base-dir resolver:

> **“Resolve Section 2 reports dir”**
> `if "sec2_reports_dir" in globals(): ... elif REPORTS_DIR ... elif PROJECT_ROOT ... else Path(...)`

But if you’re picking *one* “most redundant,” it’s the **SECTION2_REPORT_PATH resolver**, because once bootstrap sets it, *no later section should ever re-derive it again*.

💡💡 Quick heuristic: if a block’s only job is to compute a **global path** (not a section subfolder), it’s bootstrap-only—so repeated copies are pure redundancy.

Below are **each occurrence I can see in your pasted blob** of the **most redundant block** (the `if "SECTION2_REPORT_PATH" not in globals(): ...` resolver), printed **verbatim** as it appears.

---

### Example 1

```python
# Section 2 summary path
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 2

```python
# Shared Section 2 summary
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = (sec2_reports_dir.parent / "section2_summary.csv").resolve()
```

### Example 3

```python
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 4

```python
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 5

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 6

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 7

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 8

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 9

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 10

```python
# Shared Section 2 summary
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 11

```python
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 12

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 13

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 14

```python
# Ensure SECTION2_REPORT_PATH exists / is defined
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

### Example 15

```python
if "SECTION2_REPORT_PATH" not in globals():
    if "REPORTS_DIR" in globals():
        SECTION2_REPORT_PATH = (REPORTS_DIR / "section2_summary.csv").resolve()
    elif "PROJECT_ROOT" in globals():
        SECTION2_REPORT_PATH = (PROJECT_ROOT / "resources" / "reports" / "section2_summary.csv").resolve()
    else:
        SECTION2_REPORT_PATH = Path("resources/reports/section2_summary.csv").resolve()
```

---

If you want, I can also **label each one with the section it’s adjacent to** (2.4 categorical, 2.5.0x, 2.5.15, etc.) so you can immediately see where to delete/move them. **Do you want the labels added?**

># So, If I am settling on SECTION2_REPORT_PATH , should I get rid of :

```py
# Shared Section 2 reports dir
if "sec2_reports_dir" in globals():
    sec2_reports_dir = sec2_reports_dir.resolve()
elif "REPORTS_DIR" in globals():
    sec2_reports_dir = (REPORTS_DIR / "section2").resolve()
elif "PROJECT_ROOT" in globals():
    sec2_reports_dir = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
else:
    sec2_reports_dir = Path("resources/reports/section2").resolve()
```

If you’re truly “settling on” (i.e., **bootstrapping once and reusing**) `SECTION2_REPORT_PATH`, then **yes — you should get rid of that repeated `sec2_reports_dir` resolver in every downstream section**.

Keep it **only in one centralized bootstrap place** (your 2.0.x bootstrap cell/function), because:

* `SECTION2_REPORT_PATH` is the *thing you actually write to / read from* for the unified summary.
* Re-resolving `sec2_reports_dir` later is just another chance to accidentally point somewhere else (`resources/reports/section2` vs `reports/section2`, etc.).

### What to do instead in downstream cells

Use a guard + reuse pattern:

```python
assert "SEC2_REPORTS_DIR" in globals(), "Run Section 2 bootstrap (2.0.x) first."
assert "SECTION2_REPORT_PATH" in globals(), "Run Section 2 bootstrap (2.0.x) first."

# If you want a local alias for readability:
sec2_reports_dir = SEC2_REPORTS_DIR
```

### One important nuance

If you *haven’t* standardized on `SEC2_REPORTS_DIR` as well, then you still need *some* way to anchor directories. In that case, pick one canonical base and set it once:

* **Canonical base dir:** `SEC2_REPORTS_DIR`
* **Canonical summary file:** `SECTION2_REPORT_PATH`

Then downstream sections never “discover” paths again—they only build subfolders from the canonical base.

💡💡 So the answer is: **delete that block everywhere except bootstrap**. If you want, paste your 2.0.x bootstrap and I’ll show the exact minimal canonical version (no behavior change, just centralized).

># Q: Which one is better?

**Better = keep `SEC2_REPORTS_DIR` as the canonical base, and derive everything else from it (including `SECTION2_REPORT_PATH`).**

### Why that’s better

* **One anchor directory** → every artifact ends up in one predictable tree.
* `SECTION2_REPORT_PATH` is just *one file*; it’s not enough to anchor your whole folder structure.
* Most of your mess comes from resolving “base dirs” differently in different sections. A single base (`SEC2_REPORTS_DIR`) stops that.

### The clean canonical pattern

In **bootstrap (2.0.x) only**:

* set `SEC2_REPORTS_DIR` once
* set `SECTION2_REPORT_PATH` once (ideally derived from the same base)

In **every other section**:

* guard + reuse:

  * `assert "SEC2_REPORTS_DIR" in globals()`
  * `assert "SECTION2_REPORT_PATH" in globals()`
* create only **section subdirs** under `SEC2_REPORTS_DIR`

### If you must pick only one “canonical thing”

Pick **`SEC2_REPORTS_DIR`**.
Then make `SECTION2_REPORT_PATH` live under it (or consistently beside it), but don’t let it drive directory discovery.

If you tell me whether you want `section2_summary.csv` to live:

* **inside** `SEC2_REPORTS_DIR` (most common), or
* **next to** it (one level up),

I’ll give you the exact canonical lines for bootstrap + the exact two-line reuse snippet for every section.

># Q: If I am settling on SECTION2_REPORT_PATH , should I get rid of :

```python
# Shared Section 2 reports dir if "sec2_reports_dir" in globals():
sec2_reports_dir = sec2_reports_dir.resolve()
elif "REPORTS_DIR" in globals(): sec2_reports_dir = (REPORTS_DIR / "section2").resolve()
elif "PROJECT_ROOT" in globals(): sec2_reports_dir = (PROJECT_ROOT / "resources" / "reports" / "section2").resolve()
else: sec2_reports_dir = Path("resources/reports/section2").resolve()
```

If you’re truly “settling on” (i.e., **bootstrapping once and reusing**) `SECTION2_REPORT_PATH`, then **yes — you should get rid of that repeated `sec2_reports_dir` resolver in every downstream section**.

Keep it **only in one centralized bootstrap place** (your 2.0.x bootstrap cell/function), because:

* `SECTION2_REPORT_PATH` is the *thing you actually write to / read from* for the unified summary.
* Re-resolving `sec2_reports_dir` later is just another chance to accidentally point somewhere else (`resources/reports/section2` vs `reports/section2`, etc.).

### What to do instead in downstream cells

Use a guard + reuse pattern:

```python
assert "SEC2_REPORTS_DIR" in globals(), "Run Section 2 bootstrap (2.0.x) first."
assert "SECTION2_REPORT_PATH" in globals(), "Run Section 2 bootstrap (2.0.x) first."

# If you want a local alias for readability:
sec2_reports_dir = SEC2_REPORTS_DIR
```

### One important nuance

If you *haven’t* standardized on `SEC2_REPORTS_DIR` as well, then you still need *some* way to anchor directories. In that case, pick one canonical base and set it once:

* **Canonical base dir:** `SEC2_REPORTS_DIR`
* **Canonical summary file:** `SECTION2_REPORT_PATH`

Then downstream sections never “discover” paths again—they only build subfolders from the canonical base.

💡💡 So the answer is: **delete that block everywhere except bootstrap**. If you want, paste your 2.0.x bootstrap and I’ll show the exact minimal canonical version (no behavior change, just centralized).

># Q: Setting directories in each section cell (i.e. 2.1.1, 2.1.7, 2.4.14)

Those `mkdir` lines belong **in your one-time bootstrap / directory-map cell**, not inside a specific check cell (like 2.1.1 / 2.1.7 / 2.4.14).

### Best place

Put them in **Part 6 (Section directory map)** *right after* you define `SEC2_FIGURE_DIRS` and before you start running any section logic.

You already have this pattern:

```python
SEC2_FIGURE_DIRS = {s: (FIGURES_DIR / "section2" / s.replace(".", "_")).resolve() for s in SEC2_SECTIONS}

for d in (*SEC2_REPORT_DIRS.values(), *SEC2_ARTIFACT_DIRS.values(), *SEC2_FIGURE_DIRS.values()):
    d.mkdir(parents=True, exist_ok=True)
```

So ideally you **don’t need** those extra per-variable mkdirs at all.

---

## If those variables are section-specific figure roots

Map them to your canonical dirs instead of standalone roots:

```python
fig_root_211            = SEC2_FIGURE_DIRS["2.11"]          # section 2.11 figures root
bivariate_figures_root_210 = SEC2_FIGURE_DIRS["2.10"]       # or wherever you intend bivariate to live
figures_root_211        = SEC2_FIGURE_DIRS["2.11"]
```

And then **don’t mkdir them**, because the bootstrap already did.

---

## If you want subfolders (recommended)

Create subfolders **inside** the canonical root *in the section cell*:

```python
fig_root_211 = SEC2_FIGURE_DIRS["2.11"]
bivariate_figures_root_210 = SEC2_FIGURE_DIRS["2.10"] / "bivariate"
figures_root_211 = SEC2_FIGURE_DIRS["2.11"] / "summary"

bivariate_figures_root_210.mkdir(parents=True, exist_ok=True)
figures_root_211.mkdir(parents=True, exist_ok=True)
```

### Rule of thumb

* **Bootstrap (Part 6):** make the *base* dirs (`SEC2_FIGURE_DIRS[...]`) once.
* **Section cells (2.x.y):** make *subfolders* only if that section needs them.

That keeps everything predictable and avoids a million scattered `mkdir`s.

># Q: Where do i define the fig_root_211 and bivariate_fig_root_210?

then where to define these?
figures_dir_25C.mkdir(parents=True, exist_ok=True)
section2_reports_dir_25C.mkdir(parents=True, exist_ok=True)

Define **all directory “roots” once, in your bootstrap (2.0.0)**, then every later section just *reads* them.

You already did this right with:

* `SEC2_REPORT_DIRS`
* `SEC2_ARTIFACT_DIRS`
* `SEC2_FIGURE_DIRS`

So the answers are:

## Where to define `fig_root_211` and `bivariate_fig_root_210`

**Define them inside the section cell that uses them** (e.g., at the top of 2.11 / 2.10), by pulling from the maps you created in 2.0.0:

```python
# inside section 2.11 cell (or wherever you need it)
assert "SEC2_FIGURE_DIRS" in globals(), "Run 2.0.0 Part 6 first."

fig_root_211 = SEC2_FIGURE_DIRS["2.11"]
bivariate_fig_root_210 = SEC2_FIGURE_DIRS["2.10"]  # if bivariate lives under 2.10

fig_root_211.mkdir(parents=True, exist_ok=True)
bivariate_fig_root_210.mkdir(parents=True, exist_ok=True)
```

💡💡 Don’t define these as new global “truth” variables in random sections. The truth is the dict (`SEC2_FIGURE_DIRS[...]`). Local variables like `fig_root_211` are just convenient aliases **for that cell**.

---

## Where to define `figures_dir_25C` and `section2_reports_dir_25C`

Same rule: **define them at the top of the cell that uses them** by referencing your canonical roots.

### If `25C` is a subsection under 2.5:

Put its report outputs under the **2.5 report folder**, and figures under **2.5 figure folder**.

```python
assert "SEC2_REPORT_DIRS" in globals(), "Run 2.0.0 Part 6 first."
assert "SEC2_FIGURE_DIRS" in globals(), "Run 2.0.0 Part 6 first."

section2_reports_dir_25C = (SEC2_REPORT_DIRS["2.5"] / "2_5C").resolve()
figures_dir_25C = (SEC2_FIGURE_DIRS["2.5"] / "2_5C").resolve()

section2_reports_dir_25C.mkdir(parents=True, exist_ok=True)
figures_dir_25C.mkdir(parents=True, exist_ok=True)
```

That keeps your structure consistent:

* `.../reports/section2/2_5/2_5C/`
* `.../figures/section2/2_5/2_5C/`

### If `25C` is actually a standalone section folder you want:

Then include it in your `SEC2_SECTIONS` list and let the dict map create it automatically. But for “subsections” (A/B/C), the pattern above (subfolder under the parent section dir) is cleaner.

---

## Rule of thumb

* **Bootstrap (2.0.0)**: create the canonical roots (`SEC2_*_DIRS` dicts)
* **Each section cell**: define a couple of local aliases (like `fig_root_211`) from those dicts
* **Each subsection A/B/C**: create subfolders under the parent section dir (like `/2_5C/`)

If you tell me what “25C” stands for (2.5.C?) and what content goes there, I can suggest a naming convention that matches your existing `2_4`, `2_10_1` style.


># Q: Which is a better choice?
CATEGORICAL_DIR = (FIGURES_DIR / "section2" / "categorical").resolve()
CATEGORICAL_DIR.mkdir(parents=True, exist_ok=True)
print("CATEGORICAL_DIR =", CATEGORICAL_DIR)
CATEGORICAL_DIR = /Users/b/DATA/PROJECTS/Telco/_T2/Level_3/resources/figures/section2/categorical

CATEGORICAL_DIR = (SEC2_ARTIFACTS_DIR / "categorical").resolve()
CATEGORICAL_DIR.mkdir(parents=True, exist_ok=True)
print("CATEGORICAL_DIR =", CATEGORICAL_DIR)
CATEGORICAL_DIR = /Users/b/DATA/PROJECTS/Telco/_T2/Level_3/resources/artifacts/section2/categorical

Second one is the better choice **for your project as written**:

```python
CATEGORICAL_DIR = (SEC2_ARTIFACTS_DIR / "categorical").resolve()
```

Because **everything you’re storing there is data artifacts** (CSVs, JSON, reports, indexes, “issues catalogs”, drift tables, etc.). Those are *not figures*. Putting them under `FIGURES_DIR` will confuse you later and break your “what goes where” mental model.

### Use this rule

* **`SEC2_ARTIFACTS_DIR/...`** → machine-readable outputs (csv/json/parquet), catalogs, indexes, metadata, run logs, “latest” pointers
* **`FIGURES_DIR/...`** → images only (png/svg/pdf), plots, charts, heatmaps

### What you should do instead (clean separation)

Keep two roots:

```python
# data artifacts
CATEGORICAL_DIR = (SEC2_ARTIFACTS_DIR / "categorical").resolve()
CATEGORICAL_DIR.mkdir(parents=True, exist_ok=True)

# figures (if you want a categorical figures bucket too)
CATEGORICAL_FIG_DIR = (FIGURES_DIR / "section2" / "categorical").resolve()
CATEGORICAL_FIG_DIR.mkdir(parents=True, exist_ok=True)
```

Then:

* `invalid_tokens.csv`, `issues_index.csv`, `category_drift_report.csv` → `CATEGORICAL_DIR`
* `entropy_barplot.png`, `drift_heatmap.png` → `CATEGORICAL_FIG_DIR`

If you want to align this with your per-section maps (`SEC2_ARTIFACT_DIRS["2.4"]`, etc.), an even cleaner pattern is:

* `CATEGORICAL_DIR = SEC2_ARTIFACT_DIRS["2.4"] / "categorical"` (since 2.4 is the categorical chapter)

But between the two options you posted: **artifacts path wins.**

Yes — **define these in bootstrap** (your Part 5 / Part 6 area), because every downstream cell assumes they exist and point to the same places.

### What to put in bootstrap

**1) Always define the “chapter roots” once**

* `SEC2_ARTIFACTS_DIR` (already)
* `FIGURES_DIR` (already)
* (optional but useful) `SEC2_DIR = SEC2_ARTIFACTS_DIR / "_latest"` for cross-section “latest” pointers

**2) Define categorical artifact + figure dirs once**
Put this right after you create `SEC2_ARTIFACTS_DIR` + `FIGURES_DIR`:

```python
# --- Section 2 categorical roots (define once in bootstrap) ---
CATEGORICAL_DIR = (SEC2_ARTIFACTS_DIR / "categorical").resolve()
CATEGORICAL_DIR.mkdir(parents=True, exist_ok=True)

CATEGORICAL_FIG_DIR = (FIGURES_DIR / "section2" / "categorical").resolve()
CATEGORICAL_FIG_DIR.mkdir(parents=True, exist_ok=True)

print("CATEGORICAL_DIR     =", CATEGORICAL_DIR)
print("CATEGORICAL_FIG_DIR =", CATEGORICAL_FIG_DIR)
```

### Why bootstrap is the right place

* Prevents `NameError` (like your `SEC2_DIR` issue earlier).
* Prevents drift: you won’t accidentally redefine `CATEGORICAL_DIR` later to a different meaning.
* Makes every 2.4.x cell portable (run it anytime after bootstrap).

💡💡 If you want the *cleanest long-term* structure, tie it to your per-section maps:

```python
CATEGORICAL_DIR     = (SEC2_ARTIFACT_DIRS["2.4"] / "categorical").resolve()
CATEGORICAL_FIG_DIR = (SEC2_FIGURE_DIRS["2.4"] / "categorical").resolve()
```

But if you haven’t standardized 2.4 as “categorical chapter” yet, your simpler version above is totally fine.

---
---

># Q:

for *this* project, **“chapter dirs” is the pro move**

It buys you the two things recruiters (and future-you) care about most: **predictability** and **low coupling**.

## Why “chapter dirs” is the pro move here

### 1) It matches how your notebook actually runs

Your Section 2 is a long, iterative notebook where you’ll re-run cells out of order sometimes. Chapter dirs mean:

* `CATEGORICAL_DIR` is always the same place
* you don’t depend on `SEC2_ARTIFACT_DIRS["2.4"]` existing yet
* fewer `NameError` and “did Part 6 run?” headaches

### 2) You stop leaking “architecture” into every section

Per-section ownership dirs force every section to know about the section-dir map. That’s coupling.

Chapter dirs let sections just say:

* “I produce categorical artifacts” → put them in the categorical chapter folder.
* “I produce categorical figures” → put them in the categorical figures folder.

That’s clean separation.

### 3) It makes “latest shared outputs” trivial

You already introduced `_latest` publishing (`SEC2_DIR`). With chapter dirs:

* canonical storage = chapter dir (stable history + easy browsing)
* cross-section consumption = `_latest` (pointer copy)

That’s a solid pattern.

## The one “pro” tweak I’d add 💡💡

Keep chapter dirs **as the canonical write location**, but add **optional subfolders per subsection** inside them (no new global map needed):

* `SEC2_ARTIFACTS_DIR/categorical/2_4_11/…`
* `SEC2_ARTIFACTS_DIR/categorical/2_4_13/…`

This preserves simplicity while keeping outputs organized as the project grows.

## So what should you do?

Yes: **chapter dirs for canonical storage**:

* `CATEGORICAL_DIR = SEC2_ARTIFACTS_DIR / "categorical"`
* `CATEGORICAL_FIG_DIR = FIGURES_DIR / "section2" / "categorical"`

And use `SEC2_DIR/_latest` only for “published pointers” like `dashboard_alerts.json`, `run_health_summary.csv`, etc.

If you want, paste your current Part 5 again and I’ll give you the clean final Part 5 block exactly how it should look with chapter dirs (minimal diffs).
