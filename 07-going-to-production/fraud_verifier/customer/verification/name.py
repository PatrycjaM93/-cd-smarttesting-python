from fraud_verifier.customer.person import Person
from fraud_verifier.verification import Verification


class NameVerification(Verification):
    def passes(self, person: Person) -> bool:
        return person.name.isalpha()
