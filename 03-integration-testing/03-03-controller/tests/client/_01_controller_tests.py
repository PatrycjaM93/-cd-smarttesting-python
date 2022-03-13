import uuid
from datetime import date

import injector
import pytest
from fastapi import Response, status
from smarttesting.client import fraud_view
from smarttesting.client.age_verification import AgeVerification
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.person import Gender, Person


class Test01Controller:
    """Klasa testowa do slajdu z testowaniem kontrolera jako obiektu.

    W Pythonie nierzadką konwencją jest używanie funkcji jako widoków, jak w tym
    przykładzie. Jeśli wywołamy widok jako funkcję, przekazując zależności to z punktu
    widzenia widoku mamy nic innego jak test jednostkowy. W taki sposób testujemy
    bez warstwy HTTP czy WSGI/ASGI logikę naszych komponentów. Zakładając, że
    przetestowaliśmy jednostkowo `CustomerVerifier`, taki test nic nam nie daje.

    Zatem skoro naszym celem jest zweryfikowanie czy nasz kontroler komunikuje się
    po warstwie HTTP to kompletnie nam się to nie udało.

    Czy jest to zły test? Nie, ale trzeba włączyć w to testowanie warstwy HTTP.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Przygotowujemy kontener aby przygotować instancję CustomerVerifiera."""
        self.container = injector.Injector([TestModule()])

    @pytest.fixture()
    def customer_verifier(self) -> CustomerVerifier:
        return self.container.get(CustomerVerifier)

    def test_rejects_loan_application_when_person_too_young(
        self, customer_verifier: CustomerVerifier
    ):
        response = Response()
        fraud_view.fraud_check_view(
            self._too_young_zbigniew(), response, customer_verifier
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def _too_young_zbigniew(self) -> Person:
        return Person(
            uuid=uuid.uuid4(),
            name="",
            surname="",
            date_of_birth=date.today(),
            gender=Gender.MALE,
            national_id_number="",
        )


class TestModule(injector.Module):
    """Klasa konfiguracyjna ustawiająca prosty przypadek biznesowy.

    Wykorzystujemy jedną weryfikacją po wieku.
    """

    @injector.provider
    def age_verification(self) -> AgeVerification:
        return AgeVerification()

    @injector.provider
    def customer_verifier(self, age: AgeVerification) -> CustomerVerifier:
        return CustomerVerifier({age})
