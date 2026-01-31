># X: ARTIFACT REGISTRY

># 2 Types:
># 1: NO FUNCTIONS
># 2: FUNCTIONS

---
---

># V1: NO FUNCTIONS

Got you — **no `def`** anywhere. Below is the same “latest artifact registry” idea refactored into **drop-in, inline (procedural) snippets** you can paste into **2.0 bootstrap** and then reuse in sections by setting a few variables.

I’m giving you three pieces:

1. **Bootstrap constants + `_latest` setup** (goes in 2.0)
2. **Publish block** (copy/paste anywhere after you save an artifact)
3. **Resolve/consume block** (copy/paste anywhere you need to load an artifact, e.g., 2.9.5)

---

## 1) 2.0 bootstrap: create `_latest` + standard metadata suffix

Put this **right after** you create `SEC2_LATEST_DIR` (you already do):

```python
from pathlib import Path
import os, json, shutil
from datetime import datetime, timezone

assert "SEC2_LATEST_DIR" in globals(), "❌ SEC2_LATEST_DIR missing; run Part 5 first."
SEC2_LATEST_DIR = Path(SEC2_LATEST_DIR).resolve()
SEC2_LATEST_DIR.mkdir(parents=True, exist_ok=True)

# Convention: every published artifact has a sidecar meta json
SEC2_LATEST_META_SUFFIX = ".meta.json"

print("📌 SEC2_LATEST_DIR ready:", SEC2_LATEST_DIR)
```

No functions, just globals.

---

## 2) Publish block (copy/paste pattern)

Use this anytime you generate an artifact that other sections should consume.

### You set these variables:

* `PUBLISH_SRC_PATH` (Path to the file you just wrote)
* `PUBLISH_SECTION` (e.g., `"2.3"`)
* `PUBLISH_TAGS` (list of strings)
* optional `PUBLISH_NAME` (defaults to the filename)

```python
# -------------------------------
# SEC2 LATEST PUBLISH (no funcs)
# -------------------------------
PUBLISH_SRC_PATH = Path(PUBLISH_SRC_PATH).expanduser().resolve()
if not PUBLISH_SRC_PATH.exists():
    raise FileNotFoundError(f"❌ publish: src not found: {PUBLISH_SRC_PATH}")

PUBLISH_NAME = globals().get("PUBLISH_NAME", None) or PUBLISH_SRC_PATH.name
PUBLISH_SECTION = globals().get("PUBLISH_SECTION", None)
PUBLISH_TAGS = globals().get("PUBLISH_TAGS", []) or []
PUBLISH_OVERWRITE = bool(globals().get("PUBLISH_OVERWRITE", True))

PUBLISH_DEST_PATH = (SEC2_LATEST_DIR / PUBLISH_NAME).resolve()

if PUBLISH_DEST_PATH.exists() and not PUBLISH_OVERWRITE:
    print(f"   ⚠️ publish: exists and overwrite=False → {PUBLISH_DEST_PATH}")
else:
    # atomic copy: copy to tmp then replace
    _tmp = PUBLISH_DEST_PATH.with_suffix(PUBLISH_DEST_PATH.suffix + ".tmp")
    _tmp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PUBLISH_SRC_PATH, _tmp)
    os.replace(_tmp, PUBLISH_DEST_PATH)

    # write metadata sidecar
    _meta = {
        "name": PUBLISH_NAME,
        "published_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "section": PUBLISH_SECTION,
        "source_path": str(PUBLISH_SRC_PATH),
        "size_bytes": PUBLISH_DEST_PATH.stat().st_size if PUBLISH_DEST_PATH.exists() else None,
        "tags": list(PUBLISH_TAGS),
    }
    _meta_path = Path(str(PUBLISH_DEST_PATH) + SEC2_LATEST_META_SUFFIX)
    with _meta_path.open("w", encoding="utf-8") as f:
        json.dump(_meta, f, indent=2)

    print(f"   ✅ Published latest → {PUBLISH_DEST_PATH}")
```

### Example usage inside 2.3 after saving:

```python
PUBLISH_SRC_PATH = numeric_profile_path
PUBLISH_SECTION = "2.3"
PUBLISH_TAGS = ["profile", "numeric"]
# PUBLISH_NAME = "numeric_profile_df.csv"  # optional (defaults to same)
# PUBLISH_OVERWRITE = True                 # optional
# then paste publish block
```

---

## 3) Resolve/consume block (copy/paste pattern)

This finds the artifact by checking:

1. `_latest/<name>` first
2. then any fallback dirs you provide
3. optionally **recursive** search (rglob) for when artifacts are buried in subfolders

### You set:

* `RESOLVE_NAME` (like `"numeric_profile_df.csv"`)
* `RESOLVE_DIRS` (list of dirs to search after `_latest`)
* optional `RESOLVE_RECURSIVE` (`True/False`)
* optional `RESOLVE_REQUIRED` (`True/False`)

```python
# -----------------------------------
# SEC2 ARTIFACT RESOLVE (no funcs)
# -----------------------------------
RESOLVE_NAME = str(RESOLVE_NAME)
RESOLVE_RECURSIVE = bool(globals().get("RESOLVE_RECURSIVE", False))
RESOLVE_REQUIRED = bool(globals().get("RESOLVE_REQUIRED", False))

RESOLVED_PATH = None

# 1) prefer _latest
_cand = (SEC2_LATEST_DIR / RESOLVE_NAME).resolve()
if _cand.exists():
    RESOLVED_PATH = _cand

# 2) fallback dirs (direct)
if RESOLVED_PATH is None:
    for _d in (RESOLVE_DIRS or []):
        if _d is None:
            continue
        _d = Path(_d).expanduser().resolve()
        _cand = (_d / RESOLVE_NAME).resolve()
        if _cand.exists():
            RESOLVED_PATH = _cand
            break

# 3) optional recursive
if RESOLVED_PATH is None and RESOLVE_RECURSIVE:
    for _d in (RESOLVE_DIRS or []):
        if _d is None:
            continue
        _d = Path(_d).expanduser().resolve()
        if not _d.exists():
            continue
        _hits = list(_d.rglob(RESOLVE_NAME))
        if _hits:
            _hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)  # newest wins
            RESOLVED_PATH = _hits[0].resolve()
            break

if RESOLVED_PATH is None and RESOLVE_REQUIRED:
    _msg = "❌ resolve: artifact not found\n"
    _msg += f"   name: {RESOLVE_NAME}\n"
    _msg += f"   latest: {SEC2_LATEST_DIR}\n"
    _msg += "   searched:\n" + "\n".join([f"     - {Path(d).expanduser().resolve()}" for d in (RESOLVE_DIRS or []) if d is not None])
    raise FileNotFoundError(_msg)

print("   🔎 RESOLVED_PATH =", RESOLVED_PATH)
```

### Example usage in 2.9.5 for each artifact:

```python
RESOLVE_NAME = "numeric_profile_df.csv"
RESOLVE_DIRS = [
    SEC2_REPORT_DIRS.get("2.3"),
    SEC2_REPORTS_DIR,
]
RESOLVE_RECURSIVE = True
RESOLVE_REQUIRED = False
# paste resolve block

df_art = _safe_load_csv(RESOLVED_PATH) if RESOLVED_PATH else None
```

---

## 4) Optional: `_latest` “manifest” view (no functions)

```python
rows = []
for p in sorted(SEC2_LATEST_DIR.glob("*")):
    if p.name.endswith(SEC2_LATEST_META_SUFFIX):
        continue
    meta_path = Path(str(p) + SEC2_LATEST_META_SUFFIX)
    published = None
    section = None
    tags = None
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            published = meta.get("published_at_utc")
            section = meta.get("section")
            tags = meta.get("tags")
        except Exception:
            pass
    rows.append({"name": p.name, "section": section, "published_at_utc": published, "tags": tags, "path": str(p)})

latest_manifest_df = pd.DataFrame(rows)
display(latest_manifest_df)
```

---

## 💡💡 How this fixes your current pain (2.9.5)

Once you add a `PUBLISH_*` block to each upstream producer (2.3, 2.4, 2.5, …), 2.9.5 can just resolve from `_latest` and stop guessing file locations.

If you want, paste the **list of artifacts you want standardized** (the ones you attempted to merge in 2.9.5), and I’ll give you the exact **one-line “set vars”** you should add at the end of each producing section to publish them to `_latest`.

---
---

># V2: FUNCTIONS
Absolutely. Here’s a **clean, minimal “artifact registry”** you can drop into **2.0 bootstrap** that gives you:

* **Publish:** copy an artifact to `SEC2_LATEST_DIR/<artifact_name>` (atomic, with metadata)
* **Consume:** resolve an artifact by searching `_latest` first, then fallback dirs (optionally recursive)
* **One-liner ergonomics** for 2.3–2.10 and 2.9.5 rollups

Below is copy/paste-ready code.

---

# 1) Add this to 2.0 bootstrap (after SEC2_LATEST_DIR exists)

```python
from pathlib import Path
import os
import json
import shutil
from datetime import datetime, timezone

assert "SEC2_LATEST_DIR" in globals(), "❌ SEC2_LATEST_DIR missing; run bootstrap Part 5 first."
SEC2_LATEST_DIR = Path(SEC2_LATEST_DIR).resolve()
SEC2_LATEST_DIR.mkdir(parents=True, exist_ok=True)

# ---- Artifact Registry Helpers (Section 2) ----

def sec2_publish_latest(
    src_path,
    *,
    name=None,
    section=None,
    tags=None,
    overwrite=True,
    also_copy_to=None,   # optional additional destinations (list[Path])
):
    """
    Publish an artifact to SEC2_LATEST_DIR as the canonical cross-section input.

    - Copies src_path -> SEC2_LATEST_DIR/name (atomic)
    - Writes metadata -> SEC2_LATEST_DIR/name.meta.json
    """
    src_path = Path(src_path).expanduser().resolve()
    if not src_path.exists():
        raise FileNotFoundError(f"❌ publish_latest: src not found: {src_path}")

    dest_name = name or src_path.name
    dest_path = (SEC2_LATEST_DIR / dest_name).resolve()

    if dest_path.exists() and not overwrite:
        print(f"   ⚠️ publish_latest: exists and overwrite=False → {dest_path}")
        return dest_path

    # atomic copy
    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, tmp_path)
    os.replace(tmp_path, dest_path)

    meta = {
        "name": dest_name,
        "published_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "section": section,
        "source_path": str(src_path),
        "size_bytes": dest_path.stat().st_size if dest_path.exists() else None,
        "tags": list(tags) if tags else [],
    }
    meta_path = dest_path.with_suffix(dest_path.suffix + ".meta.json")
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    # optional fan-out
    if also_copy_to:
        for d in also_copy_to:
            d = Path(d).expanduser().resolve()
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest_path, (d / dest_name).resolve())

    print(f"   ✅ Published latest → {dest_path}")
    return dest_path


def sec2_resolve_artifact(
    name,
    *,
    section=None,
    search_dirs=None,
    prefer_latest=True,
    recursive=False,
    required=False,
):
    """
    Resolve an artifact path.

    Search order (default):
      1) SEC2_LATEST_DIR / name        (if prefer_latest)
      2) section dir (SEC2_REPORT_DIRS[section] or SEC2_ARTIFACT_DIRS[section]) if provided in search_dirs
      3) any additional search_dirs

    If recursive=True, rglob(name) within each search_dir.
    """
    name = str(name)

    # 1) latest first
    if prefer_latest:
        p = (SEC2_LATEST_DIR / name).resolve()
        if p.exists():
            return p

    # 2) build dirs
    dirs = []
    if search_dirs:
        dirs.extend([Path(d).expanduser().resolve() for d in search_dirs if d is not None])

    # 3) try direct lookup
    for d in dirs:
        cand = (d / name).resolve()
        if cand.exists():
            return cand

    # 4) optionally recursive
    if recursive:
        for d in dirs:
            if d.exists():
                hits = list(d.rglob(name))
                if hits:
                    # newest wins
                    hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                    return hits[0].resolve()

    if required:
        raise FileNotFoundError(
            "❌ sec2_resolve_artifact: not found\n"
            f"   name: {name}\n"
            f"   prefer_latest: {prefer_latest}\n"
            f"   recursive: {recursive}\n"
            "   searched:\n" + "\n".join([f"     - {d}" for d in dirs])
        )
    return None


def sec2_latest_manifest():
    """
    Quick view of what's in _latest (filenames + timestamps if meta exists).
    """
    rows = []
    for p in sorted(SEC2_LATEST_DIR.glob("*")):
        if p.name.endswith(".meta.json"):
            continue
        meta_path = p.with_suffix(p.suffix + ".meta.json")
        published = None
        section = None
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                published = meta.get("published_at_utc")
                section = meta.get("section")
            except Exception:
                pass
        rows.append({"name": p.name, "section": section, "published_at_utc": published, "path": str(p)})
    return pd.DataFrame(rows)
```

---

# 2) Use it when creating artifacts in 2.x sections (publish once you save)

Example: in **2.3 numeric profile** after you save `numeric_profile_df.csv`:

```python
numeric_profile_path = SEC2_REPORT_DIRS["2.3"] / "numeric_profile_df.csv"
numeric_profile_df.to_csv(numeric_profile_path, index=False)

sec2_publish_latest(
    numeric_profile_path,
    section="2.3",
    tags=["profile", "numeric"]
)
```

Same idea for 2.4 categorical profile, 2.5 logic readiness, etc.

---

# 3) Update 2.9.5 to consume from `_latest` first (no hunting)

In 2.9.5, instead of hardcoding per-section paths, do:

```python
SECTION2_ARTIFACTS = {
    "numeric_profile_df.csv": ("feature", ["missing_pct", "outlier_pct"]),
    "categorical_profile_df.csv": ("feature", ["missing_pct", "domain_violation_pct"]),
    "logic_readiness_report.csv": ("feature", ["logic_violation_pct", "contract_breach_flags"]),
    "drift_report.csv": ("feature", ["drift_score"]),
    "effect_stability_metrics.csv": ("feature", ["effect_stability_score"]),
    "statistical_readiness_index.csv": ("feature", ["sri_score"]),
    "signal_to_noise_report.csv": ("feature", ["snr_bucket", "bias_risk_flag"]),
}

# fallback dirs if not in _latest
fallback_dirs = [
    SEC2_REPORT_DIRS.get("2.3"),
    SEC2_REPORT_DIRS.get("2.4"),
    SEC2_REPORT_DIRS.get("2.5"),
    SEC2_REPORT_DIRS.get("2.6"),
    SEC2_REPORT_DIRS.get("2.7"),
    SEC2_REPORT_DIRS.get("2.8"),
    SEC2_REPORTS_DIR,
]

for fname, (key, metric_cols) in SECTION2_ARTIFACTS.items():
    df_path = sec2_resolve_artifact(
        fname,
        search_dirs=fallback_dirs,
        prefer_latest=True,
        recursive=True,     # handles your subfolder situation
        required=False
    )
    if df_path is None:
        print(f"   ⚠️ 2.9.5: {fname} not found (latest+fallback); skipping.")
        continue

    df_art = _safe_load_csv(df_path)
    ...
```

Now 2.9.5 “just works” as soon as upstream sections publish.

---

# 4) Sanity check: see what’s currently published

Run:

```python
display(sec2_latest_manifest())
```

---

## 💡💡 One tiny policy that makes this shine

When you create any rollup-worthy artifact, always save it with:

* a `feature` column (not index)
* stable filename (don’t version the name — version the run elsewhere)

Then `_latest` becomes your “semantic interface” between sections.

---

If you want, paste the list of artifacts you consider “cross-section inputs” (the ones 2.9.5 should roll up), and I’ll give you a **standard publish call** for each one (and where it should live: reports vs artifacts).
