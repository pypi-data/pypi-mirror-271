import string

from studcamp_yandex_hse.processing.normalizers.base_normalizer import BaseNormalizer


class PunctDeleter(BaseNormalizer):
    """
    A class for deleting punctuation from the text.
    """

    def __init__(self) -> None:
        self.punct = string.punctuation
        self.punct = self.punct.replace("-", "")

    def normalize(self, text: str) -> str:
        """
        Normalize text by deleting punctuation from text.
        :param text: source text
        :return: normalized text without punctuation
        """
        clear_text = text
        for punctuation in self.punct:
            clear_text = clear_text.replace(punctuation, "")

        return clear_text
