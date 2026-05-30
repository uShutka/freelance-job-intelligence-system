from collections import Counter

import pandas as pd


def source_summary(jobs: pd.DataFrame) -> pd.DataFrame:
    return jobs.groupby("source", as_index=False).agg(jobs=("id", "count"), average_score=("score", "mean"), average_rate=("hourly_rate", "mean"))


def skill_trends(jobs: pd.DataFrame) -> pd.DataFrame:
    counts = Counter(skill for skills in jobs["skills"] for skill in skills)
    return pd.DataFrame([{"skill": skill, "jobs": count} for skill, count in counts.most_common()])


def level_distribution(jobs: pd.DataFrame) -> pd.DataFrame:
    return jobs.groupby("level", as_index=False).agg(jobs=("id", "count"), average_score=("score", "mean"))


def rate_by_skill(jobs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in jobs.dropna(subset=["hourly_rate"]).iterrows():
        for skill in row["skills"]:
            rows.append({"skill": skill, "hourly_rate": row["hourly_rate"]})
    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=["skill", "average_rate"])
    return frame.groupby("skill", as_index=False)["hourly_rate"].mean().rename(columns={"hourly_rate": "average_rate"}).sort_values("average_rate", ascending=False)


def market_summary(jobs: pd.DataFrame) -> dict[str, object]:
    top = jobs.sort_values("score", ascending=False).head(1).iloc[0]
    return {
        "total_jobs": int(len(jobs)),
        "average_score": float(jobs["score"].mean()),
        "average_hourly_rate": float(jobs["hourly_rate"].dropna().mean()),
        "remote_share": float((jobs["location"] == "remote").mean()),
        "top_job_title": top["title"],
        "top_job_score": int(top["score"]),
    }
