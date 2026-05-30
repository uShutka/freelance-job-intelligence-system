from abc import ABC, abstractmethod

import pandas as pd


class BaseCollector(ABC):
    source_name: str

    @abstractmethod
    def collect(self) -> pd.DataFrame:
        raise NotImplementedError
