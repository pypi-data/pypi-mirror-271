import faiss
import fasttext
import numpy as np


class FaissKeywordExtractor:
    """
    A class for extracting tags in a faster way using Faiss library.
    """

    def __init__(self, ft_emb_model) -> None:
        self.emb_model = ft_emb_model
        self.word_vectors = np.array([self.emb_model.ft_model[word] for word in self.emb_model.ft_model.get_words()])
        self.words = list(self.emb_model.ft_model.get_words())
        self.index = faiss.IndexFlatL2(self.word_vectors.shape[1])
        self.index.add(self.word_vectors.astype(np.float32))

    def find_closest(self, vec: np.ndarray) -> str:
        """
        Finds the closest word to the given vector.
        :param vec: word embedding
        :return: word
        """
        query_vector = vec.astype(np.float32)
        _, indices = self.index.search(query_vector.reshape(1, -1), 1)
        most_similar_word = self.words[indices[0][0]]
        return most_similar_word

    def get_tags(self, centroids: list) -> list:
        """
        Extracts tags from the given centroids.
        :param centroids: list of centroids
        :return: list of tags
        """
        tags = []
        for centroid in centroids:
            word = self.find_closest(centroid).split("_")[0]
            if len(word) <= 15:
                tags.append(word)

        return tags
