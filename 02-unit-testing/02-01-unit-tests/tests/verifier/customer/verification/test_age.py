import pytest
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.event_emitter import EventEmitter
from tests.verifier.customer.factories import PersonFactory


class TestAgeVerification:
    @pytest.fixture()
    def verification(self) -> AgeVerification:
        return AgeVerification(EventEmitter())

    def test_passes_for_age_between_18_and_99(
        self, verification: AgeVerification
    ) -> None:
        # Given
        person = PersonFactory.build(age=22)

        # When
        passes = verification.passes(person)

        # Then
        assert passes is True

    def test_fails_for_person_older_than_99(
        self, verification: AgeVerification
    ) -> None:
        # Given
        person = PersonFactory.build(age=100)

        # When
        passes = verification.passes(person)

        # Then
        assert passes is False

    def test_raises_value_error_when_age_is_below_zero(
        self, verification: AgeVerification
    ) -> None:
        # Given
        person = PersonFactory.build(age=-1)

        # When & Then
        with pytest.raises(ValueError):
            verification.passes(person)
