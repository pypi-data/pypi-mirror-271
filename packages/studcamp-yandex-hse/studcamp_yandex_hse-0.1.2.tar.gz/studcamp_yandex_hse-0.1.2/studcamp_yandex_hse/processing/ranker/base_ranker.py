from abc import ABC, abstractmethod
from typing import List, Union

import numpy as np

from studcamp_yandex_hse.processing.embedder.base_embedder import BaseEmbeddingModel


class BaseRanker(ABC):
    """
    Base class for ranking embeddings based on their similarity to the text_embedding.
    """

    def __init__(self, embedding_model: BaseEmbeddingModel):
        self.embedding_model = embedding_model

    @abstractmethod
    def get_ranked_embedding(
        self,
        text_embedding: np.ndarray,
        embeddings: np.ndarray,
    ) -> np.ndarray[int]:
        """
        Ranking embeddings based on their similarity to the text_embedding.
        :param text_embedding: embedding of the whole text
        :param embeddings: embeddings of each word in the text
        :return: indices of embeddings sorted by their similarity to the text_embedding
        """

    def get_top_n_keywords(
        self,
        text: Union[str, List[str]],
        words: np.ndarray[str],
        top_n: int,
    ) -> List[str]:
        """
        Extracting top_n keywords from the text based on embeddings.
        :param text: source text
        :param words: words of the source text
        :param top_n: parameter defining the number of keywords to extract
        :return: list of top_n keywords
        """
        embeddings = self.embedding_model(words)
        if len(embeddings) == 0:
            return []

        text_embedding = self.embedding_model.get_sentence_emb(" ".join(text))
        top_n_indices = self.get_ranked_embedding(text_embedding, embeddings)
        top_n_keywords: List[str] = words[top_n_indices][:top_n].tolist()

        return top_n_keywords
