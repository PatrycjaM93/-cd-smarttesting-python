# pylint: disable=invalid-name,unused-argument
from dataclasses import dataclass


@dataclass
class Client:
    has_debt: bool = False


class DaoImpl:
    def get_client_by_name(self, name: str) -> Client:
        return Client()


@dataclass
class _01_FraudVerifier:
    _dao_impl: DaoImpl

    def is_fraud(self, name: str) -> bool:
        client = self._dao_impl.get_client_by_name(name)
        return client.has_debt
