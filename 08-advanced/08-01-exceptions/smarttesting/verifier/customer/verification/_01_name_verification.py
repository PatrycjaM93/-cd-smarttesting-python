from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


class NameVerification(Verification):
    """Weryfikacja po imieniu."""

    def passes(self, person: Person) -> bool:
        print(f"Person's gender is [{person.gender.name}]")
        if person.name is None:
            raise AttributeError("Name cannot be None")

        return person.name != ""
