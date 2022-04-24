import uuid
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.loan.loan_type import LoanType
from smarttesting.order.loan_order_service import (
    LoanOrderService,
    MongoDbDao,
    PostgresDao,
)
from smarttesting.order.promotion import Promotion


@pytest.mark.homework(reason="Na pewno możemy popracować nad czytelnościa tych testów")
class TestLoanOrderService:
    def test_not_a_student(self) -> None:
        service = LoanOrderService(None, None)  # type: ignore

        with pytest.raises(ValueError, match="Cannot order student loan"):
            service.student_loan_order(
                Customer(
                    uuid.uuid4(),
                    Person("A", "B", date.today(), Gender.FEMALE, "1234567890"),
                )
            )

    def test_student(self) -> None:
        customer = Customer(
            uuid.uuid4(), Person("A", "B", date.today(), Gender.FEMALE, "1234567890")
        )
        customer.student()
        mongodb_dao = Mock(
            MongoDbDao, get_promotion_discount=Mock(return_value=Decimal("100"))
        )
        service = LoanOrderService(Mock(PostgresDao), mongodb_dao)
        student_loan_order = service.student_loan_order(customer)
        assert student_loan_order.type == LoanType.STUDENT
        assert student_loan_order.promotions[0] == Promotion(
            "Student Promo", Decimal("100")
        )
        assert student_loan_order.commission == Decimal("200")
        assert student_loan_order.amount == Decimal("500")
