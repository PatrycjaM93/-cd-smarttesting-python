import abc
from datetime import date
from decimal import Decimal

from smarttesting.order.promotion import Promotion


class PostgresAccessor(abc.ABC):
    """Interfejs służący do komunikacji z relacyjną bazą danych.

    Posłuży nam do przykładów zastosowania mocków i weryfikacji interakcji.
    """

    @abc.abstractmethod
    def update_promotion_statistics(self, promotion_name: str) -> None:
        pass

    @abc.abstractmethod
    def update_promotion_discount(
        self, promotion_name: str, new_discount: Decimal
    ) -> None:
        pass

    @abc.abstractmethod
    def get_valid_promotions_for_date(self, a_date: date) -> list[Promotion]:
        pass
