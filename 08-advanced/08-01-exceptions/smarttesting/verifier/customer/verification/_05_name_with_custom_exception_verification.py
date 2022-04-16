from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification._04_verification_exception import (
    VerificationException,
)
from smarttesting.verifier.verification import Verification


class NameWithCustomExceptionVerification(Verification):
    """Weryfikacja po nazwisku rzucająca wyjątek w przypadku błędu."""

    def passes(self, person: Person) -> bool:
        print(f"Person's gender is [{person.gender.name}]")
        if person.name is None:
            raise VerificationException("Name cannot be None.")

        return person.name != ""
