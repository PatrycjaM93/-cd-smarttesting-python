import time
from datetime import date, datetime, timedelta
from urllib.parse import urlparse
from uuid import UUID

import pytest
import requests
from consumer import FRAUD_CHECK_URL, CustomerCheckPayload, check_customer
from requests.exceptions import RequestException


@pytest.mark.uses_docker
class TestSpringCloudContractBased:
    @pytest.fixture(scope="class", autouse=True)
    def make_sure_stub_is_running(self) -> None:
        ping_url = urlparse(FRAUD_CHECK_URL)._replace(path="/ping").geturl()
        stop_at = datetime.now() + timedelta(seconds=30)
        while stop_at > datetime.now():
            try:
                response = requests.get(ping_url)
                response.raise_for_status()
            except RequestException:
                time.sleep(0.3)
                continue
            else:
                break

    def test_returns_false_if_verification_unsuccessful(self) -> None:
        payload: CustomerCheckPayload = {
            "uuid": UUID("89c878e3-38f7-4831-af6c-c3b4a0669022"),
            "person": {
                "name": "Stefania",
                "surname": "Stefanowska",
                "gender": "FEMALE",
                "date_of_birth": date(2020, 1, 1),
                "national_id_number": "1234567890",
            },
        }

        result = check_customer(payload)

        assert result is False

    def test_returns_true_if_verification_successful(self) -> None:
        payload: CustomerCheckPayload = {
            "uuid": UUID("6cb4521f-49da-48e5-9ea2-4a1d3899581d"),
            "person": {
                "name": "Jacek",
                "surname": "Dubilas",
                "gender": "MALE",
                "date_of_birth": date(1980, 3, 8),
                "national_id_number": "80030818293",
            },
        }

        result = check_customer(payload)

        assert result is True
