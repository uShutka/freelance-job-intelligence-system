import pandas as pd

from freelance_job_intelligence_system.collectors.base import BaseCollector


class MockRedditCollector(BaseCollector):
    source_name = "reddit"

    def collect(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": "rd-001",
                    "title": "Remote Python automation for price monitoring",
                    "description": "Need Python Playwright scraping, PostgreSQL storage, FastAPI API and Telegram alerts. Remote, $55 hourly.",
                    "source": self.source_name,
                    "posted_at": "2026-05-01",
                    "url": "https://reddit.example/jobs/rd-001",
                },
                {
                    "id": "rd-002",
                    "title": "Senior-only enterprise data architect",
                    "description": "Senior only, 8+ years, big enterprise governance. Mostly meetings, $80 hourly.",
                    "source": self.source_name,
                    "posted_at": "2026-05-03",
                    "url": "https://reddit.example/jobs/rd-002",
                },
            ]
        )


class MockHackerNewsCollector(BaseCollector):
    source_name = "hackernews"

    def collect(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "id": "hn-001",
                    "title": "FastAPI ETL dashboard contract",
                    "description": "Remote contractor for FastAPI, pandas, SQL, PostgreSQL, Streamlit dashboard. $60/hr.",
                    "source": self.source_name,
                    "posted_at": "2026-05-04",
                    "url": "https://news.ycombinator.example/item?id=hn-001",
                }
            ]
        )
