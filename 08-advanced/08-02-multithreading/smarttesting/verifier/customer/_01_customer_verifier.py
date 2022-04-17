from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Optional, Set

from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Person
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.customer.fraud_alert_task import FraudAlertTask
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification


@dataclass
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i jeśli, przy którejś okaże się,
    że użytkownik jest oszustem, wówczas odpowiedni rezultat zostanie zwrócony.
    """

    _verifications: Set[Verification]
    _fraud_alert_task: Optional[FraudAlertTask]

    def __post_init__(self) -> None:
        verifications_count = len(self._verifications)
        self._executor = ThreadPoolExecutor(max_workers=verifications_count)

    def verify(self, customer: Customer) -> List[VerificationResult]:
        """Wykonuje weryfikacje w wielu wątkach."""
        futures = []

        for verification in self._verifications:
            # zacznij wykonywać wywołania równolegle
            future = self._executor.submit(verification.passes, customer.person)
            futures.append(future)

        # zwróć listę odpowiedzi w kolejności ukończenia
        return [future.result() for future in as_completed(futures)]

    def verify_no_exceptions(self, customer: Customer) -> List[VerificationResult]:
        """Wykonuje weryfikacje w wątkach.

        Uznaje wystąpienie wyjątku za nieudaną weryfikację.
        """
        futures = []

        def consider_exception_a_failed_verification(
            verification: Verification, person: Person
        ) -> VerificationResult:
            try:
                return verification.passes(person)
            except:  # pylint: disable=bare-except  # noqa: E722
                # PS: nie powinniśmy w kodzie produkcyjnym łapać wszystkich wyjątków
                return VerificationResult(verification.name, False)

        for verification in self._verifications:
            # zacznij wykonywać wywołania równolegle
            future = self._executor.submit(
                consider_exception_a_failed_verification, verification, customer.person
            )
            futures.append(future)

        # zwróć listę odpowiedzi w kolejności ukończenia
        return [future.result() for future in as_completed(futures)]

    def verify_async(self, customer: Customer) -> None:
        """Dokonuje weryfikacji w osobnych wątkach."""
        for verification in self._verifications:
            self._executor.submit(verification.passes, customer.person)

    def found_fraud(self, customer: Customer) -> None:
        """Wysyła notyfikację o znalezionym oszuście."""
        assert self._fraud_alert_task is not None

        result = CustomerVerificationResult.create_failed(customer.uuid)
        customer_verification = CustomerVerification(customer.person, result)
        self._fraud_alert_task.delay(customer_verification=customer_verification)

    def close(self) -> None:
        self._executor.shutdown()
