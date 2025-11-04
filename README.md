Marketing Metrics (MVP)
=================================

Purpose
---------------------------------
This repository contains an end-to-end, minimal-friction analytics stack to unify marketing metrics across Social (X, LinkedIn, TikTok), SEO (Semrush), PR (Brandwatch – optional), and Web (GA4) into a single warehouse (Supabase/Postgres) with transformations (dbt) and a BI dashboard (Metabase). It also includes scheduled reporting stubs for Slack (weekly) and Notion (monthly).

Architecture (at a glance)
---------------------------------
- Warehouse: Supabase (managed Postgres)
- BI: Metabase Cloud
- Ingestion:
  - Python jobs for APIs without 1st-class connectors (Typefully → X/LinkedIn, Semrush, Apify/TikTok)
  - Optional: Airbyte Cloud for GA4 and Brandwatch if licensed
- Transformations: dbt (models and materialized KPI views)
- Orchestration: GitHub Actions (cron) + Airbyte schedules (optional)
- Reporting: Weekly Slack digest and Monthly Notion doc (via scripts; connect to your tooling of choice)

Quick start
---------------------------------
1) Create a Supabase project and capture DATABASE_URL (Service Role preferred for ingestion).
2) Copy .env.example → .env and fill values (API keys, DATABASE_URL, etc.).
3) Apply base schema to Supabase using infra/schema.sql.
4) Create a Metabase Cloud workspace and connect it to the Supabase Postgres database.
5) Run Python ingestors locally (or rely on GitHub Actions once secrets are set):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env | xargs)  # load environment variables
python scripts/fetch_x.py --since-days 7
python scripts/fetch_linkedin.py --since-days 7
python scripts/fetch_semrush.py --domain example.com --since-days 7
python scripts/fetch_tiktok.py --handle plasma --since-days 7
python scripts/fetch_ga4.py --since-days 7
```

6) Build marts with dbt (ensure env points at the same database):

```bash
export DBT_PROFILES_DIR=$(pwd)/dbt
dbt deps --project-dir dbt
dbt run --project-dir dbt
```

7) Open Metabase and create the dashboard using the facts in dbt/models/marts.

Repository layout
---------------------------------
- infra/
  - schema.sql                # Base dims/raw/marts tables for Postgres (Supabase)
- ingestion/
  - config.py                 # Centralized configuration and environment handling
  - db.py                     # Postgres connection helpers and safe upsert utilities
  - http.py                   # Resilient HTTP client with retries/backoff
  - typefully.py              # X/LinkedIn ingestion (via Typefully API)
  - semrush.py                # SEO keyword/backlink ingestion (Semrush API)
  - tiktok_apify.py           # TikTok analytics via Apify actor
  - ga4.py                    # GA4 Reporting API → Postgres
  - brandwatch.py             # PR mentions (optional; stub if no license)
- scripts/
  - fetch_*.py                # Thin CLIs that call ingestion modules
- dbt/
  - dbt_project.yml           # dbt project configuration
  - packages.yml              # dbt package dependencies (dbt_utils)
  - profiles.yml              # dbt profiles (env-driven) for Postgres
  - models/                   # staging + marts models (facts)
- reporting/
  - weekly_digest.py          # Generates Slack-ready summary from marts
  - monthly_report.py         # Generates Notion-ready content from marts
- .github/workflows/
  - ingestion.yml             # Nightly ingestion schedule
  - dbt.yml                   # Nightly transformations
- docs/
  - metabase-setup.md         # How to connect Supabase to Metabase
  - airbyte-setup.md          # Optional: GA4/Brandwatch via Airbyte

Environment variables
---------------------------------
Copy .env.example to .env and fill in your values. Key entries:
- DATABASE_URL: Postgres connection string for Supabase
- TYPEFULLY_API_KEY, SEMRUSH_API_KEY, APIFY_TOKEN
- GA4_JSON_KEY_B64 (Service Account JSON, base64-encoded)
- BRANDWATCH_* (if licensed), optional

GitHub Actions (CI/CD)
---------------------------------
Workflows use the above env vars as GitHub Secrets. Recommended secrets:
- DATABASE_URL
- TYPEFULLY_API_KEY
- SEMRUSH_API_KEY
- APIFY_TOKEN
- GA4_JSON_KEY_B64
- BRANDWATCH_USERNAME / BRANDWATCH_PASSWORD (or BRANDWATCH_API_TOKEN)

Safety and idempotency
---------------------------------
- All ingestors are written to be idempotent and safe to re-run
- Upserts are key-based to prevent duplicates
- HTTP calls use retries with exponential backoff

Notes
---------------------------------
- If Typefully lacks specific metrics, you can call platform APIs directly in a drop-in function
- If Brandwatch isn’t available, leave PR ingestion disabled; marts still build
- All modules include detailed comments to aid hand-off to engineers