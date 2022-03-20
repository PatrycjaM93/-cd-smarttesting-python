import json

import pytest
from e2e.tests import constants
from e2e.tests.factories import AdultMaleCustomerFactory
from e2e.tests.schemas import CustomerSchema


@pytest.fixture()
def adult_male_customer_payload() -> str:
    customer = AdultMaleCustomerFactory.build()
    schema = CustomerSchema()
    dict_repr = schema.dump(customer)
    return json.dumps({"customer": dict_repr})


@pytest.fixture()
def fraud_service_url() -> str:
    return constants.LOAN_ORDERS_URI
