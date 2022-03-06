from datetime import date
from unittest.mock import Mock, call
from uuid import uuid4

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.customer_verification_result import Status
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.customer.verification.identity_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.customer.verification.name import NameVerification
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification import Verification
from smarttesting.verifier.verification_event import VerificationEvent
from tests.smarttesting.verifier.customer.customer_tests_base import CustomerTestBase


class TestCustomerVerifier(CustomerTestBase):
    """Klasa zawiera przykłady zastosowania mocka w celu weryfikacji interakcji.

    Przykłady zawierają wykorzystanie obiektu typu EventEmitter,
    zastosowanie buildera obiektów testowych,
    przykłady testowania komunikacji/interakcji."""

    _event_emitter: EventEmitter
    _customer_verifier: CustomerVerifier
    _customer: Customer

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._customer = self._build_customer()
        self._event_emitter = Mock(spec_set=EventEmitter)
        self._customer_verifier = CustomerVerifier(
            self._build_verifications(self._event_emitter)
        )

    def _build_verifications(self, event_emitter: EventEmitter) -> set[Verification]:
        return {
            AgeVerification(event_emitter),
            IdentificationNumberVerification(event_emitter),
            NameVerification(event_emitter),
        }

    def test_verifies_correct_person(self) -> None:
        """Zastosowanie buildera w setupie testu."""
        customer = (
            self.builder()
            .with_national_id_number("80030818293")
            .with_date_of_birth(1980, 3, 8)
            .with_gender(Gender.MALE)
            .build()
        )

        result = self._customer_verifier.verify(customer)

        assert result.status == Status.VERIFICATION_PASSED
        assert result.user_id == customer.uuid

    def test_emits_verification_event(self) -> None:
        """Testowanie komunikacji/interakcji."""
        self._customer_verifier.verify(self._customer)

        # Weryfikacja interakcji - sprawdzamy, że metoda emit(...) została wywołana 3 razy
        # z argumentem typu VerificationEvent, którego metoda passed(...) zwraca true
        self._event_emitter.assert_has_calls(  # type: ignore
            [
                call.emit(VerificationEvent(True)),
                call.emit(VerificationEvent(True)),
                call.emit(VerificationEvent(True)),
            ]
        )

    def _build_customer(self) -> Customer:
        """Metoda pomocnicza do setupu testów."""
        person = Person("John", "Smith", date(1996, 8, 28), Gender.MALE, "96082812079")
        return Customer(uuid4(), person)
