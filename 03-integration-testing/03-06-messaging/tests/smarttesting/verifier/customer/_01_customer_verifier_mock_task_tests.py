import uuid
from datetime import date
from unittest.mock import Mock

import pytest
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
from smarttesting.verifier.customer.fraud_alert_task import fraud_detected_handler
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from sqlalchemy.orm import Session
from tests.smarttesting.verifier.customer.always_failing_verification import (
    AlwaysFailingVerification,
)


class Test01CustomerVerifierMockMessaging:
    """
    W tej klasie testowej:
    - piszemy test dla CustomerVerifiera i mockujemy komponent wysyłający wiadomości
    - piszemy test dla komponentu wysyłającego wiadomość
    - piszemy test dla nasłuchiwacza wiadomości
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.repo = Mock(spec_set=VerificationRepository)

    @pytest.fixture()
    def fraud_person(self) -> Person:
        return Person("Fraud", "Fraudowski", date.today(), Gender.MALE, "1234567890")

    def test_schedules_a_task_with_fraud_details_when_found_a_fraud_using_mocks(
        self, fraud_person: Person
    ) -> None:
        """W tym teście testujemy serwis aplikacyjny, a mockujemy task.

        Nie testujemy żadnej integracji, działamy na mockach. Testy są szybkie -
        mogłyby być tak napisane dla corowej części naszej domeny.
        """
        task_mock = Mock(FraudAlertTask)
        customer = Customer(uuid.uuid4(), fraud_person)

        self._always_failing_verifier(task_mock).verify(customer)

        expected_verification = self._fraud_verification(fraud_person, customer.uuid)
        task_mock.delay.assert_called_once_with(
            customer_verification=expected_verification
        )

    def test_fraud_alert_task_stores_fraud(self, fraud_person: Person) -> None:
        """W tym teście weryfikujemy, czy task potrafi zapisać obiekt w bazie danych.

        Ten test nie integruje się z kolejką zadań czy brokerem, więc nie mamy pewności
        czy potrafimy zdeserializować wiadomość. Z punktu widzenia taska zapis do bazy
        danych jest efektem ubocznym więc możemy rozważyć użycie mocka.
        """
        session_mock = Mock(spec_set=Session)
        random_uuid = uuid.uuid4()
        verification = self._fraud_verification(fraud_person, random_uuid)

        fraud_detected_handler(
            self.repo, session_mock, customer_verification=verification
        )

        self.repo.save.assert_called_once()
        verified_person_called_with, *_ = self.repo.save.mock_calls[0].args
        assert verified_person_called_with.uuid == str(random_uuid)
        session_mock.commit.assert_called_once()

    def _always_failing_verifier(self, task: Mock) -> CustomerVerifier:
        return CustomerVerifier({AlwaysFailingVerification()}, self.repo, task)

    def _fraud_verification(
        self, fraud_person: Person, customer_uuid: uuid.UUID
    ) -> CustomerVerification:
        result = CustomerVerificationResult.create_failed(customer_uuid)
        return CustomerVerification(person=fraud_person, result=result)
