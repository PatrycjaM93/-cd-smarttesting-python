import logging

import polling
import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Person
from smarttesting.verifier.customer._01_customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification


@pytest.fixture()
def verifier() -> CustomerVerifier:
    return CustomerVerifier(
        _verifications={ExceptionThrowingVerification()},
        _fraud_alert_task=None,
    )


class ExceptionThrowingVerification(Verification):
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def passes(self, person: Person) -> VerificationResult:
        self._logger.info("Running this in a separate thread")
        raise ValueError("Boom!")

    @property
    def name(self) -> str:
        return "exception"


class Test07ExceptionThrowingVerification:
    @pytest.mark.skip
    def test_should_handle_exceptions_gracefully_when_dealing_with_results(
        self,
        verifier: CustomerVerifier,  # pylint: disable=redefined-outer-name
        stefan: Customer,
    ) -> None:
        """Zakładamy, z punktu widzenia biznesowego, że potrafimy obsłużyć sytuację
        rzucenia wyjątku.

        W naszym przypadku jest to uzyskanie wyniku procesowania klienta nawet jeśli
        wyjątek został rzucony. Nie chcemy sytuacji, w której rzucony błąd wpłynie na nasz
        proces biznesowy.

        Odkomentuj dekorator `@pytest.mark.skip`, żeby przekonać się, że test może
        nie przejść!
        """
        results = verifier.verify(stefan)

        polling.poll(
            lambda: results == [VerificationResult("exception", False)],
            step=0.1,
            timeout=5,
        )

    def test_should_handle_exceptions_gracefully_when_dealing_with_results_passing(
        self,
        verifier: CustomerVerifier,  # pylint: disable=redefined-outer-name
        stefan: Customer,
    ) -> None:
        """
        Poprawiamy problem z kodu wyżej. Metoda produkcyjna
        `CustomerVerifier.verify_no_exceptions` potrafi obsłużyć rzucony wyjątek z
        osobnego wątku.
        """
        results = verifier.verify_no_exceptions(stefan)

        polling.poll(
            lambda: results == [VerificationResult("exception", False)],
            step=0.1,
            timeout=5,
        )
