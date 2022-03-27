from typing import Protocol

from smarttesting.verifier.customer.customer_verification import CustomerVerification


class TaskResult(Protocol):
    """Prosty protokół opokowujący AsyncResult z Celery."""

    def get(self) -> None:
        ...


class FraudAlertTask(Protocol):
    """Prosty protokół opakowaujący taska celery z danym argumentem."""

    def delay(self, *, customer_verification: CustomerVerification) -> TaskResult:
        ...
