from typing import List, Union

from studcamp_yandex_hse.processing.normalizers.base_normalizer import BaseNormalizer


class NormalizersPipe:
    def __init__(self, normalizers: List[BaseNormalizer], final_split: bool = False) -> None:
        self.normalizers = normalizers
        self.final_split = final_split

    def normalize(self, text: str) -> Union[str, List[str]]:
        """
        Normalize text using a pipeline of normalizers.
        :param text: source text
        :return: normalized text with each normalizer specified in the pipeline
        """
        normalized_text = text
        for normalizer in self.normalizers:
            normalized_text = normalizer.normalize(normalized_text)

        if self.final_split:
            return normalized_text.split()

        return normalized_text
