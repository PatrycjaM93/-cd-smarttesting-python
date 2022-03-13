import uuid
from datetime import date

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
from tests.smarttesting.verifier.customer._02_in_memory_verification_repository import (
    InMemoryVerificationRepository,
)


class Test02CustomerVerifierInMemoryDatabase:
    """Klasa testowa pokazująca jak testować `CustomerVerifier` z bazą w pamięci."""

    def test_returns_cached_customer_result_when_customer_already_verified(
        self,
        repository: VerificationRepository,
        existing_verified_person: VerifiedPerson,
        customer_verifier_with_exception_throwing_bik: CustomerVerifier,
        non_fraud_person: Person,
    ) -> None:
        # Przed uruchomieniem metody do przetestowania, upewniamy się, że w bazie danych
        # istnieje wpis dla danego użytkownika
        assert repository.find_by_user_id(
            uuid.UUID(existing_verified_person.uuid)
        ), "Person not stored in the database!"

        customer = Customer(uuid.UUID(existing_verified_person.uuid), non_fraud_person)
        result = customer_verifier_with_exception_throwing_bik.verify(customer)

        assert result.user_id == uuid.UUID(
            existing_verified_person.uuid
        ), "Must represent the same person"
        assert result.status == Status.VERIFICATION_PASSED

    def test_calculates_customer_result_when_customer_not_previously_verified(
        self,
        customer_verifier_with_passing_bik: CustomerVerifier,
        non_fraud_person: Person,
        repository: VerificationRepository,
    ) -> None:
        new_uuid = uuid.uuid4()
        new_customer = Customer(new_uuid, non_fraud_person)
        # Przed uruchomieniem metody do przetestowania, upewniamy się, że w bazie danych
        # NIE istnieje wpis dla danego użytkownika
        assert (
            repository.find_by_user_id(new_uuid) is None
        ), "Person with given UUID in the database!"

        result = customer_verifier_with_passing_bik.verify(new_customer)

        assert result.user_id == new_uuid, "Must represent the same person"
        assert result.status == Status.VERIFICATION_PASSED
        # Chcemy się upewnić, że doszło do zapisu w bazie danych
        assert repository.find_by_user_id(new_uuid) is not None

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
        return InMemoryVerificationRepository()

    @pytest.fixture
    def existing_verified_person(
        self,
        verified_non_fraud: VerifiedPerson,
        repository: VerificationRepository,
    ) -> VerifiedPerson:
        """Symulujemy, że osoba została zapisana w bazie danych wcześniej."""
        repository.save(verified_non_fraud)
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
