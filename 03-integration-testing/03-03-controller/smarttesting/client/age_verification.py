from smarttesting.client.person import Person
from smarttesting.client.verification import Verification


class AgeVerification(Verification):
    """Weryfikacja wieku osoby wnioskującej o udzielenie pożyczki."""

    def passes(self, person: Person) -> bool:
        if person.age < 0:
            raise ValueError("Age cannot be negative!")
        return 18 <= person.age <= 99
