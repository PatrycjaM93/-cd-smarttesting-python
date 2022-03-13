from dataclasses import dataclass
from typing import Set
from uuid import UUID

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
    Status,
)
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import VerifiedPerson
from smarttesting.verifier.verification import Verification


@dataclass
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i zapisuje jej wynik w bazie
    danych. Jeśli przy którejś okaże się, że użytkownik jest oszustem, wówczas
    odpowiedni rezultat zostanie zwrócony.
    """

    _bik_verification_service: BIKVerificationService
    _verifications: Set[Verification]
    _repository: VerificationRepository

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        """
        Główna metoda biznesowa. Sprawdza, czy już nie doszło do weryfikacji klienta
        i jeśli rezultat zostanie odnaleziony w bazie danych to go zwraca. W innym
        przypadku zapisuje wynik weryfikacji w bazie danych. Weryfikacja wówczas
        zachodzi poprzez odpytanie BIKu o stan naszego klienta.
        """
        prior_result = self._repository.find_by_user_id(customer.uuid)
        if prior_result:
            return CustomerVerificationResult(
                UUID(prior_result.uuid), Status(prior_result.status)
            )
        else:
            return self._verify_customer(customer)

    def _verify_customer(self, customer: Customer) -> CustomerVerificationResult:
        result = self._perform_checks(customer)
        self._save_verification_result(customer, result)
        return result

    def _perform_checks(self, customer: Customer) -> CustomerVerificationResult:
        external_result = self._bik_verification_service.verify(customer)

        person = customer.person
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )

        if external_result.passed and verifications_passed:
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)

    def _save_verification_result(
        self, customer: Customer, result: CustomerVerificationResult
    ) -> None:
        self._repository.save(
            VerifiedPerson(
                uuid=str(customer.uuid),
                national_identification_number=customer.person.national_id_number,
                status=result.status.value,
            )
        )
