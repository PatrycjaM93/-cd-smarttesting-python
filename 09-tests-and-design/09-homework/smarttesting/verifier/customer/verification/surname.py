from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification.surname_checker import SurnameChecker
from smarttesting.verifier.verification import Verification


@dataclass(unsafe_hash=True)
class SurnameVerification(Verification):
    """Weryfikacja wieku osoby wnioskującej o udzielenie pożyczki."""

    _surname_checker: SurnameChecker

    def passes(self, person: Person) -> bool:
        return self._surname_checker.check_surname(person)
