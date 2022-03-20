from typing import Set

import injector
from fraud_verifier.customer.customer_verifier import CustomerVerifier
from fraud_verifier.customer.verification.age import AgeVerification
from fraud_verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)
from fraud_verifier.customer.verification.name import NameVerification
from fraud_verifier.verification import Verification


class FraudVerifierModule(injector.Module):
    @injector.provider
    def verifications(self) -> Set[Verification]:
        age = AgeVerification()
        id_number = IdentificationNumberVerification()
        name = NameVerification()
        return {age, id_number, name}

    @injector.provider
    def verifier(self, verifications: Set[Verification]) -> CustomerVerifier:
        return CustomerVerifier(verifications)
