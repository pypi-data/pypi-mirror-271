import nltk
from nltk.corpus import stopwords

from studcamp_yandex_hse.processing.normalizers.base_normalizer import BaseNormalizer
from studcamp_yandex_hse.processing.utils import languages


class StopwordsDeleter(BaseNormalizer):
    """
    A class for deleting stopwords from the text.
    """

    def __init__(self, language: str) -> None:
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words(language))

    def normalize(self, text: str) -> str:
        """
        Normalize text by deleting stopwords from text.
        :param text: source text
        :return: normalized text without stopwords
        """
        clear_text = []
        for word in text.split():
            if word.lower() not in self.stop_words and word != "":
                clear_text.append(word)

        return " ".join(clear_text)
