from typing import Set

import injector
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verifier import (
    CustomerVerifier,
    FraudAlertTask,
)
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.verification import Verification


class CustomerModule(injector.Module):
    """Moduł injectora dla modułu klienta."""

    @injector.provider
    def bik_verification_service(self) -> BIKVerificationService:
        return BIKVerificationService("http://localhost")

    @injector.provider
    def customer_verifier(
        self,
        bik_verification_service: BIKVerificationService,
        verifications: Set[Verification],
        repo: VerificationRepository,
        fraud_alert_task: FraudAlertTask,
    ) -> CustomerVerifier:
        return CustomerVerifier(
            bik_verification_service, verifications, repo, fraud_alert_task
        )
