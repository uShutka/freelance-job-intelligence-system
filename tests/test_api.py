from fastapi.testclient import TestClient

from freelance_job_intelligence_system.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_jobs_endpoint_returns_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.json()) >= 8


def test_jobs_endpoint_filters_by_min_score():
    response = client.get("/jobs?min_score=80")
    assert response.status_code == 200
    assert all(item["score"] >= 80 for item in response.json())


def test_job_detail_endpoint_returns_one_job():
    jobs = client.get("/jobs").json()
    response = client.get(f"/jobs/{jobs[0]['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == jobs[0]["id"]


def test_missing_job_returns_404():
    response = client.get("/jobs/not-found")
    assert response.status_code == 404


def test_summary_endpoint_returns_market_metrics():
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    assert response.json()["total_jobs"] >= 8


def test_skills_endpoint_returns_skill_rows():
    response = client.get("/analytics/skills")
    assert response.status_code == 200
    assert "skill" in response.json()[0]


def test_alert_endpoint_returns_message():
    response = client.get("/alerts/top")
    assert response.status_code == 200
    assert "Job market intelligence alert" in response.json()["message"]
