import pandas as pd

from freelance_job_intelligence_system.collectors.base import BaseCollector
from freelance_job_intelligence_system.config import default_jobs_path


class CSVJobCollector(BaseCollector):
    source_name = "csv"

    def __init__(self, path=None):
        self.path = path or default_jobs_path()

    def collect(self) -> pd.DataFrame:
        frame = pd.read_csv(self.path)
        frame["source"] = frame["source"].fillna(self.source_name)
        return frame
