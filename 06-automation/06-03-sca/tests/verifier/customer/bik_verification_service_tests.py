import uuid
from datetime import date
from unittest.mock import Mock, patch

import pytest
from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)


class TestBIKVerificationService:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.service = BIKVerificationService("")

    @pytest.fixture()
    def customer(self) -> Customer:
        return Customer(
            _uuid=uuid.uuid4(),
            _person=Person(
                _name="Pan",
                _surname="Fraudowski",
                _gender=Gender.MALE,
                _date_of_birth=date.today(),
                _national_id_number="12345678011",
            ),
        )

    def test_should_return_successful_verification(self, customer: Customer) -> None:
        result = self.service.verify(customer)

        assert result.passed

    def test_should_return_failed_verification(self, customer: Customer) -> None:
        pass_method_mock = Mock(side_effect=ValueError("BOOM!"))
        with patch.object(BIKVerificationService, "create_passed", pass_method_mock):
            result = self.service.verify(customer)

        assert not result.passed

    def test_not_blow_up_due_to_cyclomatic_complexity(self) -> None:
        result = self.service.complex_method(1, 2, 3)

        assert result == 8
