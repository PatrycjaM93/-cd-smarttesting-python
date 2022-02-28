import abc
from decimal import Decimal


class MongoDbAccessor(abc.ABC):
    """Interfejs służący do komunikacji z dokumentową bazą danych.

    Posłuży nam do przykładów zastosowania stubów.
    """

    @abc.abstractmethod
    def get_promotion_discount(self, promotion_name: str) -> Decimal:
        pass

    @abc.abstractmethod
    def get_min_commission(self) -> Decimal:
        pass
