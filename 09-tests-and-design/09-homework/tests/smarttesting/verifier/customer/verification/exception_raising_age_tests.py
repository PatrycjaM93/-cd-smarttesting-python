from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.exception_raising_age import (
    ExceptionRaisingAgeVerification,
)


@pytest.mark.homework("Czy na pewno te asercje są poprawne?")
class TestExceptionRaisingAge:
    def test_good(self, good_person: Person) -> None:
        assert ExceptionRaisingAgeVerification().passes(good_person)

    def test_bad(self, bad_person: Person) -> None:
        try:
            ExceptionRaisingAgeVerification().passes(bad_person)
        except ValueError:
            pass

    @pytest.fixture()
    def good_person(self) -> Person:
        today = date.today()
        twenty_years_ago = today.replace(year=today.year - 20)
        return Person("A", "B", twenty_years_ago, Gender.FEMALE, "34567890")

    @pytest.fixture()
    def bad_person(self) -> Person:
        return Person("A", "B", date.today(), Gender.FEMALE, "34567890")
