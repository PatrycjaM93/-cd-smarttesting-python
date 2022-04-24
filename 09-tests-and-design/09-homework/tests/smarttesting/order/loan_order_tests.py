import uuid
from datetime import date
from decimal import Decimal

from smarttesting.order.loan_order import LoanOrder
from tests.factories import CustomerFactory


class TestLoanOrder:
    def test_adds_manager_promo(self) -> None:
        loan_order = LoanOrder(date.today(), CustomerFactory.build())
        manager_uuid = uuid.uuid4()

        loan_order.add_manager_discount(manager_uuid)

        assert len(loan_order.promotions) == 1
        promo = loan_order.promotions[0]
        assert str(manager_uuid) in promo.name
        assert promo.discount == Decimal("50")
