import abc
from dataclasses import dataclass
from unittest.mock import Mock


class Test02DoesUnittestMockWork:
    def test_returns_positive_fraud_verification_when_fraud(self) -> None:
        """W tym teście de facto weryfikujemy czy framework do mockowania działa."""
        service = Mock(spec_set=AnotherFraudService)
        service.is_fraud = Mock(return_value=True)
        fraud_service = FraudService(service)

        result = fraud_service.check_if_fraud(Person())

        assert result is True


class Person:
    pass


class AnotherFraudService(abc.ABC):
    @abc.abstractmethod
    def is_fraud(self, person: Person) -> bool:
        pass


@dataclass
class FraudService:
    _service: AnotherFraudService

    def check_if_fraud(self, person: Person) -> bool:
        return self._service.is_fraud(person)
