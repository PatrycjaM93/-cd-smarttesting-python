import logging
import uuid
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.order.loan_order_service import (
    LoanOrderService,
    MongoDbDao,
    PostgresDao,
)

from .loan_order_assert import LoanOrderAssert

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module", autouse=True)
def before_after_all_tests():
    """Fikstura wykonująca się na początku i końcu zestawu testów z tego pliku.

    O momencie użycia decyduje parametr `scope` tu ustawiony na "module". Gdybyśmy
    chcieli wykonywać fiksturę przed i po CAŁYM zestawie, możemy użyć scope="session".

    Jeżeli mamy fikstury ze scope="session", to zalecamy je umieszczać w conftest.py
    najwyższego poziomu.
    """
    logger.info("Before all in module %s", __name__)
    # Linia z instrukcją `yield` zawiesza dalsze wykonanie kodu.
    # Wracamy tu na koniec zestawu testów, tuż po `yield`.
    yield
    logger.info("After all in module %s", __name__)


class TestLoanOrderService:
    # postgres_dao = Mock(spec_set=PostgresDao)
    # mongo_dao = Mock(spec_set=MongoDao)
    """
    Inicjalizowanie Mocków na klasie testowej nie jest zalecane w Pythonie,
    gdyż Mock jest stanowy i może to prowadzić do false-negative'ów.

    To samo dotyczy wszystkich innych obiektów potrzebnych do testowania,
    których stan może się zmieniać podczas testów.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Metoda przeprowadzająca setup.

        `scope` domyślnie ma wartość "function", co powoduje że fikstura jest
        aplikowana przed każdym testem.

        `autouse=True` spowoduje, że fikstura będzie wykonywana automatycznie
        nawet jeśli nie zadeklarujemy tego na funkcji/metodzie testowej.

        Zrobienie takiej fikstury poza klasą spowoduje wykonywanie jej przed każdym
        testem.
        """
        # Tworzac Mocki, zawsze używamy `spec_set`. W ten sposób upewniamy się,
        # że zobaczymy błąd gdy omyłkowo zawołamy nieistniejącą metodę na mocku/stubie
        self._postgres_dao = Mock(spec_set=PostgresDao)
        # unittest.mock.Mock z biblioteki standardowej ma dość ubogie możliwości.
        # Nie można na przykład łatwo go skonfigurować by zwracał określony wynik
        # dla konkretnego argumentu.
        # Dla lepszych mocków polecam port Mockito - python-mockito.
        self._postgres_dao.get_promotion_discount = Mock(return_value=Decimal("10"))

        self._mongo_dao = Mock(spec_set=MongoDbDao)
        self._service = LoanOrderService(self._postgres_dao, self._mongo_dao)

    @pytest.fixture()
    def student(self) -> Customer:
        """Fikstura tworząca nowego studenta.

        Zamiast zawsze ręcznie tworzyć instancję lub robić to w metodzie prywatnej,
        można napisać fiksturę, a następnie zadeklarować ją na liście argumentów
        danej funkcji testowej.

        Jeżeli z jakiegoś powodu nie interesuje nas wartość zwrócona a chcemy by
        fikstura była aktywna w teście, to dekorujemy go:
        ```
        @pytest.mark.usefixtures("student")
        def test_...(self) -> None:
            pass
        ```
        Można to wykorzystać np. do ustawiania stubów w określony sposób.

        W Pythonie warto iść jeszcze o krok dalej i wykorzystać bibliotekę FactoryBoy
        do tworzenia reużywalnych fabryk obiektów na potrzeby testów.
        """
        person = Person("John", "Smith", date(1996, 8, 28), Gender.MALE, "96082812079")
        customer = Customer(uuid.uuid4(), person)
        customer.student()
        return customer

    def test_creates_student_loan_order(self, student: Customer) -> None:
        loan_order = self._service.student_loan_order(student)

        assert loan_order.order_date == date.today()
        student_promos = [
            promo for promo in loan_order.promotions if promo.name == "Student Promo"
        ]
        assert len(student_promos) == 1
        assert len(loan_order.promotions) == 1
        assert loan_order.promotions[0].discount == Decimal("10")

    def test_updates_promotion_statistics(self, student: Customer) -> None:
        self._service.student_loan_order(student)

        # Weryfikacja interakcji na innej metodzie niż ta zastubbowana
        self._postgres_dao.update_promotion_statistics.assert_called_once_with(
            "Student Promo"
        )

    def test_does_not_call_update_promotion_discount(self, student: Customer) -> None:
        self._service.student_loan_order(student)

        # Weryfikacja braku wywołania danej metody
        self._postgres_dao.update_promotion_discount.assert_not_called()

    def test_assert_object_creates_student_loan_order(self, student: Customer) -> None:
        """Przykład AssertObject Pattern."""
        loan_order = self._service.student_loan_order(student)

        order_assert = LoanOrderAssert(loan_order)
        order_assert.registered_today()
        order_assert.has_promotion("Student Promo")
        order_assert.has_only_one_promotion()
        order_assert.first_promotion_has_discount_value(Decimal("10"))

    def test_chained_assert_object_creates_student_loan_order(
        self, student: Customer
    ) -> None:
        """Przykład AssertObject Pattern z chainowaniem asercji."""
        loan_order = self._service.student_loan_order(student)

        (
            LoanOrderAssert(loan_order)
            .registered_today()
            .has_promotion("Student Promo")
            .has_only_one_promotion()
            .first_promotion_has_discount_value(Decimal("10"))
        )

    def test_chained_assert_object_creates_student_loan_order_simple_assertion(
        self, student: Customer
    ) -> None:
        """Przykład AssertObject Pattern z metodą wrappującą chain asercji."""
        loan_order = self._service.student_loan_order(student)

        LoanOrderAssert(loan_order).student_loan_order()
