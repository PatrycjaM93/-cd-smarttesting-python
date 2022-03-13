import uuid
from datetime import date

import injector
from smarttesting.client.customer_verification_result import Status
from smarttesting.client.customer_verifier import (
    CustomerVerifier,
    IdentificationNumberVerification,
)
from smarttesting.client.person import Gender, Person
from tests.client._02_config import _02_Module
from tests.client.in_memory_dao import InMemoryDao


class Test04ManualInjectorIoC:
    def test_manual_config(self) -> None:
        # Utworzenie obiektu dla testowej konfiguracji
        customer_verifier = injector.Injector([TestModule()]).get(CustomerVerifier)

        # Wywołanie logiki biznesowej
        result = customer_verifier.verify(self._too_young_stefan())

        assert result.status == Status.VERIFICATION_FAILED

    def _too_young_stefan(self) -> Person:
        return Person(uuid.uuid4(), "", "", date.today(), Gender.MALE, "")


class TestModule(_02_Module):
    """Konfiguracja testowa rozszerzająca schemat produkcyjny.

    Chcemy osiągnąć sytuację, w której możemy wołać produkcyjne metody schematu,
    by utworzyć interesujący nas obiekt na potrzeby testów, bez potrzeby
    inicjalizowania całego kontenera.
    """

    def build_test_id_verification(self) -> IdentificationNumberVerification:
        """Na potrzeby testów.

        Brak dekoratora @injector.provider = brak obiektu w kontenerze.
        """
        return self.id_verification(InMemoryDao())

    def build_test_customer_verifier(self) -> CustomerVerifier:
        """
        Na potrzeby testów. Produkcyjna metoda konfiguracyjna z kolekcją weryfikacji.

        Wykorzystujemy produkcyjną metodę, do której przekazujemy kolekcję z
        pojedynczym elementem weryfikacji, który został przez nas przygotowany dla
        potrzeb testów.
        """
        return self.customer_verifier({self.build_test_id_verification()})
