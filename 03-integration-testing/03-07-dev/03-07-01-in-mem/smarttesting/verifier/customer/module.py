from typing import List, Set, cast

import injector
from celery import Celery, Task
from sqlalchemy.orm import Session

from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verifier import (
    CustomerVerifier,
    FraudAlertTask,
)
from smarttesting.verifier.customer.fraud_alert_task import fraud_detected_handler
from smarttesting.verifier.customer.task import task_with_injectables
from smarttesting.verifier.customer.verification_repository import (
    SqlAlchemyVerificationRepository,
    VerificationRepository,
)
from smarttesting.verifier.verification import Verification


class CustomerModule(injector.Module):
    """Moduł injectora dla modułu klienta."""

    @injector.singleton
    @injector.provider
    def fraud_alert_task(self, celery: Celery) -> FraudAlertTask:
        # To robimy zamiast dekorowania funkcji zadania @app.task
        registered_celery_task = celery.task(typing=False)(fraud_detected_handler)
        task_with_injected_dependencies = task_with_injectables(registered_celery_task)
        return cast(FraudAlertTask, task_with_injected_dependencies)

    @injector.multiprovider
    def tasks(self, fraud_alert_task: FraudAlertTask) -> List[Task]:
        # Potrzebne do rejestracji zadań przez Celery
        return [fraud_alert_task]  # type: ignore

    @injector.provider
    def verification_repository(self, session: Session) -> VerificationRepository:
        return SqlAlchemyVerificationRepository(session)

    @injector.provider
    def customer_verifier(
        self,
        verifications: Set[Verification],
        repo: VerificationRepository,
        fraud_alert_task: FraudAlertTask,
        bik_verification_service: BIKVerificationService,
    ) -> CustomerVerifier:
        return CustomerVerifier(
            bik_verification_service, verifications, repo, fraud_alert_task
        )
