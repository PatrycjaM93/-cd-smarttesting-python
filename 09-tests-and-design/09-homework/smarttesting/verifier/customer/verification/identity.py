from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


class IdentityVerification(Verification):
    """Weryfikacja po PESELu.

    TODO: Do zaimplementowania w najbliższym sprincie.
    """

    def passes(self, person: Person) -> bool:
        return False
