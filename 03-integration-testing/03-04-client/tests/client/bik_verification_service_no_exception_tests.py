import uuid
from datetime import date

import pytest
from requests import Session
from smarttesting.client.bik_verification_service import BIKVerificationService
from smarttesting.client.customer import Customer
from smarttesting.client.customer_verification_result import Status
from smarttesting.client.person import Gender, Person
from tests.client.wiremock_running_test import WiremockRunningTest
from wiremock.client import (
    HttpMethods,
    Mapping,
    MappingRequest,
    MappingResponse,
    Mappings,
)
from wiremock.resources.mappings import ResponseFaultType


class SessionWithDefaultTimeout(Session):
    """Prosta klasa opakowująca `Session` z requests, które zawsze będzie
    używać timeoutu.
    """

    __TIMEOUT = 1

    def request(self, *args, **kwargs):  # pylint: disable=signature-differs
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self.__TIMEOUT
        return super().request(*args, **kwargs)


class TestBIKVerificationServiceDefault(WiremockRunningTest):
    """Klasa testowa wykorzystująca ręcznie ustawione wartości połączenia po HTTP.

    W tym przypadku, domyślna implementacja BIKVerificationService, w przypadku błędu
    zaloguje informacje o wyjątku.

    W tej klasie testowej pokazujemy jak powinniśmy przetestować naszego klienta HTTP.
    Czy potrafimy obsłużyć wyjątki? Czy potrafimy obsłużyć scenariusze biznesowe?

    O problemach związanych z pisaniem zaślepek przez konsumenta API, będziemy mówić
    w dalszej części szkolenia. Tu pokażemy ręczne zaślepianie scenariuszy biznesowych.
    """

    @pytest.fixture()
    def service(self, session: Session) -> BIKVerificationService:
        """Przez initializer wstrzykujemy adres naszego serwera WireMock, zamiast
        domyślnego serwera Biura Informacji Kredytowej. Podajemy też skonfigurowaną
        instancję klienta HTTP.
        """
        return BIKVerificationService(
            f"http://{self.WIREMOCK_HOST}:{self.WIREMOCK_PORT}/", session
        )

    @pytest.fixture()
    def session(self) -> Session:
        """Tworzymy instancję klasy pochodnej od `Session`, która będzie wymuszać
        timeout na żądaniach.
        """
        return SessionWithDefaultTimeout()

    def test_returns_positive_verification(
        self, service: BIKVerificationService
    ) -> None:
        # Zaślepiamy wywołanie GET, zwracając odpowiednią wartość tekstową
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(body="VERIFICATION_PASSED"),
            )
        )

        result = service.verify(self._zbigniew())

        assert result.status == Status.VERIFICATION_PASSED

    def test_returns_negative_verification(
        self, service: BIKVerificationService
    ) -> None:
        # Zaślepiamy wywołanie GET, zwracając odpowiednią wartość tekstową
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(body="VERIFICATION_FAILED"),
            )
        )

        result = service.verify(self._zbigniew())

        assert result.status == Status.VERIFICATION_FAILED

    def test_fails_with_connection_reset_by_peer(
        self, service: BIKVerificationService
    ) -> None:
        # W tym i kolejnych testach zaślepiamy wywołanie GET zwracając różne
        # błędy techniczne. Chcemy się upewnić, że potrafimy je obsłużyć.
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(fault="CONNECTION_RESET_BY_PEER"),
            )
        )

        result = service.verify(self._zbigniew())

        assert result.status == Status.VERIFICATION_FAILED

    def test_fails_with_empty_response(self, service: BIKVerificationService) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(fault=ResponseFaultType.EMPTY_RESPONSE),
            )
        )

        result = service.verify(self._zbigniew())

        assert result.status == Status.VERIFICATION_FAILED

    def test_fails_with_malformed_response(
        self, service: BIKVerificationService
    ) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(
                    fault=ResponseFaultType.MALFORMED_RESPONSE_CHUNK
                ),
            )
        )

        result = service.verify(self._zbigniew())

        assert result.status == Status.VERIFICATION_FAILED

    def test_fails_with_random(self, service: BIKVerificationService) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(
                    fault=ResponseFaultType.RANDOM_DATA_THEN_CLOSE
                ),
            )
        )

        result = service.verify(self._zbigniew())

        assert result.status == Status.VERIFICATION_FAILED

    def _zbigniew(self) -> Customer:
        return Customer(uuid.uuid4(), self._young_zbigniew())

    def _young_zbigniew(self) -> Person:
        return Person("", "", date.today(), Gender.MALE, "18210116954")
