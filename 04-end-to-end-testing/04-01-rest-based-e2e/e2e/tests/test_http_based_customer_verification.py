from http import HTTPStatus

import pytest
import requests
from e2e.smarttesting.customer.customer import Customer
from e2e.smarttesting.customer.person import Gender
from e2e.smarttesting.order.loan_order import LoanOrder, Status
from e2e.tests import constants
from e2e.tests.factories import AdultMaleCustomerFactory, CustomerFactory
from e2e.tests.http_based_customer_verification_base import (
    HttpBasedCustomerVerificationBase,
)
from e2e.tests.loan_order_assert import LoanOrderAssert
from e2e.tests.schemas import LoanOrderSchema


class TestHttpBasedCustomerVerification(HttpBasedCustomerVerificationBase):
    def test_sets_order_status_to_verified_when_correct_customer(self) -> None:
        """Test mało czytelny ze względu na zbyt dużo kodu boiler-plate i mieszanie
        poziomów abstrakcji, brak sensownej obsługi timeout'ów."""
        # given
        customer = AdultMaleCustomerFactory.build()
        loan_order = LoanOrder(id=None, customer=customer)
        schema = LoanOrderSchema()
        payload = schema.dump(loan_order)

        # when
        post_response = requests.post(constants.LOAN_ORDERS_URI, json=payload)

        # then
        assert post_response.status_code == HTTPStatus.OK

        # when
        loan_order_id = post_response.text
        get_response = requests.get(constants.LOAN_ORDERS_URI + "/" + loan_order_id)

        # then
        get_response_json = get_response.json()
        returned_loan_order = schema.load(get_response_json)
        assert returned_loan_order.status == Status.VERIFIED

    @pytest.fixture()
    def incorrect_customer(self) -> Customer:
        return CustomerFactory.build(person__gender=Gender.MALE)

    def test_sets_order_status_to_failed_when_incorrect_customer(
        self, incorrect_customer: Customer
    ) -> None:
        """Boiler-plate i setup wyniesiony do fikstur i metod pomocniczych w klasie bazowej.
        Zastosowanie AssertObject pattern"""
        # given w fiksturze
        # when
        loan_order = self._create_and_retrieve_loan_order(incorrect_customer)

        # then
        LoanOrderAssert(loan_order).customer_verification_failed()
