from datetime import date

from assertpy import assert_that
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.event_emitter import EventEmitter


class TestAgeVerificationAssertPy:
    """Demonstracja asercji z wykorzystaniem biblioteki assertpy."""

    def test_passes_for_age_between_18_and_99(self) -> None:
        # Given
        person = build_person(22)
        verification = AgeVerification(EventEmitter())

        # When
        passes = verification.passes(person)

        # Then
        assert_that(passes).is_true()

    def test_fails_for_person_older_than_99(self) -> None:
        # Given
        person = build_person(100)
        verification = AgeVerification(EventEmitter())

        # When
        passes = verification.passes(person)

        # Then
        assert_that(passes).is_false()

    def test_raises_value_error_when_age_is_below_zero(self) -> None:
        # Given
        person = build_person(-1)
        verification = AgeVerification(EventEmitter())

        # When & Then
        assert_that(verification.passes).raises(ValueError).when_called_with(person)


def build_person(age: int) -> Person:
    today = date.today()
    date_of_birth = today.replace(year=today.year - age)
    return Person("Anna", "Smith", date_of_birth, Gender.FEMALE, "00000000000")
