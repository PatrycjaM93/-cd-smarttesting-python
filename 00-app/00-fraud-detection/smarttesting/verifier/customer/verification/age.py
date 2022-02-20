import logging

from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


logger = logging.getLogger(__name__)


class AgeVerification(Verification):
    """Weryfikacja po wieku.

    Osoba w wieku powyżej 18 lat zostanie zweryfikowana pozytywnie.
    """

    def passes(self, person: Person) -> bool:
        if person.age < 0:
            raise ValueError("Age cannot be negative!")
        passed = 16 <= person.age <= 99
        logger.info("Person %r passed the age check %s", person, passed)
        return passed
