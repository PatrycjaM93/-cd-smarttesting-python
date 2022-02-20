from typing import Set

import injector

from smarttesting.verifier.customer.verification.age import AgeVerification
from smarttesting.verifier.customer.verification.gender import GenderVerification
from smarttesting.verifier.customer.verification.identification_number import (
    IdentificationNumberVerification,
)
from smarttesting.verifier.customer.verification.name import NameVerification
from smarttesting.verifier.customer.verification.surname import SurnameVerification
from smarttesting.verifier.verification import Verification


class VerificationModule(injector.Module):
    @injector.provider
    def age(self) -> AgeVerification:
        return AgeVerification()

    @injector.provider
    def id_number(self) -> IdentificationNumberVerification:
        return IdentificationNumberVerification()

    @injector.provider
    def verifications(
        self, age: AgeVerification, id_number: IdentificationNumberVerification
    ) -> Set[Verification]:
        return {age, id_number}

    @injector.provider
    def name(self) -> NameVerification:
        return NameVerification()

    @injector.provider
    def surname(self) -> SurnameVerification:
        return SurnameVerification()

    @injector.provider
    def gender(self) -> GenderVerification:
        return GenderVerification()
