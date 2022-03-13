import uuid
from datetime import date
from typing import Generator
from unittest.mock import patch

import pytest
from requests import Session
from smarttesting.client.bik_verification_service import BIKVerificationService
from smarttesting.client.customer import Customer
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

    W tym przypadku, nasza implementacja BIKVerificationService ma nadpisaną metodę,
    która zamiast logować wyjątek będzie go rzucać.

    W tej klasie testowej pokazujemy jak wysypała by się nasza aplikacja, gdybyśmy
    odpowiednio nie obsłużyli w niej wyjątków.
    """

    @pytest.fixture()
    def service(
        self, session: Session
    ) -> Generator[BIKVerificationService, None, None]:
        """Przez initializer wstrzykujemy adres naszego serwera WireMock, zamiast
        domyślnego serwera Biura Informacji Kredytowej. Podajemy też skonfigurowaną
        instancję klienta HTTP.

        Nadpisujemy też metodę, obsługującą rzucony wyjątek. W tym przypadku będziemy
        go ponownie rzucać.
        """
        service = BIKVerificationService(
            f"http://{self.WIREMOCK_HOST}:{self.WIREMOCK_PORT}/", session
        )

        def reraise(exception: BaseException) -> None:
            raise exception

        with patch.object(service, "_process_exception", reraise):
            yield service

    @pytest.fixture()
    def session(self) -> Session:
        """Tworzymy instancję klasy pochodnej od `Session`, która będzie wymuszać
        timeout na żądaniach.
        """
        return SessionWithDefaultTimeout()

    def test_fails_with_timeout(self, service: BIKVerificationService) -> None:
        # Zwracamy odpowiedź po 5 sekundach
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(fixed_delay_milliseconds=5000),
            )
        )

        # Oczekujemy, że zostanie rzucony wyjątek związany z połączeniem HTTP
        # Według naszej konfiguracji połączenie HTTP powinno być nawiązane w ciągu
        # 1 sekundy
        with pytest.raises(IOError):
            service.verify(self._zbigniew())

    # Ten i kolejne testy rzucają różne typy wyjątków i oczekujemy, że
    # wywołanie naszej metody biznesowej zakończy się rzuceniem wyjątku.
    def test_fails_with_connection_reset_by_peer(
        self, service: BIKVerificationService
    ) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(fault="CONNECTION_RESET_BY_PEER"),
            )
        )

        with pytest.raises(IOError):
            service.verify(self._zbigniew())

    def test_fails_with_empty_response(self, service: BIKVerificationService) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(fault=ResponseFaultType.EMPTY_RESPONSE),
            )
        )

        with pytest.raises(IOError):
            service.verify(self._zbigniew())

    def test_fails_with_malformed(self, service: BIKVerificationService) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(
                    fault=ResponseFaultType.MALFORMED_RESPONSE_CHUNK
                ),
            )
        )

        with pytest.raises(IOError):
            service.verify(self._zbigniew())

    def test_fails_with_random(self, service: BIKVerificationService) -> None:
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(
                    fault=ResponseFaultType.RANDOM_DATA_THEN_CLOSE
                ),
            )
        )

        with pytest.raises(IOError):
            service.verify(self._zbigniew())

    def _zbigniew(self) -> Customer:
        return Customer(uuid.uuid4(), self._young_zbigniew())

    def _young_zbigniew(self) -> Person:
        return Person("", "", date.today(), Gender.MALE, "18210116954")
