import uuid
from datetime import date
from decimal import Decimal

from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.order.loan_order_service import LoanOrderService
from tests.order.loan_order_assert import LoanOrderAssert


class TestLoanOrderService:
    def test_creates_student_loan_order(self) -> None:
        student = self._build_student()
        service = LoanOrderService()

        loan_order = service.student_loan_order(student)

        assert loan_order.order_date == date.today()
        students_promos = [
            promo for promo in loan_order.promotions if promo.name == "Student Promo"
        ]
        assert len(students_promos) == 1
        assert len(loan_order.promotions) == 1
        assert loan_order.promotions[0].discount == Decimal("10")

    def test_assert_object_creates_student_loan_order(self) -> None:
        """Przykład AssertObject Pattern."""
        student = self._build_student()
        service = LoanOrderService()

        loan_order = service.student_loan_order(student)

        order_assert = LoanOrderAssert(loan_order)
        order_assert.registered_today()
        order_assert.has_promotion("Student Promo")
        order_assert.has_only_one_promotion()
        order_assert.first_promotion_has_discount_value(Decimal("10"))

    def test_chained_assert_object_creates_student_loan_order(self) -> None:
        """Przykład AssertObject Pattern z chainowaniem asercji."""
        student = self._build_student()
        service = LoanOrderService()

        loan_order = service.student_loan_order(student)

        (
            LoanOrderAssert(loan_order)
            .registered_today()
            .has_promotion("Student Promo")
            .has_only_one_promotion()
            .first_promotion_has_discount_value(Decimal("10"))
        )

    def test_chained_assert_object_creates_student_loan_order_simple_assertion(
        self,
    ) -> None:
        """Przykład AssertObject Pattern z metodą wrappującą chain asercji."""
        student = self._build_student()
        service = LoanOrderService()

        loan_order = service.student_loan_order(student)

        LoanOrderAssert(loan_order).student_loan_order()

    def _build_student(self) -> Customer:
        person = Person("John", "Smith", date(1996, 8, 28), Gender.MALE, "96082812079")
        customer = Customer(uuid.uuid4(), person)
        customer.student()
        return customer
