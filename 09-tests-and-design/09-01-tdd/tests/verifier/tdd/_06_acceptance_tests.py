from dataclasses import dataclass
from enum import Enum
from typing import TypedDict, cast

import injector
import pytest
from flask import Flask, Response, request
from flask_injector import FlaskInjector


class ClientPayload(TypedDict):
    has_debt: bool


class VerificationStatus(Enum):
    FRAUD = "FRAUD"
    NOT_FRAUD = "NOT_FRAUD"


@dataclass(frozen=True)
class VerificationResult:
    status: VerificationStatus


class FraudVerifier:
    def verify(self, client: ClientPayload) -> VerificationResult:
        if client["has_debt"]:
            return VerificationResult(VerificationStatus.FRAUD)
        return VerificationResult(VerificationStatus.NOT_FRAUD)


class VerifierModule(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(FraudVerifier, to=FraudVerifier)


app = Flask(__name__)


@app.route("/fraudCheck", methods=["POST"])
def fraud_check(verifier: FraudVerifier):
    payload = cast(ClientPayload, request.json)
    result = verifier.verify(payload)
    return {"status": result.status.value}


# Musi być po skonfigurowaniu routingu
# https://github.com/alecthomas/flask_injector/issues/23#issuecomment-364600214
FlaskInjector(app, [VerifierModule()])


class Test06Acceptance:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.client = app.test_client()

    def test_verifies_a_client_with_debt_as_fraud(self) -> None:
        fraud = self._client_with_debt_payload()

        verification = self._verify_client(fraud)

        self._assert_is_verified_as_fraud(verification)

    def _client_with_debt_payload(self) -> dict:
        return {"has_debt": True}

    def _verify_client(self, client_payload: dict) -> Response:
        response = self.client.post("/fraudCheck", json=client_payload)
        return cast(Response, response)

    def _assert_is_verified_as_fraud(self, verification: Response):
        assert verification.json == {"status": VerificationStatus.FRAUD.value}
