from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification.verifier_manager import VerifierManager
from smarttesting.verifier.event_emitter import EventEmitter
from smarttesting.verifier.verification import Verification
from smarttesting.verifier.verification_event import VerificationEvent


@dataclass(unsafe_hash=True)
class BusinessRulesVerification(Verification):
    """Weryfikacja po warunkach biznesowych.

    Chyba ta klasa robi za dużo, no ale trudno...
    """

    _event_emitter: EventEmitter
    _verifier: VerifierManager

    def passes(self, person: Person) -> bool:
        result = all(
            [
                self._verifier.verify_name(person),
                self._verifier.verify_address(person),
                self._verifier.verify_phone(person),
                self._verifier.verify_surname(person),
                self._verifier.verify_tax_information(person),
            ]
        )
        self._event_emitter.emit(VerificationEvent(result))
        return result
