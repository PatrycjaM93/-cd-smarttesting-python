# pylint: disable=redefined-outer-name
from queue import Queue
from typing import Set
from unittest.mock import patch

import polling
import pytest
from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer._01_customer_verifier import CustomerVerifier
from smarttesting.verifier.customer._04_fraud_alert_handler import FraudAlertHandler
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.fraud_alert_task import FraudAlertTask
from smarttesting.verifier.verification import Verification


class SpyReadyHandler(FraudAlertHandler):
    """Nadpisujemy tylko metodę wykonującą pracę w osobnym wątku."""

    def _process(
        self, customer_verification: CustomerVerification, queue: Queue
    ) -> None:
        self.spy_on_me()
        queue.put_nowait(customer_verification.result)

    def spy_on_me(self) -> None:
        self._logger.info("Hello")


@pytest.fixture()
def fraud_alert_handler() -> FraudAlertTask:
    return SpyReadyHandler()


@pytest.fixture()
def verifier(
    verifications: Set[Verification], fraud_alert_handler: FraudAlertTask
) -> CustomerVerifier:
    return CustomerVerifier(
        _verifications=verifications,
        _fraud_alert_task=fraud_alert_handler,
    )


class Test06AsyncCustomerWithSpyVerifier:
    """Test weryfikujący efekt uboczny w postaci wywołania metody asynchronicznie."""

    def test_should_delegate_work_to_a_separate_thread(
        self,
        verifier: CustomerVerifier,
        stefan: Customer,
        fraud_alert_handler: SpyReadyHandler,
    ) -> None:
        with patch.object(
            SpyReadyHandler, "spy_on_me", wraps=fraud_alert_handler.spy_on_me
        ) as wrapped_spy_on_me:
            verifier.found_fraud(stefan)

            # musi być pod contextmanagerem, inaczej szpieg zostanie wyłączony
            polling.poll(
                lambda: wrapped_spy_on_me.called,
                step=0.1,
                timeout=5,
            )
            wrapped_spy_on_me.assert_called_once()
