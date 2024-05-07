import json
import logging
from abc import ABC
from abc import abstractmethod
from pathlib import Path

import pandas as pd

from aigents.constants import MODELS, EMBEDDINGS_COLUMNS

DEBUG = True
logger = logging.getLogger('standard')


class BaseContext(ABC):
    def __init__(self,
                 text: str = None,
                 max_tokens: int = 500,
                 api_key=None,
                 organization=None,
                 **kwargs):
        
        self.text = text
        self.embeddings = pd.DataFrame([])
        self.json = "{}"
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.organization = organization

    def save_embeddings(
            self,
            path: str | Path = None,
    ):
        if self.embeddings is not None:
            self.embeddings.to_parquet(path, engine='pyarrow', index=False)
            return
        if DEBUG:
            logger.warning(
                'Embeddings weren\'t generated yet. Nothing to save.'
            )

    def to_json(self,):
        if self.embeddings is not None:
            data = json.loads(
                self.embeddings.to_json(
                    orient='table',
                    index=False,
                    force_ascii=False
                )
            )['data']
            self.json = {column: [] for column in self.embeddings.columns}
            for row in data:
                for key, value in row.items():
                    self.json[key].append(value)
            return self.json
        if DEBUG:
            logger.warning(
                'Embeddings weren\'t generated yet. Returning {}.'
            )
        return {}

    @abstractmethod
    async def generate_embeddings(
            self,
            source: str | pd.DataFrame | Path | dict,
            model: str = MODELS[0],
            max_tokens: int = None
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    async def generate_context(self, question: str, max_length=1800) -> str:
        pass

