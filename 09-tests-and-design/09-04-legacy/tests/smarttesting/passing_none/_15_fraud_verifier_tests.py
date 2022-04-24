# pylint: disable=unused-argument,invalid-name
from dataclasses import dataclass

import pytest


class Test15FraudVerifier:
    def test_should_mark_client_with_debt_as_fraud(self) -> None:
        """Przykład testu, gdzie zakładamy, że nie musimy tworzyć wszystkich obiektów
        i podmieniamy je None'm. Jeśli zależność jest wymagana - test nam się wywali.

        Jest to ciut bezpieczniejsze niż Mock nienaśladujący żadnego obiektu.
        """
        verifier = _16_FraudVerifier(None, None, DatabaseAccessor())  # type: ignore

        result = verifier.is_fraud("Fraudowski")

        assert result is True

    @pytest.mark.skip
    def test_should_calculate_penalty_when_fraud_applies_for_a_loan(self) -> None:
        """Przykład testu, gdzie zakładamy, że nie musimy tworzyć wszystkich obiektów
        i podmieniamy je None'm. Niestety nie trafiamy i leci nam AttributeError,
        gdyż dani kolaboratorzy byli wymagani.
        """
        verifier = _16_FraudVerifier(PenaltyCalculator(), None, None)  # type: ignore

        penalty = verifier.calculate_fraud_penalty("Fraudowski")

        assert penalty > 0

    def test_should_calculate_penalty_when_fraud_applies_for_a_loan_with_both_deps(
        self,
    ) -> None:
        """Wygląda na to, że musimy przekazać jeszcze `TaxHistoryRetriever`."""
        verifier = _16_FraudVerifier(
            PenaltyCalculator(), TaxHistoryRetriever(), None  # type: ignore
        )

        penalty = verifier.calculate_fraud_penalty("Fraudowski")

        assert penalty > 0


@dataclass(frozen=True)
class Client:
    name: str
    has_debt: bool


class DatabaseAccessor:
    def get_client_by_name(self, name: str) -> Client:
        return Client("Fraudowski", True)


class PenaltyCalculator:
    def calculate_penalty(self, client: Client) -> int:
        return 100


class TaxHistoryRetriever:
    def return_last_revenue(self, client: Client) -> int:
        return 150


@dataclass
class _16_FraudVerifier:
    """Implementacja zawierająca dużo zależności, skomplikowany, długi kod."""

    _penalty: PenaltyCalculator
    _history: TaxHistoryRetriever
    _accessor: DatabaseAccessor

    def calculate_fraud_penalty(self, name: str) -> int:
        # 5 000 linijek kodu dalej...

        # set client history to false, otherwise it won't work
        last_revenue = self._history.return_last_revenue(Client(name, False))
        # set client history to true, otherwise it won't work
        penalty = self._penalty.calculate_penalty(Client(name, True))
        return last_revenue // 50 + penalty

    def is_fraud(self, name: str) -> bool:
        # 7 000 linijek kodu dalej....
        client = self._accessor.get_client_by_name(name)
        return client.has_debt
