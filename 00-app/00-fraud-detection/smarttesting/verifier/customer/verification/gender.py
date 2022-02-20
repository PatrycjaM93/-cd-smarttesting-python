import logging

from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


logger = logging.getLogger(__name__)


class GenderVerification(Verification):
    """Weryfikacja po płci. Płeć musi być wybrana."""

    def passes(self, person: Person) -> bool:
        passed = person.gender is not None
        logger.info("Person %r passed the gender check %s", person, passed)
        return passed
