from freelance_job_intelligence_system.pipeline import run_pipeline
from freelance_job_intelligence_system.services.parser import extract_rate as parser_extract_rate
from freelance_job_intelligence_system.services.parser import extract_skills as parser_extract_skills
from freelance_job_intelligence_system.services.relevance_engine import score_relevance


def load_jobs():
    return run_pipeline()


def extract_rate(text: str) -> int | None:
    return parser_extract_rate(text)


def extract_skills(text: str) -> list[str]:
    return parser_extract_skills(text)


def score_job(text: str) -> int:
    return score_relevance("", text).score


def run_demo():
    jobs = run_pipeline()
    return {"jobs": jobs, "top_jobs": jobs.head(5)}
