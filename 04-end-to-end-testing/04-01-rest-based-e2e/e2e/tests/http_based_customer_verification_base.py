import pytest
import requests
from e2e.smarttesting.customer.customer import Customer
from e2e.smarttesting.order.loan_order import LoanOrder
from e2e.tests import constants
from e2e.tests.schemas import LoanOrderSchema
from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry  # pylint: disable=import-error


class HttpBasedCustomerVerificationBase:
    RETRY_STRATEGY = Retry(
        total=10,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=["GET", "POST"],
    )

    @pytest.fixture(autouse=True)
    def setup(self):
        # Zastosowanie retry's w celu uniknięcia false failures
        adapter = HTTPAdapter(max_retries=self.RETRY_STRATEGY)
        self._session = requests.Session()
        self._session.mount("http//", adapter)
        self._loan_order_schema = LoanOrderSchema()

    def _create_and_retrieve_loan_order(self, customer: Customer) -> LoanOrder:
        loan_order = LoanOrder(id=None, customer=customer)
        loan_order_id = self._create_loan_order(loan_order)
        loan_order_after_verification = self._retrieve_loan_order(loan_order_id)
        return loan_order_after_verification

    def _create_loan_order(self, loan_order: LoanOrder) -> str:
        payload = self._loan_order_schema.dump(loan_order)
        post_response = self._session.post(constants.LOAN_ORDERS_URI, json=payload)
        return post_response.text

    def _retrieve_loan_order(self, loan_order_id: str) -> LoanOrder:
        get_response = self._session.get(
            constants.LOAN_ORDERS_URI + "/" + loan_order_id
        )
        get_response_json = get_response.json()
        return self._loan_order_schema.load(get_response_json)
