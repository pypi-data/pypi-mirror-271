from abc import ABC, abstractmethod
from typing import List

import spacy

import pandas as pd
from .errors import ProcessingError


class BaseTextProcessor(ABC):
    def __init__(self, pipeline: str = None):
        super().__init__()
        self.nlp = None
        if pipeline:
            try:
                self.nlp = spacy.load(pipeline)
            except OSError as err:
                message = (
                    "You don't seem to have installed the spacy "
                    f"pipeline {pipeline}. See https://spacy.io/models"
                )
                raise ProcessingError(message) from err
        self.text = ''
        self.doc = None
        self.sequences = []
        self.chunks = []
        self.n_tokens = []
        self.segments = []
        self.dataframe = pd.DataFrame([])

    @abstractmethod
    def split(self, text: str) -> List[str]:
        pass

    @abstractmethod
    def to_chunks(self, text: str, model: str) -> List[str]:
        pass

    @abstractmethod
    def group_by_semantics(self, text: str, model: str) -> pd.DataFrame:
        pass
