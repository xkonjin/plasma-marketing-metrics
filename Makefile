SHELL := /bin/bash

.PHONY: setup
setup:
	python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

.PHONY: env
env:
	export $$(grep -v '^#' .env | xargs)

.PHONY: ingest-social
ingest-social:
	source .venv/bin/activate && export $$(grep -v '^#' .env | xargs) && 	python scripts/fetch_x.py --since-days 7 && 	python scripts/fetch_linkedin.py --since-days 7

.PHONY: ingest-seo
ingest-seo:
	source .venv/bin/activate && export $$(grep -v '^#' .env | xargs) && 	python scripts/fetch_semrush.py --domain example.com --since-days 7

.PHONY: ingest-tiktok
ingest-tiktok:
	source .venv/bin/activate && export $$(grep -v '^#' .env | xargs) && 	python scripts/fetch_tiktok.py --handle plasma --since-days 7

.PHONY: ingest-ga4
ingest-ga4:
	source .venv/bin/activate && export $$(grep -v '^#' .env | xargs) && 	python scripts/fetch_ga4.py --since-days 7

.PHONY: dbt
dbt:
	export DBT_PROFILES_DIR=$$(pwd)/dbt && source .venv/bin/activate && dbt deps --project-dir dbt && dbt run --project-dir dbt