from typing import List

from studcamp_yandex_hse.models.attention_based_model.attention_extractor import MBartTokenAttentionLevelExtractor
from studcamp_yandex_hse.models.base_extractor import BaseExtractor
from studcamp_yandex_hse.processing.normalizers import NormalizersPipe, PunctDeleter, StopwordsDeleter


class AttentionBasedTagger(BaseExtractor):
    """
    A class for extracting tags based on the attention weights of tokens in the input text.
    """

    def __init__(self):
        self.normalizer_pipe = NormalizersPipe(
            [
                StopwordsDeleter("russian"),
                PunctDeleter(),
            ]
        )
        self.attention_extractor = MBartTokenAttentionLevelExtractor()

    def extract(self, text: str, top_n: int) -> List[str]:
        """
        Main method to extract tags from text.
        :param text: source text
        :param top_n: parameter for the number of tags to extract
        :return: tags extracted from the text
        """
        clear_text = self.normalizer_pipe.normalize(text)

        top_bigrams = self.attention_extractor.get_top_bigrams_by_token_attention(clear_text, top_k=30)

        key_phrases = [word for word, attention in top_bigrams]
        top_keywords = key_phrases[:top_n]

        return top_keywords
