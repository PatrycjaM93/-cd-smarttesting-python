from datetime import date
from unittest.mock import Mock

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.business_rules_verification import (
    BusinessRulesVerification,
)
from smarttesting.verifier.customer.verification.verifier_manager import VerifierManager
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification_event import VerificationEvent


class TestBusinessRulesVerificationDone:
    """Pierwotny test był bardzo źle napisany.

    Nie dość, że nie wiemy, co testujemy patrząc na nazwę metody testowej,
    to nawet nie wiemy gdzie jest sekcja when. Kod jest bardzo nieczytelny i robi
    stanowczo za dużo. Używa też niepotrzebnych konkretnych weryfikacji.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._emitter = Mock(spec_set=EventEmitter)
        self._manager = Mock(
            spec_set=VerifierManager,
            verify_name=Mock(return_value=True),
            verify_surname=Mock(return_value=True),
            verify_address=Mock(return_value=True),
            verify_phone=Mock(return_value=True),
            verify_tax_information=Mock(return_value=True),
        )
        self._verification = BusinessRulesVerification(self._emitter, self._manager)

    @pytest.fixture()
    def person(self) -> Person:
        return Person("J", "K", date.today(), Gender.MALE, "1234567890")

    def test_passess_verification_when_all_verification_pass(
        self,
        person: Person,
    ) -> None:
        result = self._verification.passes(person)

        assert result is True
        self._emitter.emit.assert_called_once_with(VerificationEvent(True))

    @pytest.mark.parametrize(
        "verification_to_fail",
        [
            "verify_name",
            "verify_surname",
            "verify_address",
            "verify_phone",
            "verify_tax_information",
        ],
    )
    def test_fails_verification_when_a_single_verification_doesnt_pass(
        self,
        person: Person,
        verification_to_fail: str,
    ) -> None:
        """Test parametryzowany przypadków negatywnych.

        Na podstawie typu weryfikacji ustawi stuba w odpowiednim stanie.
        """
        setattr(self._manager, verification_to_fail, Mock(return_value=False))

        result = self._verification.passes(person)

        assert result is False
        self._emitter.emit.assert_called_once_with(VerificationEvent(False))
