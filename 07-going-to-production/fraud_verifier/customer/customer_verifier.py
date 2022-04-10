from dataclasses import dataclass
from typing import Set

from fraud_verifier.customer.customer import Customer
from fraud_verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from fraud_verifier.customer.verification.new_type_of_verification import (
    NewTypeOfVerification,
)
from fraud_verifier.feature_toggles.features import Feature
from fraud_verifier.feature_toggles.manager import FeatureManager
from fraud_verifier.metrics import verify_customer_timer
from fraud_verifier.verification import Verification


@dataclass
class CustomerVerifier:
    _feature_manager: FeatureManager
    _verifications: Set[Verification]

    @verify_customer_timer.time()
    def verify(self, customer: Customer) -> CustomerVerificationResult:
        person = customer.person

        verifications = self._verifications.copy()
        if self._feature_manager.is_enabled(Feature.NEW_VERIFICATION):
            verifications.add(NewTypeOfVerification())

        verifications_passed = all(
            verification.passes(person) for verification in verifications
        )

        if verifications_passed:
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)
