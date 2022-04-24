# pylint: disable=invalid-name,unused-argument
import abc
from dataclasses import dataclass
from typing import Optional
from unittest.mock import Mock

import pytest


class Test02FraudVerifier:
    @pytest.mark.skip
    def test_marks_client_with_debt_as_fraud(self) -> None:
        """Próba napisania testu do istniejącej klasy łączącej się z bazą danych."""
        accessor = _03_DatabaseAccessorImpl()
        verifier = FraudVerifier(accessor)

        assert verifier.is_fraud("Fraudowski") is True

    def test_marks_client_with_debt_as_fraud_with_seam(self) -> None:
        """Przykład testu z wykorzystaniem szwa (seam)."""
        accessor = _04_FakeDatabaseAccessor()
        verifier = FraudVerifier(accessor)

        assert verifier.is_fraud("Fraudowski") is True

    @pytest.mark.skip
    def test_marks_client_with_debt_as_fraud_with_seam_logic_in_constructor(
        self,
    ) -> None:
        verifier = _09_FraudVerifierLogicInConstructor()

        assert verifier.is_fraud("Fraudowski") is True

    @pytest.mark.skip
    def test_creates_an_instance_of_fraud_verifier(self) -> None:
        _09_FraudVerifierLogicInConstructor()

    def test_marks_client_with_debt_as_fraud_with_a_mock(self) -> None:
        accessor = Mock(spec_set=_10_DatabaseAccessorImplWithLogicInTheConstructor)
        client = Client(name="Fraudowski", has_debt=True)
        accessor.get_client_by_name = Mock(return_value=client)
        verifier = _11_FraudVerifierLogicInConstructorExtractLogic(accessor)

        assert verifier.is_fraud("Fraudowski") is True

    def test_marks_client_with_debt_as_fraud_with_an_extracted_interface(self) -> None:
        accessor = _14_FakeDatabaseAccessorWithInterface()
        verifier = _13_FraudVerifierWithInterface(accessor)

        assert verifier.is_fraud("Fraudowski") is True

    def test_marks_client_with_debt_as_fraud_with_seam_interface(self) -> None:
        accessor = _14_FakeDatabaseAccessorWithInterface()
        verifier = _13_FraudVerifierWithInterface(accessor)

        assert verifier.is_fraud("Fraudowski") is True


@dataclass(frozen=True)
class Client:
    name: str
    has_debt: bool


class _03_DatabaseAccessorImpl:
    def get_client_by_name(self, name: str) -> Client:
        client = self._perform_Long_running_task(name)
        print(client.name)
        self._do_some_additional_work(client)
        return client

    def _perform_Long_running_task(self, name: str) -> Client:
        raise IOError("Can't connect to the database!")

    def _do_some_additional_work(self, client: Client) -> None:
        print("Additional work done")


class _04_FakeDatabaseAccessor(_03_DatabaseAccessorImpl):
    """Nasz szew (seam)!

    Nadpisujemy problematyczną metodę bez zmiany kodu produkcyjnego.
    """

    def get_client_by_name(self, name: str) -> Client:
        return Client(name="Fraudowski", has_debt=True)


class _12_DatabaseAccessor(abc.ABC):
    @abc.abstractmethod
    def get_client_by_name(self, name: str) -> Client:
        pass


class _14_FakeDatabaseAccessorWithInterface(_12_DatabaseAccessor):
    def get_client_by_name(self, name: str) -> Client:
        return Client(name="Fraudowski", has_debt=True)


class DatabaseAccessorImplWithInterface(_12_DatabaseAccessor):
    def __init__(self) -> None:
        self._connect_to_db()

    def _connect_to_db(self) -> None:
        raise IOError("Can't connect to the database!")

    def get_client_by_name(self, name: str) -> Client:
        client = self._perform_Long_running_task(name)
        print(client.name)
        self._do_some_additional_work(client)
        return client

    def _perform_Long_running_task(self, name: str) -> Client:
        raise IOError("Can't connect to the database!")

    def _do_some_additional_work(self, client: Client) -> None:
        print("Additional work done")


@dataclass
class _13_FraudVerifierWithInterface:
    _accessor: _12_DatabaseAccessor

    def is_fraud(self, name: str) -> bool:
        client = self._accessor.get_client_by_name(name)
        return client.has_debt


@dataclass
class FraudVerifier:
    _accessor: _03_DatabaseAccessorImpl

    def is_fraud(self, name: str) -> bool:
        client = self._accessor.get_client_by_name(name)
        return client.has_debt


class _10_DatabaseAccessorImplWithLogicInTheConstructor:
    def __init__(self) -> None:
        self._connect_to_db()

    def _connect_to_db(self) -> None:
        raise IOError("Can't connect to the database!")

    def get_client_by_name(self, name: str) -> Client:
        client = self._perform_Long_running_task(name)
        print(client.name)
        self._do_some_additional_work(client)
        return client

    def _perform_Long_running_task(self, name: str) -> Client:
        raise IOError("Can't connect to the database!")

    def _do_some_additional_work(self, client: Client) -> None:
        print("Additional work done")


class _09_FraudVerifierLogicInConstructor:
    def __init__(self) -> None:
        self._accessor = _10_DatabaseAccessorImplWithLogicInTheConstructor()

    def is_fraud(self, name: str) -> bool:
        client = self._accessor.get_client_by_name(name)
        return client.has_debt


class _11_FraudVerifierLogicInConstructorExtractLogic:
    def __init__(
        self,
        accessor: Optional[_10_DatabaseAccessorImplWithLogicInTheConstructor] = None,
    ) -> None:
        if accessor is None:  # domyślne zachowanie
            self._accessor = _10_DatabaseAccessorImplWithLogicInTheConstructor()
        else:
            self._accessor = accessor

    def is_fraud(self, name: str) -> bool:
        client = self._accessor.get_client_by_name(name)
        return client.has_debt
