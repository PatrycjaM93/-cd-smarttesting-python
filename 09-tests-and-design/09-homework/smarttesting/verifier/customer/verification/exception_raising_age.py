from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


class ExceptionRaisingAgeVerification(Verification):
    """Weryfikacja po wieku - jeśli nie przechodzi to leci wyjątek."""

    def passes(self, person: Person) -> bool:
        result = person.age >= 18
        if not result:
            raise ValueError("You cannot be below 18 years old!")
        return result
