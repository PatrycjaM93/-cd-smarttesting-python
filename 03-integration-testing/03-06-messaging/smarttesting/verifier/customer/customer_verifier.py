from dataclasses import dataclass
from typing import Protocol, Set

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import VerifiedPerson
from smarttesting.verifier.verification import Verification


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

    _verifications: Set[Verification]
    _repository: VerificationRepository
    _fraud_alert_task: FraudAlertTask

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        """Główna metoda biznesowa. Weryfikuje czy dana osoba jest oszustem.

        W pozytywnym przypadku (jest oszustem) wysyła wiadomość do brokera.
        Zapisuje rezultat weryfikacji w bazie danych.
        """
        if not self._is_fraud(customer):
            return CustomerVerificationResult.create_passed(customer.uuid)

        result = CustomerVerificationResult.create_failed(customer.uuid)
        # Wykonaj zadanie w tle jeśli znaleziono oszusta
        customer_verification = CustomerVerification(customer.person, result)
        self._fraud_alert_task.delay(customer_verification=customer_verification)

        self._save_verification_result(customer, result)
        return result

    def _is_fraud(self, customer: Customer) -> bool:
        person = customer.person
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )
        return not verifications_passed

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
