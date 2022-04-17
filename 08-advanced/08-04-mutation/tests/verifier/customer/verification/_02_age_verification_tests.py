from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification._01_age import AgeVerification


def zbigniew(age: int) -> Person:
    today = date.today()
    date_of_birth = today.replace(year=today.year - age)
    return Person(
        "Zbigniew",
        "Stefanowski",
        date_of_birth,
        Gender.MALE,
        "1234567890",
    )


class Test02AgeVerification:
    @pytest.fixture()
    def zbigniew_from_the_future(self) -> Person:
        return zbigniew(age=-10)

    def test_should_throw_exception_when_age_invalid(
        self, zbigniew_from_the_future: Person
    ) -> None:
        verification = AgeVerification()

        with pytest.raises(ValueError, match="Age cannot be negative!"):
            verification.passes(zbigniew_from_the_future)

    @pytest.fixture()
    def old_enough_zbigniew(self) -> Person:
        return zbigniew(age=25)

    def test_should_return_positive_verification_when_age_is_within_the_threshold(
        self, old_enough_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(old_enough_zbigniew)

        assert result.result is True

    @pytest.fixture()
    def too_young_zbigniew(self) -> Person:
        return zbigniew(age=0)

    def test_should_return_negative_verification_when_age_is_below_the_threshold(
        self, too_young_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(too_young_zbigniew)

        assert result.result is False

    @pytest.fixture()
    def too_old_zbigniew(self) -> Person:
        return zbigniew(age=1000)

    def test_should_return_negative_verification_when_age_is_above_the_threshold(
        self, too_old_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(too_old_zbigniew)

        assert result.result is False


@pytest.mark.skip
class Test02AgeVerificationBoundaryTests:
    """Zakomentuj dekorator @pytest.mark.skip, żeby zwiększyć pokrycie kodu testami.
    Pokrywamy warunki brzegowe! (i to z obu stron!)"""

    @pytest.fixture()
    def lower_age_boundary_zbigniew(self) -> Person:
        return zbigniew(age=18)

    def test_should_return_positive_verification_when_age_is_in_lower_boundary(
        self, lower_age_boundary_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(lower_age_boundary_zbigniew)

        assert result.result is True

    @pytest.fixture()
    def below_lower_age_boundary_zbigniew(self) -> Person:
        return zbigniew(age=17)

    def test_should_return_negative_verification_when_age_is_below_lower_boundary(
        self, below_lower_age_boundary_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(below_lower_age_boundary_zbigniew)

        assert result.result is False

    @pytest.fixture()
    def upper_age_boundary_zbigniew(self) -> Person:
        return zbigniew(age=99)

    def test_should_return_positive_verification_when_age_is_in_upper_boundary(
        self, upper_age_boundary_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(upper_age_boundary_zbigniew)

        assert result.result is True

    @pytest.fixture()
    def above_upper_age_boundary_zbigniew(self) -> Person:
        return zbigniew(age=100)

    def test_should_return_negative_verification_when_age_is_above_upper_boundary(
        self, above_upper_age_boundary_zbigniew: Person
    ) -> None:
        verification = AgeVerification()

        result = verification.passes(above_upper_age_boundary_zbigniew)

        assert result.result is False
