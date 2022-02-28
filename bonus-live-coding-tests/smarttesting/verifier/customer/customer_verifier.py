from dataclasses import dataclass
from typing import Set, Union

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.verification import Verification


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

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        """
        Główna metoda biznesowa. Weryfikuje czy dana osoba jest oszustem.
        """
        verifications_passed = all(
            verification.passes(customer.person) for verification in self._verifications
        )

        if verifications_passed:
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)
