import abc

from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification_result import VerificationResult


class Verification(abc.ABC):
    @abc.abstractmethod
    def passes(self, person: Person) -> VerificationResult:
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass
