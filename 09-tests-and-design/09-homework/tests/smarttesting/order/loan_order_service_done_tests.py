import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.loan.loan_type import LoanType
from smarttesting.order.loan_order import LoanOrder
from smarttesting.order.loan_order_service import (
    LoanOrderService,
    MongoDbDao,
    PostgresDao,
)


class TestLoanOrderServiceDone:
    """Pierwotny test jest mało czytelny.

    Po pierwsze nazwy metod są niedokładne, po drugie w możemy lepiej kod sformatować
    i zastosować assert object, żeby zwiększyć czytelność sekcji then.
    """

    STUDENT_PROMO_DISCOUNT_NAME = "Student Promo"
    DEFAULT_STUDENT_PROMO_DISCOUNT_VALUE = "100"
    DEFAULT_STUDENT_PROMO_COMMISSION_VALUE = "200"
    DEFAULT_STUDENT_PROMO_LOAN_AMOUNT = "500"

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._postgres_dao = Mock(spec_set=PostgresDao)
        self._mongo_dao = Mock(spec_set=MongoDbDao)
        self._service = LoanOrderService(self._postgres_dao, self._mongo_dao)

    def test_raises_exception_when_not_a_student_wants_to_take_a_student_loan(
        self, not_a_student: Customer
    ) -> None:
        with pytest.raises(ValueError, match="Cannot order student loan"):
            self._service.student_loan_order(not_a_student)

    def test_grants_a_student_loan_when_a_student_applies_for_it(
        self, student: Customer
    ) -> None:
        self._mongo_dao.get_promotion_discount = Mock(
            return_value=Decimal(self.DEFAULT_STUDENT_PROMO_DISCOUNT_VALUE)
        )

        loan_order = self._service.student_loan_order(student)

        order_assert = self.LoanOrderAssert(loan_order)
        order_assert.is_student_loan()
        order_assert.has_student_promo_with_value(
            self.DEFAULT_STUDENT_PROMO_DISCOUNT_VALUE
        )
        order_assert.has_commission_equal_to(
            self.DEFAULT_STUDENT_PROMO_COMMISSION_VALUE
        )
        order_assert.has_amount_equal_to(self.DEFAULT_STUDENT_PROMO_LOAN_AMOUNT)

    @pytest.fixture()
    def not_a_student(self) -> Customer:
        return Customer(
            uuid.uuid4(), Person("A", "B", date.today(), Gender.FEMALE, "1234567890")
        )

    @pytest.fixture()
    def student(self, not_a_student: Customer) -> Customer:
        not_a_student.student()
        return not_a_student

    @dataclass(frozen=True)
    class LoanOrderAssert:
        """AssertObject.

        Klasę umieszczamy tutaj dla lepszej widoczności problemu.
        """

        _loan_order: LoanOrder

        def is_student_loan(self) -> None:
            assert self._loan_order.type == LoanType.STUDENT

        def has_student_promo_with_value(self, value: str) -> None:
            assert value
            assert len(self._loan_order.promotions) == 1
            promo = self._loan_order.promotions[0]
            expected_promo_name = TestLoanOrderServiceDone.STUDENT_PROMO_DISCOUNT_NAME
            assert (
                promo.name == expected_promo_name
            ), f"Promotion name should be {expected_promo_name} but was {promo.name}"
            expected_value = Decimal(value)
            assert (
                promo.discount == expected_value
            ), f"Promotion value should be {expected_value} but was {promo.discount}"

        def has_commission_equal_to(self, value: str) -> None:
            assert value
            expected_commission = Decimal(value)
            assert self._loan_order.commission == expected_commission, (
                f"Commission value should be {expected_commission} but is "
                f"{self._loan_order.commission}"
            )

        def has_amount_equal_to(self, value: str) -> None:
            assert value
            expected_amount = Decimal(value)
            assert self._loan_order.amount == expected_amount, (
                f"Commission value should be {expected_amount} but is "
                f"{self._loan_order.amount}"
            )
