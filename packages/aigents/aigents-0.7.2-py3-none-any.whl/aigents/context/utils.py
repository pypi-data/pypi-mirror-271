from typing import List
from scipy import spatial
from pandas import DataFrame

from .nlp.processors import TextProcessor
from .nlp.constants import PIPE_LINES



def to_embeddings(
        text: str,
        pipeline: str = PIPE_LINES[-1],
        max_tokens=120,
        threshold=0.8,
        embedding_model='openai',
) -> DataFrame:
    return TextProcessor(pipeline=pipeline).embeddings(
        text,
        max_tokens=max_tokens,
        threshold=threshold,
        embedding_model=embedding_model,
    )


async def to_embeddings_async(
        text: str,
        pipeline: str = PIPE_LINES[-1],
        max_tokens=120,
        threshold=0.8,
        embedding_model='openai',
) -> DataFrame:
    return await TextProcessor(pipeline=pipeline).async_embeddings(
        text,
        max_tokens=max_tokens,
        threshold=threshold,
        embedding_model=embedding_model,
    )


def to_embeddings_pt(text: str,
                     max_tokens=120,
                     threshold=0.8,
                     embedding_model='openai',) -> DataFrame:
    return to_embeddings(
        text,
        pipeline=PIPE_LINES[0],
        max_tokens=max_tokens,
        threshold=threshold,
        embedding_model=embedding_model,
    )


async def to_embeddings_pt_async(text: str,
                                 max_tokens=120,
                                 threshold=0.8,
                                 embedding_model='openai',) -> DataFrame:
    return await to_embeddings_async(
        text,
        pipeline=PIPE_LINES[0],
        max_tokens=max_tokens,
        threshold=threshold,
        embedding_model=embedding_model,
    )

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """
    Calculate distances between a query embedding and a list of embeddings.

    Parameters:
    - query_embedding (List[float]): The embedding of the query.
    - embeddings (List[List[float]]): A list of embeddings.
    - distance_metric (str, optional): The distance metric to use.

    Returns:
    List[List]: A list of distances.
    """
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances
