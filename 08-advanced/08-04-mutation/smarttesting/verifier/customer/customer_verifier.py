from dataclasses import dataclass
from typing import List, Set

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.verification_result import VerificationResult
from smarttesting.verifier.verification import Verification


@dataclass
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i jeśli, przy którejś okaże się,
    że użytkownik jest oszustem, wówczas odpowiedni rezultat zostanie zwrócony.
    """

    _verifications: Set[Verification]

    def verify(self, customer: Customer) -> List[VerificationResult]:
        return [
            verification.passes(customer.person) for verification in self._verifications
        ]
