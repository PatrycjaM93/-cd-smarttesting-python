# pylint: disable=redefined-outer-name
from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)


@pytest.fixture()
def anna_the_woman() -> Person:
    return Person("Anna", "Annowska", date.today(), Gender.FEMALE, "00000000020")


@pytest.fixture()
def anna_with_non_female_id() -> Person:
    return Person("Anna", "Annowska", date.today(), Gender.FEMALE, "00000000010")


@pytest.fixture()
def zbigniew_the_man() -> Person:
    return Person("Zbigniew", "Zbigniewowski", date.today(), Gender.MALE, "00000000010")


@pytest.fixture()
def zbigniew_with_non_male_id() -> Person:
    return Person("Zbigniew", "Zbigniewowski", date.today(), Gender.MALE, "00000000020")


class TestIdentificationNumberVerification:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.verification = IdentificationNumberVerification()

    def test_should_return_positive_verification_when_gender_female_corresponds_to_id_number(
        self, anna_the_woman: Person
    ) -> None:
        result = self.verification.passes(anna_the_woman)

        assert result.result is True

    def test_should_return_negative_verification_when_gender_female_does_not_correspond_to_id_number(
        self, anna_with_non_female_id: Person
    ) -> None:
        result = self.verification.passes(anna_with_non_female_id)

        assert result.result is False

    def should_return_positive_verification_when_gender_male_corresponds_to_id_number(
        self, zbigniew_the_man: Person
    ) -> None:
        result = self.verification.passes(zbigniew_the_man)

        assert result.result is True

    def test_should_return_negative_verification_when_gender_male_does_not_correspond_to_id_number(
        self, zbigniew_with_non_male_id: Person
    ) -> None:
        result = self.verification.passes(zbigniew_with_non_male_id)

        assert result.result is False
