from datetime import date

from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.simple_verification import SimpleVerification


class TestSimpleVerification:
    """
    Test zawiera przykład `false pass`.
    """

    def test_passes_simple_verification_false_pass(self) -> None:
        # Given
        verification = SimpleVerification()
        person = Person("John", "Smith", date(1996, 8, 28), Gender.MALE, "96082812079")

        # When
        verification.passes(person)

        # Then
        assert verification.verification_passed is True
