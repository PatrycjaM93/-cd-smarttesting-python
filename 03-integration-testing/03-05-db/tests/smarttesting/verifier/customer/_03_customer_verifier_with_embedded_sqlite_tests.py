import uuid
from datetime import date

import injector
import pytest
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
from sqlalchemy.orm import Session, sessionmaker
from tests.smarttesting.verifier.customer.exception_throwing_bik_service import (
    ExceptionThrowingBikService,
)


class Test03CustomerVerifierWithEmbeddedSqlite:
    """Klasa testowa podnosząca cały kontekst aplikacji.

    Rozszerzamy kontener o dodatkowe moduły specyficzne w tym teście aby zapewnić
    dostęp do bazy danych sqlite w pamięci oraz odpowiednio ją zainicjować
    (patrz `EmbeddedSqliteDb` poniżej).
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.container = injector.Injector(
            modules=[ModuleOverridingBikImplementation(), EmbeddedSqliteDb()],
            parent=assemble(),
        )

    @pytest.mark.usefixtures("saved_verification_result_for_zbigniew")
    def test_successfully_verifies_a_customer_when_previously_verified(
        self,
        verifier: CustomerVerifier,
        zbigniew: Customer,
        repository: VerificationRepository,
    ) -> None:
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


class EmbeddedSqliteDb(injector.Module):
    @injector.provider
    @injector.singleton
    def session(self) -> Session:
        """Ten provider będzie zwracał tę samą Sesję przez cały test.

        Jest to istotne ze względu na specyfikę sqlite-in-memory w SQLAlchemy.
        Każde kolejne połączenie dostałoby pustą bazę.

        Z tego też powodu w tym samym miejscu konfigurujemy od razu `engine`
        oraz tworzymy schemat używając `Base.metadata.create_all`.
        """
        engine = create_engine("sqlite:///:memory:")
        session_factory = sessionmaker(bind=engine)
        session = session_factory()
        Base.metadata.create_all(session.connection())  # pylint: disable=no-member
        return session
