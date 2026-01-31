># Q: is there a cleaner way to call append_sec2?
>### is SECTION2_APPEND_SECTIONS.add("2.1.2") needed?
>

# 2.1.2 🪪 ID & Key Field Verification | def(reporting) no C()
print("\n2.1.2 🪪 ID & Key Field Verification")

# Guards
assert "df" in globals(), "❌ df not found. Run Section 2.0.0 first."
assert "CONFIG" in globals(), "❌ CONFIG not found. Run 2.0.0 first."
assert "SECTION2_REPORT_PATH" in globals(), "❌ SECTION2_REPORT_PATH missing. Run 2.0.1 first."
assert "SEC2_REPORTS_DIR" in globals(), "❌ SEC2_REPORTS_DIR missing. Run 2.0.0/2.0.1 first."

# Resolve ID columns from CONFIG with sensible fallback
id_cols_cfg = CONFIG.get("ID_COLUMNS", []) or ["customerID"]
if isinstance(id_cols_cfg, (str, bytes)):
    id_cols = [id_cols_cfg]
else:
    id_cols = list(id_cols_cfg)

# Build ID integrity table
id_rows = []
for col in id_cols:
    exists = col in df.columns
    if exists:
        s = df[col]
        non_null = int(s.notna().sum())
        n_nulls = int(s.isna().sum())
        n_dupes = int(df.duplicated(subset=[col]).sum())
        n_unique = int(s.nunique(dropna=True))
        unique_ok = bool(n_unique == non_null)
    else:
        non_null = 0
        n_nulls = np.nan if "np" in globals() else None
        n_dupes = np.nan if "np" in globals() else None
        unique_ok = False

    id_rows.append(
        {
            "id_column":   col,
            "exists":      bool(exists),
            "non_null":    non_null,
            "nulls":       n_nulls,
            "duplicates":  n_dupes,
            "unique_ok":   bool(unique_ok),
        }
    )

id_integrity_df = pd.DataFrame(id_rows)

# Write id_integrity_report.csv atomically
id_integrity_path = SEC2_REPORTS_DIR / "id_integrity_report.csv"
tmp_id_path = id_integrity_path.with_suffix(".tmp.csv")

id_integrity_df.to_csv(tmp_id_path, index=False)
os.replace(tmp_id_path, id_integrity_path)

print(f"✅ 2.1.2 ID integrity report written → {id_integrity_path}")
display(id_integrity_df)

# Build unified diagnostics chunk for 2.1.2
n_ids = len(id_cols)
n_non_unique = int((~id_integrity_df["unique_ok"]).sum()) if not id_integrity_df.empty else 0
status = "OK" if n_non_unique == 0 else "WARN"

sec2_chunk_212 = pd.DataFrame(
    {
        "section":        ["2.1.2"],
        "section_name":   ["ID & key field verification"],
        "check":          ["ID & key field verification"],
        "level":          ["info"],
        "status":         [status],
        "n_ids":          [n_ids],
        "n_non_unique":   [n_non_unique],
        "timestamp":      [pd.Timestamp.now()],
        "detail":         [
            f"ID integrity report written to {id_integrity_path.name}; "
            f"{n_non_unique} non-unique or invalid ID columns."
        ],
    }
)

display(sec2_chunk_212)

append_sec2(sec2_chunk_212, SECTION2_REPORT_PATH)
SECTION2_APPEND_SECTIONS.add("2.1.2")

---
---

># SOLUTION:

Yep, there’s a cleaner way — you don’t really want every section to remember to both:

1. call `append_sec2(...)`, **and**
2. manually do `SECTION2_APPEND_SECTIONS.add("2.1.2")`

That’s brittle and easy to forget.

You’ve already got a central helper (`append_sec2`), so the nicer pattern is:

> **Let `append_sec2` own the “this section has been appended” side-effect.**

---

## Option A: Make `append_sec2` update the set automatically ✅

Modify your `append_sec2` helper (wherever it lives) so it updates `SECTION2_APPEND_SECTIONS` using the `section` column from the chunk:

```python
def append_sec2(chunk: pd.DataFrame, report_path: Path):
    """Append a Section 2 diagnostics chunk to the unified report CSV."""

    # 1) Append/write as you already do
    if report_path.exists():
        existing = pd.read_csv(report_path)
        combined = pd.concat([existing, chunk], ignore_index=True)
    else:
        combined = chunk.copy()

    tmp_path = report_path.with_suffix(".tmp.csv")
    combined.to_csv(tmp_path, index=False)
    os.replace(tmp_path, report_path)

    # 2) Track which sections have been appended
    try:
        sec_ids = set(chunk["section"].dropna().astype(str).unique())
    except Exception:
        sec_ids = set()

    if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
        SECTION2_APPEND_SECTIONS.update(sec_ids)
```

Then your 2.1.2 cell can end simply with:

```python
append_sec2(sec2_chunk_212, SECTION2_REPORT_PATH)
```

…and you **drop** this line entirely:

```python
SECTION2_APPEND_SECTIONS.add("2.1.2")
```

Every section will automatically register itself when it appends.

💡💡 *Nice side-effect*: if a section ever appends multiple rows with different `section` values (e.g., `"2.1.2"` and `"2.1.3"` in one chunk), they all get tracked correctly without extra code.

---

## Option B: At least avoid magic strings

If you don’t want to touch `append_sec2` yet, a smaller cleanup is:

```python
THIS_SECTION = "2.1.2"

# ...build sec2_chunk_212 with "section": [THIS_SECTION]...

append_sec2(sec2_chunk_212, SECTION2_REPORT_PATH)
SECTION2_APPEND_SECTIONS.add(THIS_SECTION)
```

That way you don’t have `"2.1.2"` duplicated in multiple places, which reduces copy-paste mistakes.

---

If you're okay editing helpers, Option A is the “most proper” version: one call, one side-effect, no section-specific boilerplate at the bottom of every cell.

def append_sec2(
    chunk: pd.DataFrame,
    report_path: str | Path,
) -> Path:
    """
    Append a diagnostics chunk into the unified Section 2 report CSV.

    Parameters
    ----------
    chunk:
        1+ row DataFrame with Section 2 diagnostics.
    report_path:
        Path to the unified Section 2 CSV
        (usually SECTION2_REPORT_PATH from the notebook).

    Behaviour
    ---------
    * Ensures parent directory exists
    * If the report exists, merges columns and appends rows
    * Writes through a temporary file and uses os.replace for atomicity
    * Normalizes a few numeric columns if present
    """

    path = Path(report_path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            existing = pd.read_csv(path)
            all_cols = pd.Index(existing.columns).union(chunk.columns)
            out = pd.concat(
                [
                    existing.reindex(columns=all_cols),
                    chunk.reindex(columns=all_cols),
                ],
                ignore_index=True,
            )
        else:
            out = chunk.copy()

        # Optional: normalize some known numeric columns if present
        for col in _NUMERIC_NORMALIZE_COLS:
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

        out.to_csv(tmp_path, index=False)
        os.replace(tmp_path, path)
        print(f"🧾 Appended diagnostics → {path}")
    except Exception as e:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        print(f"⚠️ Could not append diagnostics: {e}")

    return path

---


># TODO: refactor append_sec2 so that it updates the set automatically without the use of:
>#### SECTION2_APPEND_SECTIONS.add("2.1.2")


Nice, thanks for dropping the helper in — this is exactly where that line belongs.

Here’s how I’d refactor `append_sec2` so it **automatically** updates `SECTION2_APPEND_SECTIONS` using the `section` column in `chunk`, and you never have to write:

```python
SECTION2_APPEND_SECTIONS.add("2.1.2")
```

in the sections themselves.

---

## Step 1: Refactor `append_sec2` to track sections

Minimal, backwards-compatible change:

* Add an optional `track_sections: bool = True` argument
* After a successful write, pull unique `section` values from `chunk`
* If `SECTION2_APPEND_SECTIONS` exists & is a set, update it

```python
def append_sec2(
    chunk: pd.DataFrame,
    report_path: str | Path,
    track_sections: bool = True,
) -> Path:
    """
    Append a diagnostics chunk into the unified Section 2 report CSV.

    Parameters
    ----------
    chunk:
        1+ row DataFrame with Section 2 diagnostics.
        Expected to have a 'section' column like '2.1.2'.
    report_path:
        Path to the unified Section 2 CSV
        (usually SECTION2_REPORT_PATH from the notebook).
    track_sections:
        If True, automatically add the chunk's section IDs into
        SECTION2_APPEND_SECTIONS (a global set), if present.

    Behaviour
    ---------
    * Ensures parent directory exists
    * If the report exists, merges columns and appends rows
    * Writes through a temporary file and uses os.replace for atomicity
    * Normalizes a few numeric columns if present
    * Optionally tracks which sections have appended diagnostics
    """

    path = Path(report_path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            existing = pd.read_csv(path)
            all_cols = pd.Index(existing.columns).union(chunk.columns)
            out = pd.concat(
                [
                    existing.reindex(columns=all_cols),
                    chunk.reindex(columns=all_cols),
                ],
                ignore_index=True,
            )
        else:
            out = chunk.copy()

        # Optional: normalize some known numeric columns if present
        for col in _NUMERIC_NORMALIZE_COLS:
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce").round(4)

        out.to_csv(tmp_path, index=False)
        os.replace(tmp_path, path)
        print(f"🧾 Appended diagnostics → {path}")

        # 🔗 Optional: track which sections have appended diagnostics
        if track_sections:
            try:
                # grab section IDs from the chunk, if present
                if "section" in chunk.columns:
                    sec_ids = (
                        chunk["section"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )
                else:
                    sec_ids = []
            except Exception:
                sec_ids = []

            if sec_ids and "SECTION2_APPEND_SECTIONS" in globals():
                # Only update if it's a set-like object
                if isinstance(SECTION2_APPEND_SECTIONS, set):
                    SECTION2_APPEND_SECTIONS.update(sec_ids)

    except Exception as e:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        print(f"⚠️ Could not append diagnostics: {e}")

    return path
```

💡💡 *Design bonus:* `track_sections` lets you reuse `append_sec2` in weird contexts without touching the global set if you ever need to.

---

## Step 2: Simplify your section cells

Now your 2.1.2 cell can just end like this:

```python
append_sec2(sec2_chunk_212, SECTION2_REPORT_PATH)
```

and you can **delete**:

```python
SECTION2_APPEND_SECTIONS.add("2.1.2")
```

from 2.1.2 and every other section that uses `append_sec2`.

As long as each `sec2_chunk_xxx` includes a `"section"` column (which you already do), they’ll all be tracked automatically.

---

If you want, next refinement we can do later is a tiny helper like `register_section("2.1.2")` for non-report-producing steps (like pure setup cells) so they can still hook into the same tracking set without writing ad hoc lines.
