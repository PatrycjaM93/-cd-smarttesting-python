from typing import List, NewType, cast

import injector
from celery import Celery, Task
from kombu.serialization import register
from smarttesting import serialization
from smarttesting.verifier.customer.fraud_alert_task import FraudAlertTask
from smarttesting.verifier.customer.fraud_detected_handler import fraud_detected_handler
from smarttesting_main.task import task_with_injectables

CeleryConfig = NewType("CeleryConfig", object)


class CeleryModule(injector.Module):
    def __init__(self) -> None:
        register(
            "dataclasses_serialization",
            serialization.dataclass_dump,
            serialization.dataclass_load,
            content_type="application/json",
            content_encoding="utf-8",
        )

    @injector.singleton
    @injector.provider
    def celery(self, container: injector.Injector, config: CeleryConfig) -> Celery:
        app = Celery(config_source=config)
        app.__injector__ = container
        return app

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
