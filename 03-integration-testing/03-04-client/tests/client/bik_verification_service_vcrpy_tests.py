import pathlib
import uuid
from datetime import date

import pytest
import vcr
from smarttesting.client.bik_verification_service import BIKVerificationService
from smarttesting.client.customer import Customer
from smarttesting.client.person import Gender, Person

test_dir = pathlib.Path(__file__).parent


class TestBIKVerificationServiceVcrPy:
    """vcr.py w akcji."""

    URL = "http://dangerous-pesel-check.com/checkPesel/"

    @pytest.fixture()
    def service(self) -> BIKVerificationService:
        return BIKVerificationService(self.URL)

    @vcr.use_cassette(str(test_dir / "invalid_national_id_number.yaml"))
    def test_returns_failed_verification_unexpected_message_returned(
        self, service: BIKVerificationService
    ) -> None:
        customer = self._zbigniew("000000000")

        result = service.verify(customer)

        assert not result.passed

    @vcr.use_cassette(str(test_dir / "valid_national_id_number.yaml"))
    def test_verification_for_valid_national_id_number(
        self, service: BIKVerificationService
    ) -> None:
        customer = self._zbigniew("18210116954")

        result = service.verify(customer)

        assert result.passed

    def _zbigniew(self, national_id_no: str) -> Customer:
        return Customer(uuid.uuid4(), self._young_zbigniew(national_id_no))

    def _young_zbigniew(self, national_id_no: str) -> Person:
        return Person("", "", date.today(), Gender.MALE, national_id_no)
