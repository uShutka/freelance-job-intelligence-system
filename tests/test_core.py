from freelance_job_intelligence_system.core import extract_rate, extract_skills, score_job
def test_job_scoring():
    text = "Remote Python FastAPI scraping with PostgreSQL, $45 hourly"
    assert extract_rate(text) == 45
    assert "python" in extract_skills(text)
    assert score_job(text) >= 80
