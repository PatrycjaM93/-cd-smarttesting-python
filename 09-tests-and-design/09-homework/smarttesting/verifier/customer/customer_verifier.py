from dataclasses import dataclass
from typing import Set

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.verification import Verification


@dataclass
class CustomerVerifier:
    _verifications: Set[Verification]

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        results = [
            verification.passes(customer.person) for verification in self._verifications
        ]
        if all(results):
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)
