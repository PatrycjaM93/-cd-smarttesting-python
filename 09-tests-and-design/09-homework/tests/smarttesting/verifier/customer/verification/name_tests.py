from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.name import NameVerification
from smarttesting.verifier.event_emitter import EventEmitter


@pytest.mark.homework("Czy ten test w ogóle coś testuje?")
class TestNameVerification:
    def test_passes_when_name_is_alphanumeric(
        self, person_with_valid_name: Person
    ) -> None:
        verification = NameVerification(EventEmitter())
        expected = verification.passes(person_with_valid_name)

        assert verification.passes(person_with_valid_name) == expected

    def test_fails_when_name_is_not_alphanumeric(
        self, person_with_invalid_name: Person
    ) -> None:
        verification = NameVerification(EventEmitter())
        expected = verification.passes(person_with_invalid_name)

        assert verification.passes(person_with_invalid_name) == expected

    @pytest.fixture()
    def person_with_valid_name(self) -> Person:
        return Person("jan", "kowalski", date.today(), Gender.MALE, "abcdefghijk")

    @pytest.fixture()
    def person_with_invalid_name(self) -> Person:
        return Person("", "", date.today(), Gender.MALE, "abcdefghijk")
