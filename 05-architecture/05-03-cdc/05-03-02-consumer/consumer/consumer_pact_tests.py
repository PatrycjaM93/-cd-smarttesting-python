import copy
from datetime import date
from pathlib import Path
from uuid import UUID

import pytest
from consumer import CustomerCheckPayload, check_customer
from pact import Consumer, Pact, Provider

CONSUMER_DIR = Path(__file__).parent


@pytest.fixture(scope="module")
def pact_with_fraud_verify() -> Pact:
    pact = Consumer("some_consumer").has_pact_with(
        Provider("FraudVerify"), port=5001, pact_dir=CONSUMER_DIR
    )
    pact.start_service()
    yield pact
    pact.stop_service()


class TestPactIoBased:
    def test_returns_true_if_verification_successful(
        self, pact_with_fraud_verify: Pact  # pylint: disable=redefined-outer-name
    ) -> None:
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

        pact_payload = _get_json_friendly_payload(payload)
        headers = {"Content-Type": "application/json"}
        pact_with_fraud_verify.given(
            "Fraud verification accepts trusted data"
        ).upon_receiving("A fraud user sends their data").with_request(
            "POST", "/fraudCheck", body=pact_payload, headers=headers
        ).will_respond_with(
            200
        )

        with pact_with_fraud_verify:
            result = check_customer(payload)

        assert result is True

    def test_returns_false_if_verification_unsuccessful(
        self, pact_with_fraud_verify: Pact  # pylint: disable=redefined-outer-name
    ) -> None:
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

        pact_payload = _get_json_friendly_payload(payload)
        headers = {"Content-Type": "application/json"}
        pact_with_fraud_verify.given(
            "Fraud verification rejects suspicious data"
        ).upon_receiving("An honest user sends their data").with_request(
            "POST", "/fraudCheck", body=pact_payload, headers=headers
        ).will_respond_with(
            401
        )

        with pact_with_fraud_verify:
            result = check_customer(payload)

        assert result is False


def _get_json_friendly_payload(payload: CustomerCheckPayload) -> dict:
    """Niestety nie ma w Pact możliwości użycia swojego JSONEncodera.

    Przekonwertujemy typy na lubiane przez json.dumps ręcznie.
    """
    pact_payload: dict = copy.deepcopy(payload)  # type: ignore
    pact_payload["uuid"] = str(pact_payload["uuid"])
    pact_payload["person"]["date_of_birth"] = pact_payload["person"][
        "date_of_birth"
    ].strftime("%Y-%m-%d")
    return pact_payload
