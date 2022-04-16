from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification


class NameVerification(Verification):
    """Weryfikacja po imieniu."""

    def passes(self, person: Person) -> VerificationResult:
        result = person.name is not None and person.name != ""
        return VerificationResult(self.name, result)

    @property
    def name(self) -> str:
        return "name"
