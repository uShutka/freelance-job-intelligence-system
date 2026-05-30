import pandas as pd


class JobRepository:
    def __init__(self, jobs: pd.DataFrame):
        self.jobs = jobs.copy()

    def list_jobs(self, min_score: int | None = None) -> pd.DataFrame:
        if min_score is None:
            return self.jobs.copy()
        return self.jobs[self.jobs["score"] >= min_score].copy()

    def get_job(self, job_id: str) -> dict[str, object] | None:
        row = self.jobs[self.jobs["id"].astype(str) == str(job_id)]
        if row.empty:
            return None
        return row.iloc[0].to_dict()
