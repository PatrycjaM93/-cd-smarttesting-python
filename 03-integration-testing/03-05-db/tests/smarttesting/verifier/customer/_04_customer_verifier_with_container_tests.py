import uuid
from datetime import date
from time import sleep
from typing import Generator

import docker
import injector
import pytest
from docker.models.containers import Container
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.smart_testing_application import assemble
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import Status
from smarttesting.verifier.customer.customer_verifier import CustomerVerifier
from smarttesting.verifier.customer.verification_repository import (
    VerificationRepository,
)
from smarttesting.verifier.customer.verified_person import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from tests.smarttesting.verifier.customer.exception_throwing_bik_service import (
    ExceptionThrowingBikService,
)


@pytest.fixture
def postgresql(random_port: int) -> Generator[str, None, None]:
    """Fikstura startująca w tle kontener z PostgreSQL na losowym porcie.

    Zwraca DSN, który można wykorzystać do ustawienia połączenia w SQLAlchemy.
    """
    client = docker.from_env()
    db_container: Container = client.containers.run(
        "postgres:12",
        detach=True,
        ports={
            5432: random_port,
        },
        environment={"POSTGRES_PASSWORD": "pass"},
    )
    connection_string = f"postgresql://postgres:pass@localhost:{random_port}/postgres"
    _wait_until_server_is_ready(connection_string)
    yield connection_string
    db_container.remove(force=True)


@pytest.mark.uses_docker
class Test04CustomerVerifierWithContainer:
    """Klasa testowa podnosząca cały kontekst aplikacji.

    Rozszerzamy kontener o dodatkowe moduły specyficzne w tym teście aby zapewnić
    dostęp do bazy danych PostgreSQL uruchamianej osobno w kontenerze oraz odpowiednio
    ją zainicjować.
    """

    @pytest.fixture(autouse=True)
    def setup(self, postgresql: str) -> None:  # pylint: disable=redefined-outer-name
        self.container = injector.Injector(
            modules=[
                ModuleOverridingBikImplementation(),
                ContainerPostgreSQLDb(postgresql),
            ],
            parent=assemble(),
        )

    @pytest.mark.usefixtures("saved_verification_result_for_zbigniew")
    def test_successfully_verifies_a_customer_when_previously_verified(
        self,
        repository: VerificationRepository,
        verifier: CustomerVerifier,
        zbigniew: Customer,
    ) -> None:
        """Test weryfikujący, że wykorzystany zostanie zapisany rekord w bazie.

        W innym przypadku doszłoby do próby odpytania BIKu i rzucony zostałby wyjątek.
        """
        assert repository.find_by_user_id(zbigniew.uuid) is not None

        result = verifier.verify(zbigniew)

        assert result.user_id == zbigniew.uuid
        assert result.status == Status.VERIFICATION_PASSED

    @pytest.fixture
    def zbigniew(self, young_zbigniew: Person) -> Customer:
        return Customer(
            uuid.UUID("89c878e3-38f7-4831-af6c-c3b4a0669022"), young_zbigniew
        )

    @pytest.fixture
    def young_zbigniew(self) -> Person:
        return Person("", "", date.today(), Gender.MALE, "18210116954")

    @pytest.fixture
    def verifier(self) -> CustomerVerifier:
        return self.container.get(CustomerVerifier)

    @pytest.fixture
    def repository(self) -> VerificationRepository:
        return self.container.get(VerificationRepository)  # type: ignore

    @pytest.fixture
    def saved_verification_result_for_zbigniew(self) -> None:
        """Fikstura wrzucająca do bazy rezultat sprawdzenia.

        Jest ona użyta automatycznie pomimo braku wymienienia na liscie argumentów
        funkcji testowej dzięki dekoratorowi @pytest.mark.usefixtures(...).
        """
        conn = self.container.get(Session).connection()
        conn.execute(
            """
            INSERT INTO verified
            (uuid, national_identification_number, status)
            VALUES(
                '89c878e3-38f7-4831-af6c-c3b4a0669022',
                '1234567890',
                'VERIFICATION_PASSED'
            )
        """
        )


class ModuleOverridingBikImplementation(injector.Module):
    @injector.provider
    def bik_verification_service(self) -> BIKVerificationService:
        return ExceptionThrowingBikService()


class ContainerPostgreSQLDb(injector.Module):
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    @injector.provider
    @injector.singleton
    def session(self) -> Session:
        """Ten provider będzie zwracał tę samą Sesję przez cały test."""
        engine = create_engine(self._connection_string)
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        Base.metadata.create_all(session.connection())  # pylint: disable=no-member
        return session


def _wait_until_server_is_ready(dsn: str) -> None:
    """Oczekiwanie przez maksymalnie 10 sekund aż serwer będzie gotowy."""
    for _ in range(50):
        try:
            create_engine(dsn).execute("SELECT 1")
        except OperationalError:
            sleep(0.1)
            continue
        else:
            return

    raise TimeoutError("Test DB server was not ready in time!")
