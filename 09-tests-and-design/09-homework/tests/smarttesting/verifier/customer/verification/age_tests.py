from unittest.mock import Mock

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification_event import VerificationEvent


@pytest.mark.homework(reason="Czy ten test na pewno weryfikuje... cokolwiek?")
class TestAgeVerification:
    def test_emits_event_when_date_of_birth_invalid(self) -> None:
        emitter = Mock(spec_set=EventEmitter)
        verification = AgeVerification(emitter)

        with pytest.raises(AttributeError):
            person = Person(
                "jan", "kowalski", None, Gender.MALE, "abcdefghijkl"  # type: ignore
            )
            verification.passes(person)
            emitter.emit.assert_called_once_with(VerificationEvent(False))
