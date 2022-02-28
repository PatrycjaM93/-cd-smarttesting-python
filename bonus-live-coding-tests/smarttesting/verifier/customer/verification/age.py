import logging
from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification import Verification
from smarttesting.verifier.verification_event import VerificationEvent

logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class AgeVerification(Verification):
    """Weryfikacja wieku osoby wnioskującej o udzielenie pożyczki."""

    _event_emitter: EventEmitter

    def passes(self, person: Person) -> bool:
        age = person.age
        if age < 0:
            logger.warning("Age is negative")
            self._event_emitter.emit(VerificationEvent(False))
            raise ValueError("Age cannot be negative!")
        logger.info("Person has age %s", age)
        result = 18 <= age <= 99
        self._event_emitter.emit(VerificationEvent(result))
        return result
