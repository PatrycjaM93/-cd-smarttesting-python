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
    Klasa używa obiektu-wrappera otaczającego metodę statyczną realizującą operacje
    bazodanowe. Nie polecamy robienia czegoś takiego w metodzie statycznej, ale tu
    pokazujemy jak to obejść i przetestować jeżeli z jakiegoś powodu nie da się tego
    zmienić (np. metoda statyczna jest dostarczana przez kogoś innego).
    """

    _verifications: Set[Verification]

    def __init__(self, *args: Union[Verification, Set[Verification]]):
        """
        Initializer wspierający dwie metody tworzenia obiektu.

        Ponieważ w Pythonie brakuje przeciążania, zapewnienie takiej implementacji
        wiąże się z koniecznością sprawdzenia typu argumentu. Alternatywna
        implementacja bez instrukcji warunkowych to metody fabrykujące typu
        udekorowane @classmethod, na przykład:

            ```
            @classmethod
            def from_verifications_set(cls, verifications: Set[Verification]) -> None:
                return cls(verifications)

            @classmethod
            def from_verifications(*verifications: Verification) -> None:
                return cls(set(verifications))
            ```

        Inne rozwiązanie to użycie functools.singledispatch (o ile to możliwe).

        Mimo wszystko, w bibliotece standardowej Pythona i bibliotekach 3rd party
        występują funkcje przyjmujące różne typy argumentów wejściowych i sprawdzają
        typ w środku.
        """
        self._verifications = set()
        for arg in args:
            if isinstance(arg, set):
                self._verifications.update(arg)
            else:
                self._verifications.add(arg)

    def verify(self, customer: Customer) -> CustomerVerificationResult:
        person = customer.person
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )

        if verifications_passed:
            return CustomerVerificationResult.create_passed(customer.uuid)
        else:
            return CustomerVerificationResult.create_failed(customer.uuid)
