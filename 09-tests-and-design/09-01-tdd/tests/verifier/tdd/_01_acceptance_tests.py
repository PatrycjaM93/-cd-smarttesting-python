# pylint: disable=assignment-from-no-return
"""Wyłączamy czujnego pylinta, który oprotestowuje (słusznie!) niedokończony kod."""
from typing import Any

import pytest


class Test01Acceptance:
    """Kod do slajdów [Zacznijmy od testu]."""

    @pytest.mark.xfail
    def test_verifies_a_client_with_debt_as_fraud(self) -> None:
        fraud = self._client_with_debt()

        verification = self._verify_client(fraud)

        self._assert_is_verified_as_fraud(verification)

    def _client_with_debt(self):
        pass

    def _verify_client(self, client):
        pass

    def _assert_is_verified_as_fraud(self, verification: Any):
        assert verification is not None
