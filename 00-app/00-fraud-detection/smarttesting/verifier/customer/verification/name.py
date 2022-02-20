import logging
from dataclasses import dataclass

from smarttesting.customer.person import Person, Gender
from smarttesting.verifier.verification import Verification


logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class NameVerification(Verification):
    """Weryfikacja po imieniu. Dla kobiety imię musi się kończyc na "a"."""

    def passes(self, person: Person) -> bool:
        result = True
        if person.gender == Gender.FEMALE:
            result = person.name.endswith("a")
        logger.info("Person %r passed the name check %s", person, result)
        return result
