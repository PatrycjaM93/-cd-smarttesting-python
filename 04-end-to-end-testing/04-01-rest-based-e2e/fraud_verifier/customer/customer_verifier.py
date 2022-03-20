from dataclasses import dataclass
from typing import Set

from fraud_verifier.customer.customer import Customer
from fraud_verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from fraud_verifier.verification import Verification


@dataclass
class CustomerVerifier:
    _verifications: Set[Verification]

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        person = customer.person
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )

        if verifications_passed:
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)
