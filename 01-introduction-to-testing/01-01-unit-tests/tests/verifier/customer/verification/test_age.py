from datetime import date

import pytest
from assertpy import assert_that
from expects import be_false, be_true, expect, raise_error
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.age import AgeVerification


def build_person(age: int) -> Person:
    today = date.today()
    date_of_birth = today.replace(year=today.year - age)
    return Person("Anna", "Smith", date_of_birth, Gender.FEMALE, "00000000000")


class TestAgeVerificationPytest:
    """Demonstracja asercji z wykorzystaniem standardowych asercji.

    Pytest będzie "rozwijał" w kodzie zwykłe asercje dostarczając w większości
    przypadków wartościowy feedback (np. pokaże nam co znajdowało się po obu stronach
    porównania).
    """

    def test_passes_for_age_between_18_and_99(self) -> None:
        # Given
        person = build_person(22)
        verification = AgeVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert passes is True

    def test_fails_for_person_older_than_99(self) -> None:
        # Given
        person = build_person(100)
        verification = AgeVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert passes is False

    def test_raises_value_error_when_age_is_below_zero(self) -> None:
        # Given
        person = build_person(-1)
        verification = AgeVerification()

        # When & Then
        with pytest.raises(ValueError):
            verification.passes(person)


class TestAgeVerificationAssertPy:
    """Demonstracja asercji z wykorzystaniem biblioteki assertpy."""

    def test_passes_for_age_between_18_and_99(self) -> None:
        # Given
        person = build_person(22)
        verification = AgeVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert_that(passes).is_true()

    def test_fails_for_person_older_than_99(self) -> None:
        # Given
        person = build_person(100)
        verification = AgeVerification()

        # When
        passes = verification.passes(person)

        # Then
        assert_that(passes).is_false()

    def test_raises_value_error_when_age_is_below_zero(self) -> None:
        # Given
        person = build_person(-1)
        verification = AgeVerification()

        # When & Then
        assert_that(verification.passes).raises(ValueError).when_called_with(person)


class TestAgeVerificationExpects:
    """Demonstracja asercji z wykorzystaniem biblioteki expects."""

    def test_passes_for_age_between_18_and_99(self) -> None:
        # Given
        person = build_person(22)
        verification = AgeVerification()

        # When
        passes = verification.passes(person)

        # Then
        expect(passes).to(be_true)

    def test_fails_for_person_older_than_99(self) -> None:
        # Given
        person = build_person(100)
        verification = AgeVerification()

        # When
        passes = verification.passes(person)

        # Then
        expect(passes).to(be_false)

    def test_raises_value_error_when_age_is_below_zero(self) -> None:
        # Given
        person = build_person(-1)
        verification = AgeVerification()

        # When & Then
        expect(lambda: verification.passes(person)).to(raise_error(ValueError))
