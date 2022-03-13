import uuid
from datetime import date
from pathlib import Path
from typing import Generator

import pytest
from celery import Celery
from celery.contrib.testing import worker
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.smart_testing_application import assemble
from smarttesting.verifier.customer.customer_verification import CustomerVerification
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.customer.customer_verifier import FraudAlertTask
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)


@pytest.mark.uses_docker
class Test03FraudAlertTask:
    """W tej klasie piszemy test dla taska odpalanego z środka serwisu aplikacyjnego.

    Wywołamy task w ten sam sposób jak robi to serwis aplikacyjny, przechodząc przez
    brokera i wszystkie procesy serializacji i deserializacji wiadomości.
    """

    @pytest.fixture(autouse=True)
    def setup(self, rabbitmq: str, tmp_path: Path) -> None:
        sqlite_path = tmp_path / "test_sqlite.db"
        db_dsn = f"sqlite:///{sqlite_path}"
        container = assemble(broker_url=rabbitmq, db_dsn=db_dsn)
        self.celery_app = container.get(Celery)
        self.task = container.get(FraudAlertTask)  # type: ignore
        self.repository = container.get(VerificationRepository)  # type: ignore

    @pytest.fixture()
    def running_worker(self) -> Generator:
        """Użyjemy funkcji do testowania z Celery, która pozwala uruchamiać workera.

        Koniecznie sprawdź dokumentację Celery - zawiera kilka wbudowanych fikstur
        ułatwiających testowanie, na przykład `celery_worker`.
        https://docs.celeryproject.org/en/stable/userguide/testing.html
        """
        self.celery_app.control.purge()  # czyścimy kolejkę z potencjalnych śmieci
        with worker.start_worker(self.celery_app, perform_ping_check=False):
            yield

    @pytest.fixture()
    def stefania(self) -> Customer:
        person = Person(
            "Stefania", "Stefanowska", date.today(), Gender.FEMALE, "18210145358"
        )
        return Customer(uuid.uuid4(), person)

    @pytest.mark.usefixtures("running_worker")  # <- na czas tego testu pracuje worker
    def test_stores_a_fraud(self, stefania: Customer) -> None:
        verification = CustomerVerification(
            stefania.person, CustomerVerificationResult.create_failed(stefania.uuid)
        )

        # Wysyłamy zadanie na kolejkę
        result = self.task.delay(customer_verification=verification)

        # Czekamy aż zadanie się zakończy
        result.get()
        assert self.repository.find_by_user_id(stefania.uuid) is not None
