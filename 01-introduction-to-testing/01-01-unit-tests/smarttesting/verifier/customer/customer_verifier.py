from dataclasses import dataclass
from typing import Set

from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer.bik_verification_service import (
    BIKVerificationService,
)
from smarttesting.verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)
from smarttesting.verifier.customer.very_bad_verification_service_wrapper import (
    VeryBadVerificationServiceWrapper,
)
from smarttesting.verifier.verification import Verification


@dataclass
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i zwraca zagregowany wynik.
    Klasa używa obiektu-wrappera otaczającego metodę statyczną realizującą operacje
    bazodanowe. Nie polecamy robienia czegoś takiego w metodzie statycznej, ale tu
    pokazujemy jak to obejść i przetestować jeżeli z jakiegoś powodu nie da się tego
    zmienić (np. metoda statyczna jest dostarczana przez kogoś innego).
    """

    _bik_verification_service: BIKVerificationService
    _verifications: Set[Verification]
    _service_wrapper: VeryBadVerificationServiceWrapper

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        external_result = self._bik_verification_service.verify(customer)

        person = customer.person
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )

        if (
            verifications_passed
            and external_result.passed
            and self._service_wrapper.verify()
        ):
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)
