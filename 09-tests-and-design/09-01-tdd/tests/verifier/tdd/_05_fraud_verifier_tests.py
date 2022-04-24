from dataclasses import dataclass
from enum import Enum
from typing import TypedDict

import pytest


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


class TestFraudVerifier:
    def test_should_return_fraud_when_client_has_debt(
        self, client_payload_with_debt: ClientPayload
    ) -> None:
        verifier = FraudVerifier()

        result = verifier.verify(client_payload_with_debt)

        assert result.status == VerificationStatus.FRAUD

    def test_should_return_not_fraud_when_client_has_no_debt(
        self, client_payload_without_debt: ClientPayload
    ) -> None:
        verifier = FraudVerifier()

        result = verifier.verify(client_payload_without_debt)

        assert result.status == VerificationStatus.NOT_FRAUD

    @pytest.fixture()
    def client_payload_with_debt(self) -> ClientPayload:
        return {"has_debt": True}

    @pytest.fixture()
    def client_payload_without_debt(self) -> ClientPayload:
        return {"has_debt": False}
