from pathlib import Path

PROFILE_SKILLS = [
    "python",
    "fastapi",
    "postgresql",
    "sql",
    "pandas",
    "playwright",
    "selenium",
    "scraping",
    "automation",
    "docker",
    "streamlit",
    "telegram",
    "etl",
]

DATA_SKILLS = {"sql", "postgresql", "pandas", "etl", "dashboard", "analytics", "streamlit"}
AUTOMATION_SKILLS = {"automation", "scraping", "playwright", "selenium", "browser automation"}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_jobs_path() -> Path:
    return project_root() / "data" / "jobs.csv"
