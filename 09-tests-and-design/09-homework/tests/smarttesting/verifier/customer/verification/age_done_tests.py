from datetime import date, timedelta
from unittest.mock import Mock

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification_event import VerificationEvent


class TestAgeVerificationDone:
    """Pierwotny test ma dobry zamiary, ale wykonanie niestety takowe nie jest...

    Zamieniając w pierwotnym teście warunki weryfikacji mocka widzimy, że test dalej
    przechodzi. Ponadto, okazuje się, że AttributeError może polecieć z `.age` (co ma
    miejsce gdy przekazujemy None'a).

    Czyli powinniśmy sprawdzić wiadomość wyjątku i napisać dwa scenariusze testowe -
    jeden dla None'a i jeden dla negatywnego wyniku.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._emitter_mock = Mock(spec_set=EventEmitter)
        self._verification = AgeVerification(self._emitter_mock)

    def test_raises_exception_when_date_of_birth_not_set(self) -> None:
        person = Person(
            "jan", "kowalski", None, Gender.MALE, "abcdefghijkl"  # type: ignore
        )

        with pytest.raises(AttributeError):
            self._verification.passes(person)

    def test_emits_event_when_age_negative(self) -> None:
        """Ustawiając datę na przyszłość uzyskujemy wartość ujemną wieku.

        W ten sposób jesteśmy w stanie zweryfikować, że emitter się wykonał."""
        person = Person(
            "jan",
            "kowalski",
            date.today() + timedelta(days=5),
            Gender.MALE,
            "abcdefghijkl",
        )

        with pytest.raises(ValueError):
            self._verification.passes(person)

        self._emitter_mock.emit.assert_called_once_with(VerificationEvent(False))
