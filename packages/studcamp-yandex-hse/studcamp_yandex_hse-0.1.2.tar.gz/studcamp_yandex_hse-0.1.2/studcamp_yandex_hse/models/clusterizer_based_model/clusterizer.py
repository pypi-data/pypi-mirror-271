import numpy as np
from sklearn.cluster import DBSCAN

from studcamp_yandex_hse.models.base_extractor import BaseExtractor
from studcamp_yandex_hse.models.clusterizer_based_model.faiss import FaissKeywordExtractor
from studcamp_yandex_hse.processing.embedder import FastTextEmbedder
from studcamp_yandex_hse.processing.normalizers import NormalizersPipe, NounsKeeper, PunctDeleter, StopwordsDeleter


class DBSCANFaissTagger(BaseExtractor):
    """
    A class for extracting tags based on the clusterization idea
    """

    def __init__(self, ft_emb_model) -> None:
        self.normalizer = NormalizersPipe(
            [
                PunctDeleter(),
                StopwordsDeleter("russian"),
                NounsKeeper("russian"),
            ],
            final_split=True,
        )
        self.embedder = ft_emb_model
        self.faiss = FaissKeywordExtractor(ft_emb_model)

    def extract(self, text: str, top_n: int) -> list:
        """
        Main method to extract tags from text.
        :param text: source text
        :param top_n: parameter for the number of tags to extract
        :return: tags extracted from the text
        """
        splitted_text = self.normalizer.normalize(text)
        vectorized_nouns = self.embedder(splitted_text)

        labels, samples = None, None
        for parameter in range(2, int(np.sqrt(vectorized_nouns.shape[0]))):
            dbscan = DBSCAN(min_samples=parameter, eps=0.1, metric="cosine")
            model = dbscan.fit(vectorized_nouns)
            labels = model.labels_

            if len(set(labels) - {-1}) < top_n:
                break

        clusters = {}
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

        for cluster_id in range(n_clusters):
            points_in_cluster = vectorized_nouns[labels == cluster_id]
            clusters[cluster_id] = points_in_cluster

        centroids = [np.mean(embeddings, axis=0) for key, embeddings in clusters.items()]
        tags = self.faiss.get_tags(centroids)
        return tags
