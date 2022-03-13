import uuid
from datetime import date
from unittest.mock import Mock

import injector
import pytest
from celery import Celery
from smarttesting.celery_module import CeleryModule
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.customer.customer_verifier import (
    CustomerVerifier,
    FraudAlertTask,
)
from smarttesting.verifier.customer.module import CustomerModule
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from tests.smarttesting.verifier.customer.always_failing_verification import (
    AlwaysFailingVerification,
)


class Test02CustomerVerifierInMemoryMessaging:
    """W tej klasie testowej piszemy test dla serwisu CustomerVerifier, który
    wyśle w tło taska jak na produkcji, jednak zamiast produkcyjnego brokera użyjemy
    implementacji działającej w pamięci.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        # Podmieniamy konfigurację Celery tak, by używała brokera in-memory
        # W ten sposób nadal będzie ono przeprowadzać serializację danych,
        # a zadanie trafi do kolejki w pamięci
        container = injector.Injector([CeleryModule("memory://"), CustomerModule()])
        self.celery_app = container.get(Celery)
        self.task = container.get(FraudAlertTask)  # type: ignore
        self.repo = Mock(spec_set=VerificationRepository)

    @pytest.fixture()
    def fraud_person(self) -> Person:
        return Person("Fraud", "Fraudowski", date.today(), Gender.MALE, "1234567890")

    def test_schedules_a_task_with_fraud_details(self, fraud_person: Person) -> None:
        """W tym teście wykorzystujemy implementację brokera działającą w pamięci.

        W momencie, w którym zostaje wysłana wiadomość, ląduje ona w kolejce.
        Wykorzystując system kolejkowy i prawdziwy task, możemy sprawdzić co faktycznie
        trafiło do brokera i ocenić, czy to jest to, co oczekiwaliśmy.

        Ten test weryfikuje konfigurację systemu kolejkowego
        oraz serializację/deserializację wiadomości.
        """
        customer = Customer(uuid.uuid4(), fraud_person)

        self._always_failing_verifier().verify(customer=customer)

        pending_tasks = self._get_pending_tasks_from_celery()
        assert len(pending_tasks) == 1, "Nieoczekiwana liczba oczekujących tasków!"
        _args, kwargs, *_ = pending_tasks[0]
        expected_verification = self._fraud_verification(fraud_person, customer.uuid)
        assert kwargs == {"customer_verification": expected_verification}

    def _always_failing_verifier(self) -> CustomerVerifier:
        return CustomerVerifier({AlwaysFailingVerification()}, self.repo, self.task)

    def _fraud_verification(
        self, fraud_person: Person, customer_uuid: uuid.UUID
    ) -> CustomerVerification:
        result = CustomerVerificationResult.create_failed(customer_uuid)
        return CustomerVerification(person=fraud_person, result=result)

    def _get_pending_tasks_from_celery(self) -> list:
        task_args = []
        with self.celery_app.connection_or_acquire() as conn:
            consumer = self.celery_app.amqp.TaskConsumer(conn)
            consumer.register_callback(
                lambda body, _amqp_message: task_args.append(body)
            )
            with consumer:
                conn.drain_events(timeout=0)

        return task_args
