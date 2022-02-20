import logging
from dataclasses import dataclass
from typing import ClassVar

from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class SurnameVerification(Verification):
    """Weryfikacja po nazwisku. Nazwisko musi mieć przynajmniej jedną samogłoskę."""

    VOWELS: ClassVar[set[str]] = {"a", "i", "o", "u"}

    def passes(self, person: Person) -> bool:
        surname_letters = set(person.surname)
        result = len(surname_letters & self.VOWELS) > 0
        logger.info("Person %r passed the surname check %s", person, result)
        return result
