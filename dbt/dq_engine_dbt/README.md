# DQ Engine + Snowflake + dbt + GitHub Actions (hireable scaffold)

**Ingest → Snowflake RAW → dbt build/tests → DQ Engine deep diagnostics → DQ results tables + artifacts → CI gating**

Supports:
- **Snowflake** (primary)
- **DuckDB** (local dev fallback)

## One-time Snowflake setup

```sql
create warehouse if not exists DBT_WH
  warehouse_size='XSMALL'
  auto_suspend=60
  auto_resume=true
  initially_suspended=true;

create database if not exists DQ_ENGINE;
create schema if not exists DQ_ENGINE.RAW;
create schema if not exists DQ_ENGINE.ANALYTICS;
create schema if not exists DQ_ENGINE.DQ;

create role if not exists DBT_ROLE;

grant usage on warehouse DBT_WH to role DBT_ROLE;
grant usage on database DQ_ENGINE to role DBT_ROLE;
grant usage on schema DQ_ENGINE.RAW to role DBT_ROLE;
grant usage on schema DQ_ENGINE.ANALYTICS to role DBT_ROLE;
grant usage on schema DQ_ENGINE.DQ to role DBT_ROLE;

grant create table, create view, create stage, create file format on schema DQ_ENGINE.RAW to role DBT_ROLE;
grant create table, create view on schema DQ_ENGINE.ANALYTICS to role DBT_ROLE;
grant create table, create view on schema DQ_ENGINE.DQ to role DBT_ROLE;

create user if not exists DBT_SVC
  default_role=DBT_ROLE
  default_warehouse=DBT_WH
  must_change_password=false;

grant role DBT_ROLE to user DBT_SVC;
```

## Key-pair auth (recommended)

Generate keys (PKCS#8, encrypted):

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 aes-256-cbc -inform PEM -out dbt_svc_key.p8
openssl rsa -in dbt_svc_key.p8 -pubout -out dbt_svc_key.pub
```

Set `rsa_public_key` on the Snowflake user. citeturn0search18turn0search15

dbt: use `private_key_path` (most reliable across dbt versions). citeturn0search15  
Python connector: pass the key as DER bytes (not a raw string). citeturn0search1

## Local run

1) Copy `.env.example` to `.env` and fill values
2) Install:

```bash
pip install -e ".[snowflake]"
```

3) Run:

```bash
dq run --config configs/dq_project.yml
```

Skip dbt (if you already ran dbt build):

```bash
dq run --config configs/dq_project.yml --skip-dbt
```

## GitHub Actions CI

Add repo secrets:
- SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_ROLE, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
- SNOWFLAKE_PRIVATE_KEY_P8 (contents of your `.p8`)
- SNOWFLAKE_PRIVATE_KEY_PASSPHRASE

CI pattern aligns with dbt docs on CI workflows. citeturn0search2turn0search17
