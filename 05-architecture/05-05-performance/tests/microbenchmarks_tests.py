"""Wykorzystujemy bibliotekę pytest-benchmark."""
import uuid
from datetime import date
from unittest.mock import Mock

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.fraud_alert_task import FraudAlertTask
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)


@pytest.fixture()
def verifier() -> CustomerVerifier:
    return CustomerVerifier(
        _bik_verification_service=Mock(spec_set=BIKVerificationService),
        _verifications=set(),
        _repository=Mock(
            spec_set=VerificationRepository, find_by_user_id=Mock(return_value=None)
        ),
        _fraud_alert_task=Mock(spec_set=FraudAlertTask),
    )


@pytest.fixture()
def customer() -> Customer:
    return Customer(
        _uuid=uuid.uuid4(),
        _person=Person(
            _name="Fraud",
            _surname="Fraudowski",
            _date_of_birth=date.today(),
            _gender=Gender.MALE,
            _national_id_number="1234567890",
        ),
    )


def test_processing_fraud(  # pylint: disable=redefined-outer-name
    verifier: CustomerVerifier, customer: Customer, benchmark: BenchmarkFixture
) -> None:
    """Test micro-benchmarkowy.

    Sprawdza jak szybki jest algorytm weryfikujący czy klient jest oszustem.
    """
    benchmark(verifier.verify, customer)
