from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.name import NameVerification


class TestNameVerification:
    @pytest.fixture()
    def nameless_person(self) -> Person:
        return Person("", "Stefanowski", date.today(), Gender.MALE, "1234567890")

    def test_should_return_positive_result_when_name_is_not_blank(
        self, nameless_person: Person
    ) -> None:
        verification = NameVerification()

        result = verification.passes(nameless_person)

        assert result.result is False
