import logging

import pandas as pd

from freelance_job_intelligence_system.collectors.base import BaseCollector
from freelance_job_intelligence_system.collectors.csv_collector import CSVJobCollector
from freelance_job_intelligence_system.collectors.mock_collectors import MockHackerNewsCollector, MockRedditCollector
from freelance_job_intelligence_system.services.enrichment import enrich_jobs

logger = logging.getLogger(__name__)


def collect_jobs(collectors: list[BaseCollector] | None = None) -> pd.DataFrame:
    active_collectors = collectors or [CSVJobCollector(), MockRedditCollector(), MockHackerNewsCollector()]
    frames = []
    for collector in active_collectors:
        logger.info("Collecting jobs", extra={"source": collector.source_name})
        frames.append(collector.collect())
    return pd.concat(frames, ignore_index=True).drop_duplicates(subset=["id"])


def run_pipeline(collectors: list[BaseCollector] | None = None) -> pd.DataFrame:
    return enrich_jobs(collect_jobs(collectors))
