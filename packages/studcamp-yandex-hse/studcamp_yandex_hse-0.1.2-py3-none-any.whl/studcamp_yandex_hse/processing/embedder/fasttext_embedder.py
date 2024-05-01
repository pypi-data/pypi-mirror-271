import os
from typing import List, Union

import fasttext
import numpy as np

from studcamp_yandex_hse.processing.embedder.base_embedder import BaseEmbeddingModel


class FastTextEmbedder(BaseEmbeddingModel):
    """
    FastText embedder model.
    """

    def __init__(self, model_path: str = "./cc.ru.300.bin") -> None:
        abs_path = os.path.abspath(model_path)
        self.ft_model = fasttext.load_model(abs_path)

    def get_embeddings(self, words: np.ndarray[str]) -> np.ndarray[np.ndarray[float]]:
        """
        Returns embedding for each word in words.
        :param words: list of words
        :return: embeddings for each word
        """
        embeddings = np.array([np.array(self.ft_model[word]) for word in words])
        return embeddings

    def get_sentence_emb(self, text: Union[List[str], str]) -> np.ndarray[float]:
        """
        Returns embedding for full text
        :param text: source text
        :return: embedding for the whole text
        """
        emb = self.ft_model.get_sentence_vector(text)
        return emb
