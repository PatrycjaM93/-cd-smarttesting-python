from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from smarttesting.order.loan_order import LoanOrder


@dataclass
class LoanOrderAssert:
    """AssertObject pattern demo."""

    _loan_order: LoanOrder

    def registered_today(self) -> "LoanOrderAssert":
        assert self._loan_order.order_date == date.today()
        return self

    def has_promotion(self, promotion_name: str) -> "LoanOrderAssert":
        assert [
            promo
            for promo in self._loan_order.promotions
            if promo.name == promotion_name
        ]
        return self

    def has_only_one_promotion(self) -> "LoanOrderAssert":
        self.has_promotion_len(1)
        return self

    def has_promotion_len(self, number: int) -> "LoanOrderAssert":
        assert len(self._loan_order.promotions) == number
        return self

    def first_promotion_has_discount_value(self, number: Decimal) -> "LoanOrderAssert":
        assert self._loan_order.promotions[0].discount == number
        return self

    def student_loan_order(self) -> "LoanOrderAssert":
        return (
            self.registered_today()
            .has_promotion("Student Promo")
            .has_only_one_promotion()
            .first_promotion_has_discount_value(Decimal("10"))
        )
