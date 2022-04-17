import logging
import random
import time
from dataclasses import dataclass

from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.application.event_bus import EventBus
from smarttesting.verifier.application.verification_event import VerificationEvent
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification

logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class IdentificationNumberVerification(Verification):
    """Weryfikacja poprawności numeru PESEL.

    Po zakończonym procesowaniu weryfikacji wysyła zdarzenie z rezultatem weryfikacji.
    """

    _publisher: EventBus

    def passes(self, person: Person) -> VerificationResult:
        logger.info("Running age verification")
        # Symuluje procesowanie w czasie losowym do 2 sekund
        time.sleep(random.randint(0, 2000) / 1000)
        logger.info("Id verification done")

        result = (
            self._gender_matches_id_number(person)
            and self._starts_with_date_of_birth(person)
            and self._weight_is_correct(person)
        )
        self._publisher.publish(VerificationEvent(self, self.name, result))
        return VerificationResult(self.name, result)

    @property
    def name(self) -> str:
        return "id"

    def _gender_matches_id_number(self, person: Person) -> bool:
        tenth_character = person.national_id_number[9:10]
        if int(tenth_character) % 2 == 0:
            return person.gender == Gender.FEMALE
        else:
            return person.gender == Gender.MALE

    def _starts_with_date_of_birth(self, person: Person) -> bool:
        dob_formatted = person.date_of_birth.strftime("%y%m%d")
        if dob_formatted[0] == "0":
            month = person.date_of_birth.month + 20
            dob_formatted = dob_formatted[:2] + str(month) + dob_formatted[4:]

        return dob_formatted == person.national_id_number[:6]

    def _weight_is_correct(self, person: Person) -> bool:
        if len(person.national_id_number) != 11:
            return False

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        weight_sum = sum(
            int(person.national_id_number[index]) * weights[index]
            for index in range(10)
        )
        actual_sum = (10 - weight_sum % 10) % 10

        check_sum = int(person.national_id_number[10])
        return actual_sum == check_sum
