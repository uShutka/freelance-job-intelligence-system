import re
import pandas as pd
SKILLS = ["python", "fastapi", "postgresql", "selenium", "playwright", "pandas", "scraping", "docker"]
def load_jobs(path="data/jobs.csv"):
    return pd.read_csv(path)
def extract_skills(text: str) -> list[str]:
    lower = text.lower()
    return [skill for skill in SKILLS if skill in lower]
def extract_rate(text: str) -> int | None:
    match = re.search(r"\$(\d+)", text)
    return int(match.group(1)) if match else None
def score_job(text: str) -> int:
    skills = extract_skills(text)
    return len(skills) * 20 + (20 if "remote" in text.lower() else 0)
def enrich_jobs(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["skills"] = enriched["description"].apply(extract_skills)
    enriched["rate"] = enriched["description"].apply(extract_rate)
    enriched["score"] = enriched["description"].apply(score_job)
    return enriched.sort_values("score", ascending=False)
if __name__ == "__main__":
    print(enrich_jobs(load_jobs()).head())
