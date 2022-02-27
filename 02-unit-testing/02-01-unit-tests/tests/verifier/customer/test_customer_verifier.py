from datetime import date
from typing import Set
from unittest.mock import Mock, call

import pytest
from smarttesting.customer.person import Gender
from smarttesting.verifier.customer.customer_verification_result import Status
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.customer.verification.name import NameVerification
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification import Verification
from smarttesting.verifier.verification_event import VerificationEvent

from .factories import CustomerFactory


class TestCustomerVerifier:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._customer = CustomerFactory.build()
        self._event_emitter = Mock(spec_set=EventEmitter)
        verifications = self._build_verifications(self._event_emitter)
        self._service = CustomerVerifier(verifications)

    def _build_verifications(self, event_emitter: EventEmitter) -> Set[Verification]:
        return {
            AgeVerification(event_emitter),
            IdentificationNumberVerification(event_emitter),
            NameVerification(event_emitter),
        }

    def test_verifies_person(self) -> None:
        """Zastosowanie fabryki w setupie testu."""
        customer = CustomerFactory.build(
            person__national_id_number="80030818293",
            person__date_of_birth=date(1980, 3, 8),
            person__gender=Gender.MALE,
        )

        result = self._service.verify(customer)

        assert result.status == Status.VERIFICATION_PASSED
        assert result.user_id == customer.uuid

    def test_emits_verification_event(self) -> None:
        self._service.verify(self._customer)

        # Weryfikacja interakcji. Sprawdzamy, że metoda emit zostala wywołana
        # 3 razy z argumentem typu VerificationEvent o określonej wartości
        self._event_emitter.emit.assert_has_calls(
            [call(VerificationEvent(True)) for _ in range(3)]
        )
