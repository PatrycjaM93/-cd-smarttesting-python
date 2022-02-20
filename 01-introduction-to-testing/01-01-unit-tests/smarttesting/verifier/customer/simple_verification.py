from smarttesting.customer.person import Person
from smarttesting.verifier.verification import Verification


class SimpleVerification(Verification):
    def __init__(self) -> None:
        self._verification_passed = True

    def passes(self, person: Person) -> bool:
        """Metoda z niezaimplementowaną logiką, dla której przechodzą testy."""
        # TODO: use _some_logic_resolving_to_bool(person);
        return False

    def _some_logic_resolving_to_bool(self, person: Person) -> bool:
        # TODO: calculate based on verificationPassed value
        raise NotImplementedError

    @property
    def verification_passed(self) -> bool:
        return self._verification_passed
