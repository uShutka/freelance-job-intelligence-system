import pandas as pd

from freelance_job_intelligence_system.alerts.telegram import build_job_alert
from freelance_job_intelligence_system.analytics.market_metrics import (
    level_distribution,
    market_summary,
    rate_by_skill,
    skill_trends,
    source_summary,
)
from freelance_job_intelligence_system.collectors.csv_collector import CSVJobCollector
from freelance_job_intelligence_system.collectors.mock_collectors import MockHackerNewsCollector, MockRedditCollector
from freelance_job_intelligence_system.pipeline import collect_jobs, run_pipeline
from freelance_job_intelligence_system.repositories.job_repository import JobRepository
from freelance_job_intelligence_system.services.enrichment import enrich_jobs


def test_csv_collector_loads_demo_jobs():
    frame = CSVJobCollector().collect()
    assert len(frame) >= 8
    assert {"id", "title", "description", "source"}.issubset(frame.columns)


def test_mock_collectors_return_sources():
    assert MockRedditCollector().collect()["source"].eq("reddit").all()
    assert MockHackerNewsCollector().collect()["source"].eq("hackernews").all()


def test_collect_jobs_deduplicates_ids():
    jobs = collect_jobs()
    assert jobs["id"].is_unique


def test_enrich_jobs_adds_score_and_skills():
    raw = pd.DataFrame(
        [{"id": "1", "title": "Python automation", "description": "Remote Playwright PostgreSQL $50/hr", "source": "test"}]
    )
    enriched = enrich_jobs(raw)
    assert enriched.iloc[0]["score"] > 60
    assert "python" in enriched.iloc[0]["skills"]


def test_run_pipeline_sorts_by_score():
    jobs = run_pipeline()
    scores = jobs["score"].tolist()
    assert scores == sorted(scores, reverse=True)


def test_repository_filters_by_min_score():
    repository = JobRepository(run_pipeline())
    filtered = repository.list_jobs(min_score=70)
    assert filtered["score"].ge(70).all()


def test_repository_get_job_returns_dict():
    jobs = run_pipeline()
    repository = JobRepository(jobs)
    job = repository.get_job(str(jobs.iloc[0]["id"]))
    assert job is not None
    assert "title" in job


def test_source_summary_has_average_score():
    summary = source_summary(run_pipeline())
    assert "average_score" in summary.columns


def test_skill_trends_counts_python():
    trends = skill_trends(run_pipeline())
    assert "python" in set(trends["skill"])


def test_rate_by_skill_returns_average_rate():
    rates = rate_by_skill(run_pipeline())
    assert rates["average_rate"].notna().all()


def test_level_distribution_contains_middle():
    levels = level_distribution(run_pipeline())
    assert "middle" in set(levels["level"])


def test_market_summary_returns_top_job():
    summary = market_summary(run_pipeline())
    assert summary["total_jobs"] >= 8
    assert summary["top_job_score"] >= 70


def test_job_alert_contains_score_and_skills():
    message = build_job_alert(run_pipeline().iloc[0])
    assert "Score:" in message
    assert "Skills:" in message
