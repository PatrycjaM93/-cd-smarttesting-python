import uuid
from datetime import date

import pytest
import responses
from smarttesting.client.bik_verification_service import BIKVerificationService
from smarttesting.client.customer import Customer
from smarttesting.client.person import Gender, Person


class TestBIKVerificationServiceResponses:
    """Biblioteka responses od Sentry w akcji.

    W każdym teście, w którym chcemy odciąć się od API używamy responses.add,
    konfigurując żądanie, na które chcemy przygotować odpowiedź.
    Testy muszą być udekorowane @responses.activate, żeby wszystko zadziałało.
    """

    URL = "https://bardzo-bezpieczny-url.pl/sprawdz/"

    @pytest.fixture()
    def service(self) -> BIKVerificationService:
        return BIKVerificationService(self.URL)

    @responses.activate
    def test_returns_failed_verification_unexpected_message_returned(
        self, service: BIKVerificationService
    ) -> None:
        customer = self._zbigniew()
        responses.add(
            responses.GET,
            self.URL + customer.person.national_id_number,
            status=200,
            json={"message": "Task failed successfully"},
        )

        result = service.verify(customer)

        assert not result.passed

    @responses.activate
    def test_returns_passed_verification_for_verification_passed_response(
        self, service: BIKVerificationService
    ) -> None:
        customer = self._zbigniew()
        responses.add(
            responses.GET,
            self.URL + customer.person.national_id_number,
            status=200,
            body="VERIFICATION_PASSED",
        )

        result = service.verify(customer)

        assert result.passed

    def _zbigniew(self) -> Customer:
        return Customer(uuid.uuid4(), self._young_zbigniew())

    def _young_zbigniew(self) -> Person:
        return Person("", "", date.today(), Gender.MALE, "18210116954")
