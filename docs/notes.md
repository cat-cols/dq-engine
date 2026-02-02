How would I layer the folders for my glossary that contains how to map a current design to Prefect flow?
I’d treat this like a little “Rosetta Stone” for your pipeline → Prefect, with **layers from general → specific**.

Here’s a clean, opinionated layout you could drop into `Telco/Library` or `Telco/docs`:

```text
Telco/
  docs/
    prefect_glossary/
      00_overview/
        README.md
      10_domain_language/
        sections.md
        artifacts.md
        checks_rules.md
      20_prefect_language/
        flows_tasks.md
        deployments_storage.md
        schedules_blocks.md
      30_mapping_patterns/
        section_to_flow.md
        check_to_task.md
        report_to_notification.md
      40_concrete_mappings/
        telco_level3/
          sections_to_flows.md
          artifacts_to_blocks.md
          configs_to_parameters.md
        edgar_project/        # later, to “prove” generality
          ...
      90_meta/
        changelog.md
        backlog.md
```

---

## What each layer does

### `00_overview/` – “What this glossary is”

* `README.md`

  * Why this exists: *“map existing designs (Section 2.x, artifacts, configs) to Prefect concepts in a consistent way.”*
  * How to read the rest (the “layers” below).
  * One tiny diagram showing: **Current Design → Mapping Pattern → Prefect Object**.

💡💡 This lets future-you (and recruiters) grok the system in 1–2 minutes.

---

### `10_domain_language/` – Your current design terms

This is **your world**: Telco pipeline / EDGAR patterns.

Examples:

* `sections.md`

  * 2.0 Bootstrap
  * 2.1 Type & role registration
  * 2.3 Numeric diagnostics
  * 2.5 Logic checks
  * 2.6 Cleaning, etc.
* `artifacts.md`

  * Raw vs processed vs artifacts vs reports
  * Where `numeric_profile_df.csv`, `logic_checks_summary.csv`, etc. live.
* `checks_rules.md`

  * “ratio rule”, “dependency rule”, “mutual exclusion”, “drift check” etc.

The goal: **define your vocabulary, independent of Prefect**.

---

### `20_prefect_language/` – Prefect concepts in your words

This is **Prefect’s world**, explained in your voice:

* `flows_tasks.md`

  * `Flow`: orchestrates a unit of work, can call subflows
  * `Task`: an atomic step (e.g. “compute numeric profile”, “run dependency checks”)
  * “subflow vs task” as it relates to “Section 2.x vs 2.3.7 internal step”
* `deployments_storage.md`

  * Deployment = “saved run recipe + schedule”
  * Storage blocks, result storage, etc.
* `schedules_blocks.md`

  * Cron, interval, RRule, etc.
  * Blocks for GCS, S3, local, etc.

Goal: **clean Prefect glossary**, but oriented to your use case.

---

### `30_mapping_patterns/` – The actual “Rosetta Stone”

This is the **core of what you asked about**: generic mapping recipes.

Examples:

* `section_to_flow.md`

  * Pattern: “One major section (e.g. 2.3 numeric diagnostics) → one Prefect flow”
  * When to split into subflows (`2.3.7 numeric profile` / `2.3.8 outliers`).
* `check_to_task.md`

  * Pattern: “One check rule or check family → one task”
  * E.g. “ratio check rule set” -> `task run_ratio_checks(df, config)`.
* `report_to_notification.md`

  * Pattern for “Section 2 summary → Prefect notifications / artifacts”
  * How a report becomes “upload to GCS + link in task logs”.

💡💡 Each file here can follow a template:

````md
# Pattern: <Domain Thing> → <Prefect Thing>

## When to use
- …

## Domain side
- Example: Section 2.3.7 numeric_profile_df.csv

## Prefect mapping
- Flow: telco_numeric_profile_flow
- Tasks:
  - load_df_task
  - compute_numeric_profile_task
  - write_profile_artifact_task

## Pros / Cons
- …

## Example snippet
```python
@flow
def telco_numeric_profile_flow(config_path: str):
    ...
````

````

---

### `40_concrete_mappings/` – Project-specific mapping tables

Now it gets **concrete and opinionated**.

Example: `telco_level3/sections_to_flows.md`

```md
# Telco Level 3 – Sections → Prefect Flows

| Section    | Description                          | Prefect Object                     |
|-----------:|--------------------------------------|------------------------------------|
| 2.0        | Bootstrap Section 2                  | Flow: `bootstrap_section2_flow`    |
| 2.1        | Type & role registration            | Flow: `type_role_registration_flow`|
| 2.3.7      | Numeric profile                     | Subflow: `numeric_profile_flow`    |
| 2.3.14     | Drift diagnostics                   | Subflow: `drift_diagnostics_flow`  |
| 2.5.3      | Mutual exclusion rules              | Task family under `logic_flow`     |
| 2.6A       | Controlled cleaning framework       | Flow: `controlled_cleaning_flow`   |
````

And `artifacts_to_blocks.md`:

```md
# Artifacts → Storage Blocks

| Artifact path                                      | Storage / Block         |
|---------------------------------------------------|-------------------------|
| resources/artifacts/section2/numeric_profile_*.csv| GCS block: `telco-artifacts` |
| resources/reports/section2/section2_summary.csv   | Local file system block |
```

This is where your **pipeline design** and **Prefect config** shake hands.

Later, for EDGAR:

* `edgar_project/sections_to_flows.md`
* `edgar_project/artifacts_to_blocks.md`

so you prove **pipeline generality**.

---

### `90_meta/` – To keep your brain sane

* `changelog.md`

  * “2025-11-21 – initial Prefect mapping for Telco Level3”
* `backlog.md`

  * “TODO: decide where drift dashboard lives (flow vs downstream report)”
  * “TODO: Prefect blocks for S3 vs local”

---

## Tiny naming tip 💡💡

Use **numbered folders** (`00_`, `10_`, `20_`…) so you can reorder later without breaking links, and they also visually communicate the “layering”:

1. Understand the *domain*.
2. Understand *Prefect*.
3. Learn the *mapping patterns*.
4. See *concrete project mappings*.

---

If you want, next I can:

* turn this into an actual `README.md` for `docs/prefect_glossary/`, or
* sketch a first “mapping pattern” page like `section_to_flow.md` specifically for your Telco Section 2.3 / 2.5 world.

