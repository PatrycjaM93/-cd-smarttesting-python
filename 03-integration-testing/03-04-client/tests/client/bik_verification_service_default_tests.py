import uuid
from datetime import date

import pytest
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


class TestBIKVerificationServiceDefault(WiremockRunningTest):
    @pytest.mark.skip("Pomijamy, ponieważ wisi w nieskończoność")
    def test_fails_with_connection_reset_by_peer(self):
        """
        Jeśli odkomentujemy ten test - nigdy się nie zakończy. Dlatego, że wartości
        domyślne timeout'u w `requests` zakładają nieskończone oczekiwanie.
        :return:
        """
        # Mówimy zaślepce serwera HTTP, żeby odpowiedziała błędem resetującym
        # połączenie. Dobrze skonfigurowany klient HTTP powinien rzucić wyjątkiem
        # po określonym czasie.
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/18210116954"),
                response=MappingResponse(fault="CONNECTION_RESET_BY_PEER"),
            )
        )

        service = BIKVerificationService(
            f"http://{self.WIREMOCK_HOST}:{self.WIREMOCK_PORT}/"
        )

        person = Person("", "", date.today(), Gender.MALE, "18210116954")
        customer = Customer(uuid.uuid4(), person)
        result = service.verify(customer)

        assert result.status == Status.VERIFICATION_FAILED
