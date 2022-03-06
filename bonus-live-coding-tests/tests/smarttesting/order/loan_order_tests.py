from datetime import date
from decimal import Decimal
from uuid import uuid4

from smarttesting.customer.customer import Customer
from smarttesting.order.loan_order import LoanOrder
from tests.smarttesting.order.loan_order_tests_base import LoanOrderTestsBase


class LoanOrderTest(LoanOrderTestsBase):
    """Przykład testowania stanu."""

    def test_adds_manager_promo(self, customer: Customer) -> None:
        loan_order = LoanOrder(
            date.today(),
            customer,
            amount=Decimal("2000"),
            interest_rate=Decimal("5"),
            commission=Decimal("200"),
        )
        manager_uuid = uuid4()

        loan_order.add_manager_discount(manager_uuid)

        assert len(loan_order.promotions) == 1
        the_only_promotion = loan_order.promotions[0]
        assert str(manager_uuid) in the_only_promotion.name
        assert the_only_promotion.discount == Decimal("50")
