# pylint: disable=invalid-name,protected-access
from unittest.mock import patch

import pytest
from tests.smarttesting.staticmethod import other_module
from tests.smarttesting.staticmethod.client import Client


class Test17FraudVerifier:
    @pytest.mark.skip
    def test_should_mark_client_with_debt_as_fraud(self) -> None:
        """Test się wywala, gdyż wywołanie `is_fraud` wywoła połączenie do bazy danych.

        Nie wierzysz? Odkomentuj @pytest.mark.skip i sprawdź sam!
        """
        verifier = _18_FraudVerifier()

        result = verifier.is_fraud("Fraudowski")

        assert result is True

    def test_should_mark_client_with_debt_as_fraud_with_imported_from_other_module(
        self,
    ) -> None:
        """Test wykorzystujący czarną magię monkey-patchingu do poradzenia sobie z
        poleganiem na zmiennej importowanej z innego modułu przechowującej instancję.

        Swoisty najprostszy sposób na singleton w Pythonie.
        """
        verifier = _18_FraudVerifier()

        # Zastępujemy "singletona" naszą instancją
        new_obj = _21_FakeDatabaseAccessor()
        with patch.object(other_module, "database_accessor", new=new_obj):
            result = verifier.is_fraud("Fraudowski")

        assert result is True


class _18_FraudVerifier:
    """Przykład implementacji wołającej instancję zainicjalizowaną w innym module."""

    def is_fraud(self, name: str) -> bool:
        client = other_module.database_accessor.get_client_by_name(name)
        return client.has_debt


class _21_FakeDatabaseAccessor(other_module._19_DatabaseAccessor):
    def get_client_by_name(self, name: str) -> Client:
        return Client("Fraudowski", True)
