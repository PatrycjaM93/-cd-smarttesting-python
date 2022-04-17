import logging
import time
from queue import Queue
from threading import Thread

from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.fraud_alert_task import FraudAlertTask, TaskResult


class FraudAlertHandler(FraudAlertTask):
    """Implementacja zadania uruchamiająca sobie metodę procesującą w tle."""

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def delay(self, *, customer_verification: CustomerVerification) -> TaskResult:
        """'Procesowanie' będzie się odbywać w osobnym wątku.

        Używamy kolejki z biblioteki standardowej która gwarantuje nam thread-safety
        oraz prosty sposób do zwrócenia wyniku z wątku.
        """
        queue: Queue = Queue(maxsize=1)

        thread = Thread(
            target=self._process, args=(customer_verification, queue), daemon=True
        )
        thread.start()

        return queue

    def _process(
        self, customer_verification: CustomerVerification, queue: Queue
    ) -> None:
        self._logger.info("Running fraud notification in a new thread")
        time.sleep(2)
        queue.put_nowait(customer_verification.result)
