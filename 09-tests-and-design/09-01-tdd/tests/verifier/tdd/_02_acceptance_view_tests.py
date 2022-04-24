from enum import Enum
from typing import cast

import pytest
from flask import Flask, Response

app = Flask(__name__)


@app.route("/fraudCheck", methods=["POST"])
def fraud_check():
    pass


class VerificationStatus(Enum):
    FRAUD = "FRAUD"
    NOT_FRAUD = "NOT_FRAUD"


class Test02AcceptanceView:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.client = app.test_client()

    @pytest.mark.xfail
    def test_verifies_a_client_with_debt_as_fraud(self) -> None:
        fraud = self._client_with_debt_payload()

        verification = self._verify_client(fraud)

        self._assert_is_verified_as_fraud(verification)

    def _client_with_debt_payload(self) -> dict:
        return {"has_debt": True}

    def _verify_client(self, client_payload: dict) -> Response:
        response = self.client.post("/fraudCheck", json=client_payload)
        return cast(Response, response)

    def _assert_is_verified_as_fraud(self, verification: Response) -> None:
        assert verification.json() == {"status": VerificationStatus.FRAUD.value}  # type: ignore
