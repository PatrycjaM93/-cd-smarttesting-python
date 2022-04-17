from dataclasses import dataclass

from smarttesting.customer.person import Person
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)


@dataclass(frozen=True)
class CustomerVerification:
    """Klasa wiadomości, którą wysyłamy poprzez brokera.

    Reprezentuje osobę i rezultat weryfikacji.
    """

    person: Person
    result: CustomerVerificationResult
