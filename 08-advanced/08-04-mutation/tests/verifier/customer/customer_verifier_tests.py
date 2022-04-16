import uuid
from datetime import date

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification


class TestCustomerVerifier:
    @pytest.fixture()
    def too_young_stefan(self) -> Customer:
        return Customer(
            uuid.uuid4(),
            Person("Stefan", "Stefanowski", date.today(), Gender.MALE, "1234567890"),
        )

    def test_should_collect_verification_results(
        self, too_young_stefan: Customer
    ) -> None:
        verifications = {FirstVerification(), SecondVerification()}
        verifier = CustomerVerifier(verifications)

        results = verifier.verify(too_young_stefan)

        assert set(results) == {
            VerificationResult("first", False),
            VerificationResult("second", True),
        }


class FirstVerification(Verification):
    def passes(self, person: Person) -> VerificationResult:
        return VerificationResult(self.name, False)

    @property
    def name(self) -> str:
        return "first"


class SecondVerification(Verification):
    def passes(self, person: Person) -> VerificationResult:
        return VerificationResult(self.name, True)

    @property
    def name(self) -> str:
        return "second"
