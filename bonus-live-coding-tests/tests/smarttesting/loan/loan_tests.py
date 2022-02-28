from datetime import date
from decimal import Decimal
from typing import ClassVar

from freezegun import freeze_time
from smarttesting.loan.loan import Loan
from smarttesting.order.promotion import Promotion
from tests.smarttesting.loan.factories import build_loan_order


class TestLoan:
    AMOUNT: ClassVar = Decimal("3000")
    INTEREST_RATE: ClassVar = Decimal("5")
    COMMISSION: ClassVar = Decimal("200")

    @freeze_time()  # to make sure it won't fail when executed at midnight ;)
    def test_creates_loan(self) -> None:
        loan_order = build_loan_order(
            amount=self.AMOUNT,
            interest_rate=self.INTEREST_RATE,
            commission=self.COMMISSION,
        )

        loan = Loan.opened_today(loan_order, 6)

        assert loan.loan_opened_date == date.today()
        assert loan.number_of_installments == 6
        assert loan.amount == Decimal("3350.00")

    def test_calculates_installment_amount(self) -> None:
        loan_order = build_loan_order(
            amount=self.AMOUNT,
            interest_rate=self.INTEREST_RATE,
            commission=self.COMMISSION,
        )

        loan_installment = Loan.opened_today(loan_order, 6).installment_amount

        assert loan_installment == Decimal("558.33")

    def test_applies_promotion_discount(self) -> None:
        loan_order = build_loan_order(
            amount=self.AMOUNT,
            interest_rate=self.INTEREST_RATE,
            commission=self.COMMISSION,
            promotions=[
                Promotion("Test 10", Decimal("10")),
                Promotion("test 20", Decimal("20")),
            ],
        )

        loan = Loan.opened_today(loan_order, 6)

        assert loan.amount == Decimal("3320.00")
        assert loan.installment_amount == Decimal("553.33")

    def test_applies_fixed_discount_if_promotion_discount_sum_higher_than_threshold(
        self,
    ) -> None:
        loan_order = build_loan_order(
            amount=Decimal("2000"),
            interest_rate=Decimal("5"),
            commission=Decimal("300"),
            promotions=[
                Promotion("61", Decimal("61")),
                Promotion("300", Decimal("300")),
            ],
        )

        # Base amount: 2400
        loan = Loan.opened_today(loan_order, 6)

        assert loan.amount == Decimal("2040.00")
