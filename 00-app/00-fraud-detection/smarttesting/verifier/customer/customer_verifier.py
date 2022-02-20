import logging
from dataclasses import dataclass
from typing import Protocol, Set
from uuid import UUID

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
    Status,
)
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import VerifiedPerson
from smarttesting.verifier.verification import Verification


logger = logging.getLogger(__name__)


class TaskResult(Protocol):
    """Prosty protokół opakowujący AsyncResult z Celery"""

    def get(self) -> None:
        pass


class FraudAlertTask(Protocol):
    """Prosty protokół opakowaujący taska celery z danym argumentem."""

    def delay(self, *, customer_verification: CustomerVerification) -> TaskResult:
        ...


@dataclass
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i jeśli, przy którejś okaże się,
    że użytkownik jest oszustem, wówczas wysyłamy wiadomość do brokera, z informacją
    o oszuście.
    """

    _bik_verification_service: BIKVerificationService
    _verifications: Set[Verification]
    _repository: VerificationRepository
    _fraud_alert_task: FraudAlertTask

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
        if not result.passed:
            customer_verification = CustomerVerification(customer.person, result)
            self._fraud_alert_task.delay(customer_verification=customer_verification)
        return result

    def _perform_checks(self, customer: Customer) -> CustomerVerificationResult:
        logger.info("Customer with ID %s not found in the database. Will calculate the new result", customer.uuid)
        external_result = self._bik_verification_service.verify(customer)
        logger.info("The result from BIK was %s", external_result)

        person = customer.person
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )
        logger.info("The result from other checks was %s", verifications_passed)

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
