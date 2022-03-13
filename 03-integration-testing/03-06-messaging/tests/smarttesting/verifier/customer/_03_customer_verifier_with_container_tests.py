import uuid
from datetime import date

import pytest
from celery import Celery
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.smart_testing_application import assemble
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier


@pytest.mark.uses_docker
class Test03CustomerVerifierWithContainer:
    """W tej klasie testowej piszemy test dla serwisu CustomerVerifier.

    Przed uruchomieniem właściwych testów, dzięki użyciu biblioteki `docker`,
    uruchamiany kontener z Rabbitem.

    Ten test używa konfiguracji maksymalnie zbliżonej do produkcyjnej.
    """

    @pytest.fixture(autouse=True)
    def setup(self, rabbitmq: str) -> None:
        container = assemble(broker_url=rabbitmq)
        self.celery_app = container.get(Celery)
        self.verifier = container.get(CustomerVerifier)

    @pytest.fixture()
    def zbigniew(self) -> Customer:
        person = Person("Fraud", "Fraudowski", date.today(), Gender.MALE, "1234567890")
        customer = Customer(uuid.uuid4(), person)
        return customer

    def test_sends_a_message_to_a_broker_when_fraud_was_found(
        self, zbigniew: Customer
    ) -> None:
        self.verifier.verify(zbigniew)

        pending_tasks = self._get_pending_tasks_from_celery()
        assert len(pending_tasks) == 1
        _args, kwargs, *_rest = pending_tasks[0]
        assert str(zbigniew.uuid) in str(kwargs)

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
