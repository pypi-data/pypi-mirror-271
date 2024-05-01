from collections import Counter
from itertools import chain

import numpy as np

from studcamp_yandex_hse.models.base_extractor import BaseExtractor
from studcamp_yandex_hse.models.rake_based_model.keyphrases_extractor import RakeKeyphrasesExtractor
from studcamp_yandex_hse.processing.embedder import FastTextEmbedder
from studcamp_yandex_hse.processing.normalizers import NormalizersPipe, NounsKeeper, PunctDeleter, StopwordsDeleter
from studcamp_yandex_hse.processing.ranker import MaxDistanceRanker


class TagsExtractor(BaseExtractor):
    """
    A class used to extract tags from text based on keyword extraction, normalization, and ranking.

    Args:
        ft_emb_model (FastTextEmbedder): FastText model used for word embeddings.
        language (str): Language used for text processing. Defaults to 'russian'.
        min_cnt_keyword (int): Minimum count for a keyword to be included in the tag results.

    Attributes:
        extractor (RakeKeyphrasesExtractor): Keyword extractor configured for specific language.
        normalizer (NormalizersPipe): Pipeline of text normalizers.
        ranker (MaxDistanceRanker):
            Ranking mechanism for keywords based on distance metrics in embedding space.
        min_cnt_keyword (int):
            Minimum occurrence threshold for a word to be considered as a potential tag.

    Methods:
        extract(text: str, top_n: int) -> np.ndarray:
            Extracts and returns top_n tags from the given text.
    """

    def __init__(
        self,
        ft_emb_model: FastTextEmbedder,
        language: str = "russian",
        min_cnt_keyword: int = 2,
    ) -> None:
        self.extractor = RakeKeyphrasesExtractor(language=language)
        self.normalizer = NormalizersPipe(
            [
                PunctDeleter(),
                StopwordsDeleter(language),
                NounsKeeper(language),
            ],
            final_split=True,
        )
        self.ranker = MaxDistanceRanker(ft_emb_model)
        self.min_cnt_keyword = min_cnt_keyword

    def extract(
        self,
        text: str,
        top_n: int,
    ) -> np.ndarray:
        """
        Extracts the top_n most relevant tags from the provided text.

        Args:
            text (str): The text from which to extract tags.
            top_n (int): The number of tags to extract.

        Returns:
            np.ndarray: An array of the top_n extracted tags.
        """
        keyphrases_with_scores = self.extractor.extract(text.lower())
        keyphrases = [text for _, text in keyphrases_with_scores]

        normalized_keyphrases = list(map(self.normalizer.normalize, keyphrases))
        normalized_words = list(chain(*normalized_keyphrases))

        most_co_occurring_words = np.array(
            [word for word, cnt in Counter(normalized_words).most_common(top_n) if cnt >= self.min_cnt_keyword]
        )

        keywords = self.ranker.get_top_n_keywords(normalized_words, most_co_occurring_words, top_n)

        return keywords
