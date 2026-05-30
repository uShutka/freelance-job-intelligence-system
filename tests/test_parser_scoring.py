from freelance_job_intelligence_system.services.parser import (
    classify_level,
    extract_location,
    extract_rate,
    extract_skills,
    is_remote,
)
from freelance_job_intelligence_system.services.relevance_engine import score_relevance


def test_extract_rate_single_value():
    assert extract_rate("Remote Python work, $45 hourly") == 45


def test_extract_rate_range_averages_values():
    assert extract_rate("Budget is $40-60/hr") == 50


def test_extract_rate_returns_none_without_rate():
    assert extract_rate("No rate listed") is None


def test_extract_skills_finds_profile_skills():
    skills = extract_skills("Python FastAPI scraping with PostgreSQL and Docker")
    assert {"python", "fastapi", "postgresql", "scraping", "docker"}.issubset(set(skills))


def test_extract_location_detects_remote():
    assert extract_location("Remote EU contract") == "remote"


def test_is_remote_detects_worldwide():
    assert is_remote("Worldwide async role")


def test_classify_level_detects_senior():
    assert classify_level("Senior only, 8+ years required") == "senior"


def test_classify_level_detects_junior():
    assert classify_level("Junior entry level task") == "junior"


def test_classify_level_defaults_to_middle():
    assert classify_level("Python data automation contract") == "middle"


def test_relevance_engine_scores_strong_match_high():
    result = score_relevance("Python automation", "Remote Playwright FastAPI PostgreSQL Docker, $55 hourly")
    assert result.score >= 85
    assert "Python match" in result.reasons


def test_relevance_engine_penalizes_senior_only_roles():
    result = score_relevance("Lead architect", "Senior only 8+ years, $95 hourly")
    assert result.level == "senior"
    assert result.score < 60


def test_relevance_engine_penalizes_low_rate():
    result = score_relevance("Python task", "Remote Python scraping, $12 hourly")
    assert "Low hourly rate penalty" in result.reasons
