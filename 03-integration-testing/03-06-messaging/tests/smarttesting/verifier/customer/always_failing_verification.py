from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


class AlwaysFailingVerification(Verification):
    """Weryfikacja, która zawsze jest negatywna - klient chce nas oszukać."""

    def passes(self, person: Person) -> bool:
        return False
