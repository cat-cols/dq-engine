# Section 2 Execution Map

- **2.0.1 Reporting Bootstrap/Setup**  
  • Kind: `infra`  
  • Depends on: `1.x`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/reports/section2, /Users/b/DATA/PROJECTS/Telco/Level_3/reports/section2/section2_data_quality_20251114_154802.csv`
- **2.0.2 Config & Constants Registration**  
  • Kind: `infra`  
  • Depends on: `2.0.1`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/reports/section2/section2_config_checks.csv`
- **2.0.3 Logging & Metadata Setup**  
  • Kind: `infra`  
  • Depends on: `2.0.1, 2.0.2`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/resources/artifacts/section2_run_metadata.json`
- **2.0.4 Dataset Ingestion & Preview**  
  • Kind: `overview`  
  • Depends on: `1.5`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/reports/section2/dataset_overview.csv`
- **2.0.5 Row/Column Baseline Summary**  
  • Kind: `overview`  
  • Depends on: `2.0.4`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/reports/section2/baseline_summary.csv`
- **2.0.6 Identifier Detection & Registration**  
  • Kind: `overview`  
  • Depends on: `2.0.4, 2.0.5`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/resources/artifacts/protected_columns.yaml`
- **2.0.7 Dependency Registry Build**  
  • Kind: `infra`  
  • Depends on: `2.0.1, 2.0.2, 2.0.3, 2.0.4, 2.0.5, 2.0.6`  
  • Expected outputs: `/Users/b/DATA/PROJECTS/Telco/Level_3/resources/artifacts/section2_registry.json`
- **2.0.8 Sanity Preview Printout**  
  • Kind: `infra`  
  • Depends on: `2.0.7`  
  • Expected outputs: `stdout, section2_execution_map.md`
- **2.1 Base Schema & Consistency**  
  • Kind: `dq_step`  
  • Depends on: `2.0.x`  
  • Expected outputs: `2_1_report.csv`
- **2.2 Numeric Ranges & Outliers**  
  • Kind: `dq_step`  
  • Depends on: `2.1`  
  • Expected outputs: `2_2_report.csv`
- **2.3 Categorical Levels & Rarity**  
  • Kind: `dq_step`  
  • Depends on: `2.1`  
  • Expected outputs: `2_3_report.csv`
- **2.4 Missingness Patterns**  
  • Kind: `dq_step`  
  • Depends on: `2.1`  
  • Expected outputs: `2_4_report.csv`
- **2.5 Leakage & Target Dependence**  
  • Kind: `dq_step`  
  • Depends on: `2.1`  
  • Expected outputs: `2_5_report.csv`
- **2.6 Time/Drift & Stability Checks**  
  • Kind: `dq_step`  
  • Depends on: `2.1`  
  • Expected outputs: `2_6_report.csv`
- **2.7 Business Rules & Contracts**  
  • Kind: `dq_step`  
  • Depends on: `2.2, 2.3, 2.4`  
  • Expected outputs: `2_7_report.csv`
- **2.8 Aggregated DQ Score / Summary**  
  • Kind: `dq_step`  
  • Depends on: `2.2, 2.3, 2.4, 2.5, 2.6, 2.7`  
  • Expected outputs: `2_8_report.csv`
- **2.9 Export / Handoff**  
  • Kind: `dq_step`  
  • Depends on: `2.8`  
  • Expected outputs: `2_9_report.csv`