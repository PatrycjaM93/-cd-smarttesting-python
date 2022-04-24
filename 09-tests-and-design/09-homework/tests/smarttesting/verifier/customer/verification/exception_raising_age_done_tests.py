from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.exception_raising_age import (
    ExceptionRaisingAgeVerification,
)


class TestExceptionRaisingAgeDone:
    """Pierwotny test nie weryfikował nic albo nie dość dokładnie.

    Asercje były niedokończone; w przypadku pozytywnego scenariusza powinniśmy
    sprawdzać czy wartość jest dokładnie True (operator is), a dla wyjątku użyć raczej
    `pytest.raises` by test się załamał dla przypadku, gdy wyjątek nie jest rzucany.

    Ponadto test był nieczytelny."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._verification = ExceptionRaisingAgeVerification()

    def test_passes_when_a_person_is_an_adult(self, adult: Person) -> None:
        result = self._verification.passes(adult)

        assert result is True

    def test_raises_exception_when_a_person_is_a_minor(self, minor: Person) -> None:
        with pytest.raises(ValueError):
            self._verification.passes(minor)

    @pytest.fixture()
    def adult(self) -> Person:
        today = date.today()
        twenty_years_ago = today.replace(year=today.year - 20)
        return Person("A", "B", twenty_years_ago, Gender.FEMALE, "34567890")

    @pytest.fixture()
    def minor(self) -> Person:
        return Person("A", "B", date.today(), Gender.FEMALE, "34567890")
