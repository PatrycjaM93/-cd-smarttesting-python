from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification import Verification
from smarttesting.verifier.verification_event import VerificationEvent


@dataclass(unsafe_hash=True)
class AgeVerification(Verification):
    """Weryfikacja wieku osoby wnioskującej o udzielenie pożyczki."""

    _event_emitter: EventEmitter

    def passes(self, person: Person) -> bool:
        if person.age < 0:
            raise ValueError("Age cannot be negative!")
        passes = 18 <= person.age <= 99
        self._event_emitter.emit(VerificationEvent(passes))
        return passes
