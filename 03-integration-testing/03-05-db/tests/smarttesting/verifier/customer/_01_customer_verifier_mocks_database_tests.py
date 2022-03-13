import uuid
from datetime import date
from unittest.mock import Mock

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import Status
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import VerifiedPerson


class Test01CustomerVerifierMocksDatabase:
    """
    Klasa testowa pokazująca jak testując serwis aplikacyjny `CustomerVerifier`,
    możemy zamockować komunikację z bazą danych.
    """

    def test_returns_stored_customer_result_when_customer_already_verified(
        self,
        existing_verified_person: VerifiedPerson,
        customer_verifier_with_exception_throwing_bik: CustomerVerifier,
        non_fraud_person: Person,
        repository: Mock,
    ) -> None:
        result = customer_verifier_with_exception_throwing_bik.verify(
            Customer(uuid.UUID(existing_verified_person.uuid), non_fraud_person)
        )

        assert result.user_id == uuid.UUID(
            existing_verified_person.uuid
        ), "Must represent the same person"
        assert result.status == Status.VERIFICATION_PASSED
        # No storing to DB took place
        repository.save.assert_not_called()

    def test_calculates_customer_result_when_customer_not_previously_verified(
        self,
        customer_verifier_with_passing_bik: CustomerVerifier,
        non_fraud_person: Person,
        repository: Mock,
    ) -> None:
        new_uuid = uuid.uuid4()
        new_customer = Customer(new_uuid, non_fraud_person)

        result = customer_verifier_with_passing_bik.verify(new_customer)

        assert result.user_id == new_uuid, "Must represent the same person"
        assert result.status == Status.VERIFICATION_PASSED
        # Chcemy się upewnić, że doszło do zapisu w bazie danych
        repository.save.assert_called_once()
        _, call_args, _ = repository.save.mock_calls[0]
        assert call_args[0].uuid == str(new_uuid)

    @pytest.fixture
    def customer_verifier_with_exception_throwing_bik(
        self,
        repository: VerificationRepository,
        exception_throwing_bik_identifier: BIKVerificationService,
    ) -> CustomerVerifier:
        """Testowa implementacja serwisu CustomerVerifier.

        Jeśli zapis w bazie miał już miejsce to nie powinniśmy wołać BIKa.
        Jeśli BIK zostanie wywołany to chcemy rzucić wyjątek.
        """
        return CustomerVerifier(exception_throwing_bik_identifier, set(), repository)

    @pytest.fixture
    def customer_verifier_with_passing_bik(
        self,
        repository: VerificationRepository,
        always_passing_bik_verifier: BIKVerificationService,
    ) -> CustomerVerifier:
        """Testowa implementacja serwisu CustomerVerifier.

        Z z nadpisaną implementacją klienta BIK. Klient ten zawsze zwraca,
        że weryfikacja się powiodła.
        """
        return CustomerVerifier(always_passing_bik_verifier, set(), repository)

    @pytest.fixture
    def repository(self) -> VerificationRepository:
        return Mock(
            spec_set=VerificationRepository, find_by_user_id=Mock(return_value=None)
        )

    @pytest.fixture
    def existing_verified_person(
        self,
        verified_non_fraud: VerifiedPerson,
        repository: Mock,
    ) -> VerifiedPerson:
        """Symulujemy, że osoba została zapisana w bazie danych wcześniej."""
        repository.find_by_user_id = Mock(return_value=verified_non_fraud)
        return verified_non_fraud

    @pytest.fixture
    def verified_non_fraud(self) -> VerifiedPerson:
        return VerifiedPerson(
            uuid=str(uuid.uuid4()),
            national_identification_number="1234567890",
            status=Status.VERIFICATION_PASSED.value,
        )

    @pytest.fixture
    def non_fraud_person(self) -> Person:
        return Person("Uczciwy", "Ucziwowski", date.today(), Gender.MALE, "1234567890")
