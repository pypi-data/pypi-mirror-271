import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

from studcamp_yandex_hse.processing.embedder.base_embedder import BaseEmbeddingModel
from studcamp_yandex_hse.processing.ranker.base_ranker import BaseRanker


class MaxDistanceRanker(BaseRanker):
    """
    A class for ranking embeddings based on the maximum distance towards other words embeddings.
    """

    def __init__(self, embedding_model: BaseEmbeddingModel, distance_metric: str = "cosine"):
        super().__init__(embedding_model)
        self.distance_metric = distance_metric

    def get_ranked_embedding(
        self,
        text_embedding: np.ndarray,
        embeddings: np.ndarray,
    ) -> np.ndarray[int]:
        """
        Ranking embeddings based on their maximum distance to other embeddings.
        :param text_embedding: embedding of the whole text
        :param embeddings: embeddings of each word in the text
        :return: indices of embeddings sorted by their distance to other words
        """
        distances = pairwise_distances(embeddings, metric=self.distance_metric).mean(axis=1)
        top_n_indices = (-distances).argsort()
        return top_n_indices
