from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.identity import IdentityVerification


@pytest.mark.homework("Czy ten test weryfikuje kod produkcyjny?")
class TestIdentifyVerification:
    def test_fails_for_an_invalid_identity_number(
        self, person_with_invalid_pesel: Person
    ) -> None:
        verification = IdentityVerification()

        result = verification.passes(person_with_invalid_pesel)

        assert result is False

    @pytest.fixture()
    def person_with_invalid_pesel(self) -> Person:
        return Person("jan", "kowalski", date.today(), Gender.MALE, "abcdefghijk")
