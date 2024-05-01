from abc import ABC, abstractmethod


class BaseNormalizer(ABC):
    """
    Base class for text normalizers.
    """

    @abstractmethod
    def normalize(self, text: str) -> str:
        """
        Normalize text.
        :param text: source text
        :return: normalized text in some way
        """
