from datetime import date
from decimal import Decimal
from typing import Iterator
from unittest.mock import Mock, call

import pytest
from freezegun import freeze_time
from smarttesting.customer.customer import Customer
from smarttesting.db.mongo_db_accessor import MongoDbAccessor
from smarttesting.db.postgres_accessor import PostgresAccessor
from smarttesting.order.loan_order_service import LoanOrderService
from tests.smarttesting.order.loan_order_assert import LoanOrderAssert
from tests.smarttesting.order.loan_order_tests_base import LoanOrderTestsBase


class TestLoanOrderService(LoanOrderTestsBase):
    """Klasa zawiera przykłady różnych sposobów setupu i teardownu testów.

    Do tego znajdziesz w środku przykłady zastosowania stubów i mocków.
    """

    # Mock, który będzie wykorzystywany później do weryfikacji interakcji
    _postgres_accessor = Mock(spec_set=PostgresAccessor)

    # Tworzenie obiektów stub/ mock
    # Ten obiekt jest wyłącznie stubem (nie używamy go do weryfikacji interakcji),
    # a to, że jest tworzony przez `Mock(...)` to wyłącznie specyfika frameworku.
    _mongo_db_accessor = Mock(spec_set=MongoDbAccessor)

    _loan_order_service = LoanOrderService(_postgres_accessor, _mongo_db_accessor)

    @pytest.fixture(autouse=True, scope="class")
    def class_setup_teardown(self) -> Iterator[None]:
        """Metoda setupująca wywoływana raz w danej klasie (scope="class").

        Dzięki słówku kluczowemu yield możemy też umieścić w jednej funkcji
        teardown (sprzątanie) po wykonaniu wszystkich testów w klasie.
        """
        self.logger.info("Running tests")
        yield
        self.logger.info("Finished running tests.")

    @pytest.fixture(autouse=True)
    def setup(self, student: Customer) -> Iterator[None]:
        """Metoda setupująca wywoływana przed każdym testem.

        Używa domyślnej wartości argumentu `scope`, (scope="function")"""
        self._student = student
        self._mongo_db_accessor.get_promotion_discount = Mock(
            return_value=Decimal("10")
        )
        yield
        self._mongo_db_accessor.reset_mock()
        self._postgres_accessor.reset_mock()

    @freeze_time()  # just in case the test is run at midnight ;)
    def test_creates_student_loan_order(self) -> None:
        """Testowanie wyniku operacji."""
        loan_order = self._loan_order_service.student_loan_order(self._student)

        assert loan_order.order_date == date.today()
        student_promos = [
            promo for promo in loan_order.promotions if promo.name == "Student Promo"
        ]
        assert len(student_promos) == 1
        assert len(loan_order.promotions) == 1
        assert loan_order.promotions[0].discount == Decimal("10")

    def test_updates_promotion_statistics(self) -> None:
        self._loan_order_service.student_loan_order(self._student)

        # Weryfikacja interakcji z użyciem obiektu, który jest też stosowany jako stub
        self._postgres_accessor.assert_has_calls(
            [call.update_promotion_statistics("Student Promo")]
        )

        # Weryfikacja tego, że dana interakcja nie wystąpiła
        unexpected_call = call.update_promotion_statistics("Student Promo 2")
        assert unexpected_call not in self._postgres_accessor.mock_calls

        # Alternatywna asercja, która sprawdza że mock został wywołany dokładnie raz
        # z oczekiwanym argumentem
        self._postgres_accessor.update_promotion_statistics.assert_called_once_with(
            "Student Promo"
        )

    @freeze_time()
    def test_creates_student_loan_order_with_assert_object(self) -> None:
        """Przykład AssertObject Pattern."""
        loan_order = self._loan_order_service.student_loan_order(self._student)

        order_assert = LoanOrderAssert(loan_order)
        order_assert.registered_today()
        order_assert.has_promotion("Student Promo")
        order_assert.has_only_one_promotion()
        order_assert.first_promotion_has_discount_value(Decimal("10"))

    def test_creates_student_loan_order_with_assert_object_chained(self) -> None:
        """AssertObject Pattern z zastosowaniem metody robiącej kilka asercji."""
        loan_order = self._loan_order_service.student_loan_order(self._student)

        order_assert = LoanOrderAssert(loan_order)
        order_assert.student_loan_order()
