from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException

from freelance_job_intelligence_system.alerts.telegram import build_job_alert
from freelance_job_intelligence_system.analytics.market_metrics import (
    level_distribution,
    market_summary,
    rate_by_skill,
    skill_trends,
    source_summary,
)
from freelance_job_intelligence_system.pipeline import run_pipeline
from freelance_job_intelligence_system.repositories.job_repository import JobRepository

app = FastAPI(title="Freelance & Remote Job Market Intelligence System", version="0.1.0")


def _jobs() -> pd.DataFrame:
    return run_pipeline()


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    safe = frame.copy()
    return safe.where(pd.notnull(safe), None).to_dict(orient="records")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "freelance-job-intelligence-system"}


@app.get("/jobs")
def jobs(min_score: int | None = None) -> list[dict[str, Any]]:
    repository = JobRepository(_jobs())
    return _records(repository.list_jobs(min_score=min_score))


@app.get("/jobs/{job_id}")
def job_detail(job_id: str) -> dict[str, Any]:
    repository = JobRepository(_jobs())
    job = repository.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/analytics/summary")
def analytics_summary() -> dict[str, object]:
    return market_summary(_jobs())


@app.get("/analytics/sources")
def analytics_sources() -> list[dict[str, Any]]:
    return _records(source_summary(_jobs()))


@app.get("/analytics/skills")
def analytics_skills() -> list[dict[str, Any]]:
    return _records(skill_trends(_jobs()))


@app.get("/analytics/rates")
def analytics_rates() -> list[dict[str, Any]]:
    return _records(rate_by_skill(_jobs()))


@app.get("/analytics/levels")
def analytics_levels() -> list[dict[str, Any]]:
    return _records(level_distribution(_jobs()))


@app.get("/alerts/top")
def top_alert() -> dict[str, str]:
    top = _jobs().iloc[0]
    return {"message": build_job_alert(top)}
