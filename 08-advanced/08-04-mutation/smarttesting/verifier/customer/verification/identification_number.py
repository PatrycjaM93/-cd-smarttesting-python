import logging

from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification

logger = logging.getLogger(__name__)


class IdentificationNumberVerification(Verification):
    """Weryfikacja poprawności numeru PESEL."""

    def passes(self, person: Person) -> VerificationResult:
        result = self._gender_matches_id_number(person)
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
