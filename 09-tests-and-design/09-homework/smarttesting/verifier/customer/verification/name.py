from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification import Verification
from smarttesting.verifier.verification_event import VerificationEvent


@dataclass(unsafe_hash=True)
class NameVerification(Verification):
    """Weryfikacja po imieniu."""

    _event_emitter: EventEmitter

    def passes(self, person: Person) -> bool:
        result = self._verify(person.name)
        self._event_emitter.emit(VerificationEvent(result))
        return result

    def _verify(self, name: str) -> bool:
        return name.isalpha()
