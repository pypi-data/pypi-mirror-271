import inspect
import logging
import asyncio
from pathlib import Path
from typing import Coroutine

import pandas as pd

from openai import APIError
from openai import AsyncOpenAI

from aigents.constants import (
    MODELS, EMBEDDINGS_COLUMNS, MODELS_EMBEDDING, MAX_TOKENS
)
from aigents.settings import DEBUG
from aigents.utils import number_of_tokens

from .nlp.processors import naive_text_to_embeddings_async
from .nlp.errors import ProcessingError
from .base import BaseContext
from .errors import ContextError
from .errors import APIContextError
from .utils import distances_from_embeddings, to_embeddings_async


logger = logging.getLogger('standard')


class Context(BaseContext):
    """
    A class representing a context for contextual chat applications.

    Parameters:
    - text (str, optional): The initial text for the context.
    - model (str, optional): The model to use for generating embeddings.
    - max_tokens (int, optional): The maximum number of tokens per chunk.
    - openai_key (str, optional): The OpenAI API key.
    - openai_organization (str, optional): The OpenAI organization.
    - **kwargs: Additional keyword arguments.

    Methods:
    - generate_embeddings(source, model=MODELS[1], max_tokens=None) ->
        pd.DataFrame:
        Generate embeddings from a source.

        Parameters:
        - source (str | pd.DataFrame | Path | dict): The source data for
            generating embeddings.
        - model (str, optional): The model to use for generating embeddings.
        - max_tokens (int, optional): The maximum number of tokens per chunk.

        Returns:
        pd.DataFrame: The generated embeddings.

    - generate_context(question, max_length=1800) -> str:
        Generate a context based on a question.

        Parameters:
        - question (str): The question for generating the context.
        - max_length (int, optional): The maximum length of the context.

        Returns:
        str: The generated context.

    """
    def __init__(self,
                 text: str = None,
                 max_tokens: int = 500,
                 api_key=None,
                 organization=None,
                 **kwargs):
        super().__init__(
            text=text,
            max_tokens=max_tokens,
            api_key=api_key,
            organization=organization,
            **kwargs
        )
        self.question_embedding = None
        self.pipeline: str = None
        self.embeddings_generator: str = None
        self.embedding_model: str = None

    async def generate_embeddings(
            self,
            source: str | pd.DataFrame | Path | dict = None,
            model: str = MODELS[0],
            max_tokens: int = None,  # tokens per chunk
            embeddings_generator: str | Coroutine = naive_text_to_embeddings_async,
            **kwargs
    ) -> pd.DataFrame:
        """Generate embeddings dataframe from source.

        Dataframe columns can be found at:
            context_files.constants.EMBEDDINGS_COLUMNS
        Which are
            - 'chunks': sentences of the text. The size of chunks in tokens
                measure is limited by `max_tokens`.
            - 'n_tokens': number of tokens of the corresponding chunk of text.
            - 'embeddings': vector encoding of the meaning of the word, used
                to generate the context based on a question or prompt. Prefer
                create embeddings using the language model's api suggestion.
                In case of Openai's, it is the Ada model, which will be used
                if `embeddings_generator` is provided as a string. But you can
                provide your own embedding generator, the only requirement is
                that is must be a coroutine,

        NOTE: `embeddings_generator`: if str, it must be an installed
            spacy model pipeline (see https://github.com/explosion/spacy-models/releases)
            and a model (either `openai`or `gemini`), both separated by a comma.
            Example: "en_core_web_md,openai"
            
        
        Parameters
        ----------
        source : str | pd.DataFrame | Path | dict, optional
            The source data from which embeddings will be generated. It can be
            provided as a string (text data), a pandas DataFrame, a Path to a
            parquet file containing embeddings, or a dictionary containing
            'chunks', 'n_tokens', and 'embeddings' keys. If not provided,
            defaults to the text stored in the instance (`self.text`).
        model : str, optional
            The language model to use for generating embeddings. Defaults to
            the second model in the available models list:
                `context_chat.agents.constants.MODELS`
        max_tokens : int, optional
            The maximum number of tokens per chunk of text. This parameter
            limits the size of the chunks when breaking down the input text.
        embeddings_generator : str | Callable, obligatory if `source` is str
            The embeddings generator to use. If a string, it must correspond
            to an installed spaCy model pipeline
            (see https://github.com/explosion/spacy-models/releases).
            If a callable, it must be a coroutine that generates embeddings.
            Defaults to None.
        **kwargs
            Additional keyword arguments to be passed to the embeddings
            generator.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the generated embeddings with columns:
                - 'chunks': Sentences of the text, limited by `max_tokens`.
                - 'n_tokens': Number of tokens in the corresponding chunk.
                - 'embeddings': Vector encoding of the meaning of the words,
                  used for generating context based on a question or prompt.

        Raises
        ------
        ContextError
            If the keys of the provided `source` dictionary do not match
            `context_files.constants.EMBEDDINGS_COLUMNS`, or if the items
            in the dictionary do not have the same length, or if `source` type
            `str` and `embeddings_generator`is not provided.
        TypeError
            If the provided `source` is not a DataFrame, Path object, string,
            or dictionary.
        APIError
            If an error occurs while using the OpenAI API to generate
            embeddings.
        APIContextError
            If there is an issue with the OpenAI API, such as an error message
            or code returned during the generation process.
        """
        if source is None:
            source = self.text
        if max_tokens is None:
            max_tokens = self.max_tokens
        
        if isinstance(source, pd.DataFrame):
            self.embeddings = source
        elif isinstance(source, Path):
            self.embeddings = pd.read_parquet(source, engine='pyarrow')
        elif isinstance(source, dict):
            if not set(EMBEDDINGS_COLUMNS).issubset(set(source.keys())):
                raise ContextError(
                    f"Keys of `source` must contain: {','.join(EMBEDDINGS_COLUMNS)}"
                )
            lengths = list(map(len, source.values()))
            if not all(x == lengths[0] for x in lengths[1:]):
                raise ContextError(
                    "Items of `source`must have the same length"
                )
            self.json = source
            self.embeddings = pd.DataFrame(source)
            return self.embeddings
        else:
            if not isinstance(source, str):
                raise TypeError(
                    '`source` must either be a DataFrame, '
                    'Path object, a string or a dict'
                )
            try:
                if isinstance(embeddings_generator, str):
                    try:
                        (
                            self.pipeline, self.embedding_model
                        ) = embeddings_generator.rsplit(maxsplit=2, sep=',')
                    except ValueError as err:
                        if 'unpack' in str(err):
                            message = (
                                "`embeddings_generator` must be a spacy "
                                "pipeline and a model (either `openai`or "
                                "`gemini`) separated by a comma"
                            )
                            message = f"{message}: {err.message}"
                            raise ContextError(message) from err
                    try:
                        self.embeddings = await to_embeddings_async(
                            source,
                            self.pipeline.strip(),
                            max_tokens=max_tokens,
                            embedding_model=self.embedding_model.strip()
                        )
                    except ProcessingError as err:
                        raise ContextError(err.message) from err
                elif inspect.iscoroutinefunction(embeddings_generator):
                    self.embeddings = await embeddings_generator(
                        source,
                        model=model,
                        max_tokens=max_tokens,
                        **kwargs
                    )
                else:
                    raise ContextError(
                        '`embeddings_generator` must be a coroutine or a str '
                        'corresponding to a spacy pipeline model (either `openai`or '
                        '`gemini`) separated by a comma'
                    )
            except APIError as err:
                message = (
                    f"OpenAI's error: {err.message} "
                    f"(code {err.code}) "
                    "Try again in a few minutes."
                )
                raise APIContextError(message) from err
        self.json = self.to_json()
        return self.embeddings

    async def generate_context(self,
                               question: str,
                               data: pd.DataFrame = None,
                               max_length: int = 1800,
                               pipeline: str = None,
                               embedding_model: str = None,
                               prefix: str = None) -> str:
        results = []
        current_length = 0
        if data is None:
            data = self.embeddings
        if pipeline is None:
            pipeline = self.pipeline
            if pipeline is None:
                pipeline = 'en_core_web_md'
        if embedding_model is None:
            embedding_model = self.embedding_model
            if embedding_model is None:
                embedding_model = 'openai'

        max_tokens = MAX_TOKENS[2][1]  # gtp4
        if 'gemini' in embedding_model.lower():
            max_tokens = MAX_TOKENS[-2][1]  # gemini
        data_question_embedding = await to_embeddings_async(
            question,
            pipeline,
            max_tokens=max_tokens,
            embedding_model=embedding_model
        )
        question_embedding = data_question_embedding.iloc[0]['embeddings']
        self.question_embedding = question_embedding
        data['distances'] = distances_from_embeddings(
            question_embedding,
            data['embeddings'].values,
            distance_metric='cosine'
        )

        if prefix is None:
            prefix = '*'
        for _, row in data.sort_values('distances', ascending=True).iterrows():

            results.append(row["chunks"].replace('\n', ' '))

            current_length = number_of_tokens("\n-".join(results))

            if current_length > max_length:
                if len(results) > 1:
                    results.pop()
                break

        context = f"{prefix} {results[0]}"
        context += "".join(
            [f"\n{prefix} {result}" for result in results[1:]]
        )
        length = number_of_tokens(context)
        if DEBUG:
            logger.debug(
                'Context created. Length: %s', length
            )
        # Return the context
        return context


async def embeddings_from_dict(source: dict,
                               max_tokens: int = None,  # tokens per chunk
                               embeddings_generator: str | Coroutine = None,) -> pd.DataFrame:
    contexter = Context()
    dataframe = None
    tasks = []
    for text in source.values():
        tasks.append(
            contexter.generate_embeddings(
                source=text,
                max_tokens=max_tokens,
                embeddings_generator=embeddings_generator
            )
        )

    results = await asyncio.gather(*tasks)
    for reference, result in zip(source, results):
        if dataframe is None:
            dataframe = result
            dataframe['reference'] = dataframe.shape[0]*[reference]
            continue
        result['reference'] = result.shape[0]*[reference]
        dataframe = pd.concat([dataframe, result], ignore_index=True)
    return dataframe
        