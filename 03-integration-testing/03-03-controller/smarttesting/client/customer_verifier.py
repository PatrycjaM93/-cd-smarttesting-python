from dataclasses import dataclass
from typing import Set, Union

from smarttesting.client.customer_verification_result import CustomerVerificationResult
from smarttesting.client.person import Person
from smarttesting.client.verification import Verification


@dataclass(init=False)
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i zwraca zagregowany wynik.
    """

    _verifications: Set[Verification]

    def __init__(self, *args: Union[Verification, Set[Verification]]):
        """
        Initializer wspierający dwie metody tworzenia obiektu.
        """
        self._verifications = set()
        for arg in args:
            if isinstance(arg, set):
                self._verifications.update(arg)
            else:
                self._verifications.add(arg)

    def verify(self, person: Person) -> CustomerVerificationResult:
        """
        Główna metoda biznesowa. Weryfikuje czy dana osoba jest oszustem.
        """
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )

        if verifications_passed:
            return CustomerVerificationResult.create_passed(person.uuid)
        else:
            return CustomerVerificationResult.create_failed(person.uuid)
