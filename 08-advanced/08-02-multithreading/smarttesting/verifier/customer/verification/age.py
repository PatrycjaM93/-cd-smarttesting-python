import logging
import random
import time
from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.application.event_bus import EventBus
from smarttesting.verifier.application.verification_event import VerificationEvent
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification

logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class AgeVerification(Verification):
    """Weryfikacja wieku osoby wnioskującej o udzielenie pożyczki.

    Po zakończonym procesowaniu weryfikacji wysyła zdarzenie z rezultatem weryfikacji.
    """

    _publisher: EventBus

    def passes(self, person: Person) -> VerificationResult:
        logger.info("Running age verification")
        # Symuluje procesowanie w czasie losowym do 2 sekund
        time.sleep(random.randint(0, 2000) / 1000)
        logger.info("Age verification done")

        if person.age < 0:
            raise ValueError("Age cannot be negative!")
        result = 18 <= person.age <= 99
        self._publisher.publish(VerificationEvent(self, self.name, result))
        return VerificationResult(self.name, result)

    @property
    def name(self) -> str:
        return "age"
