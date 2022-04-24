from datetime import date
from unittest.mock import Mock

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.surname import SurnameVerification
from smarttesting.verifier.customer.verification.surname_checker import SurnameChecker


@pytest.mark.homework("Czy framework do mockowania działa?")
class TestSurnameVerification:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._checker = Mock(spec_set=SurnameChecker)
        self._verification = SurnameVerification(self._checker)

    def test_returns_false_when_surname_invalid(self, person: Person) -> None:
        self._checker.check_surname = Mock(return_value=False)

        assert self._verification.passes(person) is False

    def test_returns_true_when_surname_invalid(self, person: Person) -> None:
        self._checker.check_surname = Mock(return_value=True)

        assert self._verification.passes(person) is True

    @pytest.fixture()
    def person(self) -> Person:
        return Person("a", "b", date.today(), Gender.MALE, "1234567890")
