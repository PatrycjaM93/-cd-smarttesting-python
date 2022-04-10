from fraud_verifier.customer.person import Person
from fraud_verifier.verification import Verification


class NewTypeOfVerification(Verification):
    def passes(self, person: Person) -> bool:
        return False
