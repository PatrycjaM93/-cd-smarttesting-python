from enum import Enum
from typing import TypedDict, cast

import injector
import pytest
from flask import Flask, Response, request
from flask_injector import FlaskInjector


class ClientPayload(TypedDict):
    has_debt: bool


class FraudVerifier:
    def verify(self, client: ClientPayload):
        pass


class VerifierModule(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(FraudVerifier, to=FraudVerifier)


app = Flask(__name__)


@app.route("/fraudCheck", methods=["POST"])
def fraud_check(verifier: FraudVerifier):
    payload = cast(ClientPayload, request.json)
    result = verifier.verify(payload)
    return {"status": result.value}


# Musi być po skonfigurowaniu routingu
# https://github.com/alecthomas/flask_injector/issues/23#issuecomment-364600214
FlaskInjector(app, [VerifierModule()])


class VerificationStatus(Enum):
    FRAUD = "FRAUD"
    NOT_FRAUD = "NOT_FRAUD"


class TestFailingFraudVerifier:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.client = app.test_client()

    @pytest.mark.xfail
    def test_verifies_a_client_with_debt_as_fraud(self) -> None:
        fraud = self._client_with_debt_payload()

        verification = self._verify_client(fraud)

        assert verification.json == {"status": VerificationStatus.FRAUD.value}

    @pytest.mark.xfail
    def test_verifies_a_client_without_debt_as_not_fraud(self) -> None:
        fraud = self._client_without_debt_payload()

        verification = self._verify_client(fraud)

        assert verification.json == {"status": VerificationStatus.NOT_FRAUD.value}

    def _client_with_debt_payload(self) -> dict:
        return {"has_debt": True}

    def _client_without_debt_payload(self) -> dict:
        return {"has_debt": False}

    def _verify_client(self, client_payload: dict) -> Response:
        response = self.client.post("/fraudCheck", json=client_payload)
        return cast(Response, response)
