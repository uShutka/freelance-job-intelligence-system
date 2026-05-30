import pandas as pd

from freelance_job_intelligence_system.services.parser import extract_location
from freelance_job_intelligence_system.services.relevance_engine import score_relevance


def enrich_jobs(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    enriched["description"] = enriched["description"].fillna("")
    enriched["title"] = enriched["title"].fillna("")
    scores = enriched.apply(lambda row: score_relevance(row["title"], row["description"]), axis=1)
    enriched["score"] = [score.score for score in scores]
    enriched["level"] = [score.level for score in scores]
    enriched["hourly_rate"] = [score.hourly_rate for score in scores]
    enriched["skills"] = [score.skills for score in scores]
    enriched["score_reasons"] = [score.reasons for score in scores]
    enriched["location"] = enriched.apply(lambda row: extract_location(f"{row['title']} {row['description']}"), axis=1)
    return enriched.sort_values(["score", "hourly_rate"], ascending=[False, False], na_position="last").reset_index(drop=True)
