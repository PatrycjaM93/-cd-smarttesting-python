from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.name import NameVerification
from smarttesting.verifier.event_emitter import EventEmitter


class TestNameVerificationDone:
    """Pierwotny test duplikuje logikę weryfikacji w sekcji given.

    To oznacza, że de facto nic nie testujemy. Wykorzystujemy tę samą logikę do
    przygotowania obiektu, który oczekujemy na wyjściu. Jeśli zmieni się logika
    biznesowa oba nasze testy dalej będą przechodzić.

    Szczerze mówiąc to nawet nie weryfikujemy czy wynik boolowski jest true czy false.
    Po prostu sprawdzamy czy jest taki sam jaki na wejściu.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._verification = NameVerification(EventEmitter())

    def test_passes_when_name_is_alphanumeric(
        self, person_with_valid_name: Person
    ) -> None:
        result = self._verification.passes(person_with_valid_name)

        assert result is True

    def test_fails_when_name_is_not_alphanumeric(
        self, person_with_invalid_name: Person
    ) -> None:
        result = self._verification.passes(person_with_invalid_name)

        assert result is False

    @pytest.fixture()
    def person_with_valid_name(self) -> Person:
        return Person("jan", "kowalski", date.today(), Gender.MALE, "abcdefghijk")

    @pytest.fixture()
    def person_with_invalid_name(self) -> Person:
        """Często zdarza się tak, że jak obiekt podczas inicjalizacji potrzebuje kilku
        parametrów tych samych typów. Warto jawnie wprowadzić nieprawidłową wartość w
        każde inne "podejrzane" pole, tak żeby mieć pewność, że testujemy to, co
        powinniśmy.
        """
        return Person("", "Kowalski", date.today(), Gender.MALE, "abcdefghijk")
