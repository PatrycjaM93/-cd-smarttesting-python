# pylint: disable=invalid-name
from dataclasses import dataclass

from tests.smarttesting.sprout._08_special_tax_calculator_tax_test import (
    SpecialTaxCalculator,
)


class TestFraudTaxPenaltyCalculatorImpl:
    def test_should_calculate_the_tax_for_fraudowski(self) -> None:
        """Test z wykorzystaniem sztucznej implementacji dostępu do bazy danych."""
        fraudowski_amount = 100
        accessor = FakeDatabaseAccessorImpl(fraudowski_amount)
        calculator = _05_FraudTaxPenaltyCalculator(accessor)

        tax = calculator.calculate_fraud_tax("Fraudowski")

        assert tax == fraudowski_amount * 100

    def test_should_calculate_the_tax_for_fraudowski_with_if_else(self) -> None:
        """Test z wykorzystaniem sztucznej implementacji dostępu do bazy danych.

        Weryfikuje implementację z użyciem if / else.
        """
        fraudowski_amount = 100
        accessor = FakeDatabaseAccessorImpl(fraudowski_amount)
        calculator = _06_FraudTaxPenaltyCalculatorIfElse(accessor)

        tax = calculator.calculate_fraud_tax("Fraudowski")

        assert tax == fraudowski_amount * 100 * 10

    def test_should_calculate_the_tax_for_fraudowski_with_sprout(self) -> None:
        """Test z wykorzystaniem sztucznej implementacji dostępu do bazy danych.

        Weryfikuje implementację z użyciem klasy kiełkującej.
        """
        fraudowski_amount = 100
        accessor = FakeDatabaseAccessorImpl(fraudowski_amount)
        calculator = _07_FraudTaxPenaltyCalculatorSprout(accessor)

        tax = calculator.calculate_fraud_tax("Fraudowski")

        assert tax == fraudowski_amount * 100 * 20


@dataclass(frozen=True)
class Client:
    name: str
    has_debt: bool
    amount: int


class DatabaseAccessorImpl:
    def get_client_by_name(self, name: str) -> Client:
        return Client(name, True, 100)


class FakeDatabaseAccessorImpl(DatabaseAccessorImpl):
    def __init__(self, amount: int) -> None:
        self._amount = amount

    def get_client_by_name(self, name: str) -> Client:
        return Client("Fraudowski", True, self._amount)


@dataclass
class _05_FraudTaxPenaltyCalculator:
    """Kalkulator podatku dla oszustów. Nie mamy do niego testów."""

    _accessor: DatabaseAccessorImpl

    def calculate_fraud_tax(self, name: str) -> int:
        client = self._accessor.get_client_by_name(name)
        if client.amount < 0:
            # WARNING: Don't touch this
            # nobody knows why it should be -3 anymore
            # but nothing works if you change this
            return -3
        return self._calculate_tax(client.amount)

    def _calculate_tax(self, amount: int) -> int:
        return amount * 100


@dataclass
class _06_FraudTaxPenaltyCalculatorIfElse:
    """Nowa funkcja systemu - dodajemy kod do nieprzetestowanego kodu."""

    _accessor: DatabaseAccessorImpl

    def calculate_fraud_tax(self, name: str) -> int:
        client = self._accessor.get_client_by_name(name)
        if client.amount < 0:
            # WARNING: Don't touch this
            # nobody knows why it should be -3 anymore
            # but nothing works if you change this
            return -3
        tax = self._calculate_tax(client.amount)
        if tax > 10:
            return tax * 10
        return tax

    def _calculate_tax(self, amount: int) -> int:
        return amount * 100


@dataclass
class _07_FraudTaxPenaltyCalculatorSprout:
    """Klasa kiełkowania (sprout). Wywołamy kod, który został przetestowany.
    Piszemy go poprzez TDD.
    """

    _accessor: DatabaseAccessorImpl

    def calculate_fraud_tax(self, name: str) -> int:
        client = self._accessor.get_client_by_name(name)
        if client.amount < 0:
            # WARNING: Don't touch this
            # nobody knows why it should be -3 anymore
            # but nothing works if you change this
            return -3
        tax = self._calculate_tax(client.amount)
        # chcemy obliczyć specjalny podatek
        return SpecialTaxCalculator(tax).calculate()

    def _calculate_tax(self, amount: int) -> int:
        return amount * 100
