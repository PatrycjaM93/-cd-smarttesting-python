from datetime import date

from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)


def build_person(date_of_birth: date, gender: Gender) -> Person:
    return Person("John", "Doe", date_of_birth, gender, "98031416402")


class TestIdentificationNumberVerification:
    def test_passes_for_correct_identification_number(self) -> None:
        # Given
        person = build_person(date(1998, 3, 14), Gender.FEMALE)
        verification = IdentificationNumberVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert passes is True

    def test_should_fail_for_inconsistent_gender(self) -> None:
        # Given
        person = build_person(date(1998, 3, 14), Gender.MALE)
        verification = IdentificationNumberVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert passes is False

    def test_verification_should_fail_for_wrong_year_of_birth(self) -> None:
        # Given
        person = build_person(date(2000, 3, 14), Gender.FEMALE)
        verification = IdentificationNumberVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert passes is False
