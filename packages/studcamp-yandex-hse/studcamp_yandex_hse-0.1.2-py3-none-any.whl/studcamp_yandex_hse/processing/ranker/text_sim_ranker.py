import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from studcamp_yandex_hse.processing.ranker.base_ranker import BaseRanker


class TextSimRanker(BaseRanker):
    """
    A class for ranking embeddings based on their similarity to the text_embedding.
    """

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
        similarity_scores = np.array([cosine_similarity([text_embedding], [vector])[0][0] for vector in embeddings])
        top_n_indices = (-similarity_scores).argsort()
        return top_n_indices
