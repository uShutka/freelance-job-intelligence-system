# Freelance & Remote Job Market Intelligence System

Production-style system that collects freelance and remote job posts, extracts skills and rates, classifies seniority, calculates relevance score, stores enriched records, exposes analytics through FastAPI, visualizes market trends, and prepares Telegram alerts for the best opportunities.

## Project Overview

This project is a market intelligence tool for freelance and remote job opportunities. It combines data collection, parsing, lightweight NLP, scoring, analytics, dashboarding, API design, tests, Docker, and CI.

## Business Problem

Freelancers and remote candidates often monitor many sources manually. Good opportunities are easy to miss, and raw job posts do not answer the important questions: which skills are in demand, which sources have better rates, and which posts are actually relevant.

## Solution

The system collects job posts from CSV and mock Reddit/Hacker News collectors, enriches them with extracted skills, hourly rate, location, seniority, relevance score, and score reasons, then serves the data through API, dashboard, and alert previews.

## Architecture

```text
Job Sources
-> Collectors
-> Parser & Enrichment Services
-> Relevance Engine
-> Repository Layer
-> Analytics Layer
-> FastAPI + Dashboard + Telegram Alerts
```

## Features

- Multi-source job collection
- Title/body/rate/location/skills parsing
- Seniority classification: junior, middle, senior
- Separate `relevance_engine.py` scoring module
- Source quality analytics
- Skill demand trends
- Average rates by skill
- Top opportunity alert preview
- REST API
- Streamlit dashboard
- Docker Compose
- pytest and GitHub Actions

## Tech Stack

Python, pandas, FastAPI, Streamlit, Plotly, Docker, pytest, ruff, Telegram Bot API-ready alert module.

## Relevance Scoring

The scoring model rewards matches with the target profile:

- Python match: +20
- Automation/scraping match: +20
- Data/analytics stack match: +15
- FastAPI backend match: +10
- Docker production setup: +5
- Remote-friendly post: +10
- Hourly rate detected: +10
- Low rate penalty: -10
- Senior-only penalty: -20
- Junior task penalty: -5

The scoring logic is intentionally isolated in `src/freelance_job_intelligence_system/services/relevance_engine.py` and covered by tests.

## Database Schema

Production-ready tables would include:

- `sources(id, name, type, base_url, is_active)`
- `job_posts(id, external_id, source_id, title, body, url, posted_at, collected_at)`
- `job_skills(id, job_id, skill)`
- `job_scores(id, job_id, relevance_score, level, hourly_rate, reasons, created_at)`
- `collection_runs(id, source_id, started_at, finished_at, status, items_collected, errors_count)`
- `job_alerts(id, job_id, alert_type, message, created_at)`

## Data Pipeline

1. Collect jobs from configured sources.
2. Deduplicate by external id.
3. Normalize title and body text.
4. Extract skills, hourly rate, location, and seniority.
5. Calculate relevance score and reasons.
6. Build analytics by source, skill, rate, and level.
7. Expose API/dashboard and prepare Telegram alert.

## API Endpoints

- `GET /health`
- `GET /jobs`
- `GET /jobs?min_score=70`
- `GET /jobs/{job_id}`
- `GET /analytics/summary`
- `GET /analytics/sources`
- `GET /analytics/skills`
- `GET /analytics/rates`
- `GET /analytics/levels`
- `GET /alerts/top`

## Dashboard Screenshots

Screenshots are stored in `docs/screenshots/`:

- Dashboard overview
- Skill trends
- Rate by skill
- Top jobs table
- API response example
- Telegram alert example

## Analytics Results

Example conclusions from the demo dataset:

- Python automation and data pipeline jobs have the highest relevance scores.
- Remote posts with explicit hourly rates are easier to prioritize and alert on.
- Senior-only roles may have higher rates, but relevance can be lower due to mismatch with target positioning.
- FastAPI, PostgreSQL, pandas, Playwright/Selenium, and dashboard work cluster into the strongest opportunity segment.

## How to Run

```bash
docker compose up --build
```

Open:

- API docs: `http://localhost:8003/docs`
- Dashboard: `http://localhost:8504`

Local development:

```bash
python -m pip install -e .
uvicorn freelance_job_intelligence_system.api.main:app --reload
streamlit run dashboard/streamlit_app.py
```

## Tests

```bash
pytest
ruff check .
```

The suite covers collectors, parsing, rate extraction, seniority classification, relevance scoring, enrichment, repositories, analytics, alerts, and API endpoints.

## Engineering Notes

The project is deliberately modular: collectors are replaceable, parsing is isolated, scoring is explainable, analytics consume enriched data, and alerts reuse the same top-job selection as the dashboard and API.

## Known Limitations

- External sources are mocked or CSV-based for portfolio reproducibility.
- Real job boards may require API keys, rate limiting, custom selectors, or terms-of-service review.
- Current NLP is rule-based and explainable, not ML-based.
- Telegram sending requires real credentials in environment variables.

## Future Improvements

- Add Reddit/Hacker News API integrations.
- Add PostgreSQL persistence and scheduled collection runs.
- Add semantic similarity scoring with embeddings.
- Add user-defined target profile weights.
- Add saved searches and weekly market reports.
