# pylint: disable=redefined-outer-name
from typing import Set
from unittest.mock import Mock

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer._01_customer_verifier import CustomerVerifier
from smarttesting.verifier.customer._04_fraud_alert_handler import FraudAlertHandler
from smarttesting.verifier.customer.fraud_alert_task import FraudAlertTask
from smarttesting.verifier.verification import Verification


@pytest.fixture()
def fraud_alert_handler() -> FraudAlertTask:
    return Mock(spec_set=FraudAlertHandler)


@pytest.fixture()
def verifier(
    verifications: Set[Verification], fraud_alert_handler: FraudAlertTask
) -> CustomerVerifier:
    return CustomerVerifier(
        _verifications=verifications,
        _fraud_alert_task=fraud_alert_handler,
    )


class Test05AsyncCustomerVerifier:
    """Test weryfikujący efekt uboczny w postaci wywołania metody asynchronicznie."""

    def test_should_notify_about_fraud(
        self,
        verifier: CustomerVerifier,
        stefan: Customer,
        fraud_alert_handler: Mock,
    ) -> None:
        verifier.found_fraud(stefan)

        fraud_alert_handler.delay.assert_called_once()
