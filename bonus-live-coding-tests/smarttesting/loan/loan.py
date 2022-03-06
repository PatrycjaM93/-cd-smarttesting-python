from datetime import date
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from uuid import UUID, uuid4

from smarttesting.loan.validation.loan_validation_exception import (
    LoanValidationException,
)
from smarttesting.order.loan_order import LoanOrder


class Loan:
    _loan_opened_date: date
    _amount: Decimal
    _number_of_installments: int
    _installment_amount: Decimal
    _uuid: UUID

    def __init__(
        self, loan_opened_date, loan_order: LoanOrder, number_of_installments: int
    ) -> None:
        self._loan_opened_date = loan_opened_date
        self._amount = self._calculate_loan_amount(loan_order)
        self._number_of_installments = number_of_installments
        self._installment_amount = (
            self._amount / self._number_of_installments
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        self._uuid = uuid4()

    @classmethod
    def opened_today(cls, loan_order: LoanOrder, number_of_installments: int) -> "Loan":
        return Loan(date.today(), loan_order, number_of_installments)

    def _calculate_loan_amount(self, loan_order: LoanOrder) -> Decimal:
        assert loan_order.amount
        assert loan_order.interest_rate
        assert loan_order.commission
        self._validate_element(loan_order.amount)
        self._validate_element(loan_order.interest_rate)
        self._validate_element(loan_order.commission)
        interest_factor = Decimal("1") + (
            loan_order.interest_rate / Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        base_amount = loan_order.amount * interest_factor + loan_order.commission
        return self._apply_promotion_discount(loan_order, base_amount)

    def _apply_promotion_discount(
        self, loan_order: LoanOrder, base_amount: Decimal
    ) -> Decimal:
        discount_sum = sum(
            [promo.discount for promo in loan_order.promotions], start=Decimal("0")
        )
        fifteen_percent_of_base_sum = (base_amount * Decimal("0.15")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        if fifteen_percent_of_base_sum <= discount_sum:
            return base_amount - fifteen_percent_of_base_sum
        else:
            return base_amount - discount_sum

    def _validate_element(self, element_amount: Decimal) -> None:
        if element_amount < Decimal("1"):
            raise LoanValidationException

    @property
    def installment_amount(self) -> Decimal:
        return self._installment_amount

    @property
    def uuid(self):
        return self._uuid

    @property
    def loan_opened_date(self) -> date:
        return self._loan_opened_date

    @property
    def number_of_installments(self) -> int:
        return self._number_of_installments

    @property
    def amount(self) -> Decimal:
        return self._amount
