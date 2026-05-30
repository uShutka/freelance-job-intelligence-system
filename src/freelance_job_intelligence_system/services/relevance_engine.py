from freelance_job_intelligence_system.config import AUTOMATION_SKILLS, DATA_SKILLS
from freelance_job_intelligence_system.models import ScoreBreakdown
from freelance_job_intelligence_system.services.parser import classify_level, extract_rate, extract_skills, is_remote


def score_relevance(title: str, body: str) -> ScoreBreakdown:
    text = f"{title} {body}"
    skills = extract_skills(text)
    skill_set = set(skills)
    level = classify_level(text)
    hourly_rate = extract_rate(text)
    reasons: list[str] = []
    score = 0

    if "python" in skill_set:
        score += 20
        reasons.append("Python match")
    if skill_set & AUTOMATION_SKILLS:
        score += 20
        reasons.append("Automation/scraping match")
    if skill_set & DATA_SKILLS:
        score += 15
        reasons.append("Data/analytics stack match")
    if "fastapi" in skill_set:
        score += 10
        reasons.append("FastAPI backend match")
    if "docker" in skill_set:
        score += 5
        reasons.append("Docker production setup")
    if is_remote(text):
        score += 10
        reasons.append("Remote-friendly")
    if hourly_rate:
        score += 10
        reasons.append("Rate detected")
        if hourly_rate < 25:
            score -= 10
            reasons.append("Low hourly rate penalty")
    if level == "senior":
        score -= 20
        reasons.append("Senior-only penalty")
    if level == "junior":
        score -= 5
        reasons.append("Junior-level penalty")

    return ScoreBreakdown(score=max(0, min(score, 100)), level=level, hourly_rate=hourly_rate, skills=skills, reasons=reasons)
