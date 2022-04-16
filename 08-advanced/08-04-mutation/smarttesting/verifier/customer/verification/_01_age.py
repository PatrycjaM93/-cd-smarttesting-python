import logging

from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification

logger = logging.getLogger(__name__)


class AgeVerification(Verification):
    """Weryfikacja wieku osoby wnioskującej o udzielenie pożyczki."""

    def passes(self, person: Person) -> VerificationResult:
        age = person.age
        if age < 0:
            logger.warning("Age is negative")
            raise ValueError("Age cannot be negative!")
        logger.info("Person has age %s", age)
        result = 18 <= age <= 99
        return VerificationResult(self.name, result)

    @property
    def name(self) -> str:
        return "age"
