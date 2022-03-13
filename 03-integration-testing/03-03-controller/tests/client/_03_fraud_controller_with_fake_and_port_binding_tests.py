from datetime import date

import injector
import pytest
import requests
from fastapi import status
from smarttesting.client.app import create_app
from smarttesting.client.customer_verification_result import CustomerVerificationResult
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.person import Person


class PortControllerWithFake(injector.Module):
    @injector.provider
    def customer_verifier(self) -> CustomerVerifier:
        """Serwis aplikacyjny, który nie przyjmuje żadnych produkcyjnych weryfikacji.

        Nadpisujemy jego logikę biznesową w taki sposób, żeby zwrócone zostały dane
        "na sztywno". Wartość 10 została wzięta w losowy sposób, dla testów.
        """

        class DummyVerifier(CustomerVerifier):
            def verify(self, person: Person) -> CustomerVerificationResult:
                if person.age < 10:
                    return CustomerVerificationResult.create_failed(person.uuid)
                else:
                    return CustomerVerificationResult.create_passed(person.uuid)

        return DummyVerifier()


# Z uwagi na specyfikę uruchamiania procesu w tle i uvicorna,
# najłatwiej pożenić je ze sobą poprzez zrobienie z `app` zmiennej lokalnej
app = create_app([PortControllerWithFake()])


@pytest.fixture(scope="module")
def app_path() -> str:
    """Nadpisujemy fiksturę w tym teście by uruchomić przekonfigurowaną aplikację."""
    return f"{__name__}:app"


@pytest.mark.usefixtures("running_server")
class Test03FraudControllerWithFakeAndPortBinding:
    """Klasa testowa do slajdu z testowaniem kontrolera po warstwie HTTP z alokacją
    portu z zamockowanym serwisem aplikacyjnym.

    Wykorzystując fabrykę `create_app` i `PortControllerWithFake` tworzymy specjalną
    wersję aplikacji która zostanie uruchomiona w tle. W tym teście nie traktujemy
    kontrolera jako funkcji. Wyślemy prawdziwe żądanie HTTP i zweryfikujemy czy
    otrzymujemy rezultat, który nas interesuje.

    Rejestrujemy tylko nadpisaną wersję `CustomerVerifier`, która
    zwraca wartości "na sztywno". Gdybyśmy w którymś z innych komponentów mieli
    połączenie z bazą danych, NIE zostałoby ono nawiązane.
    """

    def test_rejects_loan_application_when_person_too_young(
        self, root_address: str
    ) -> None:
        """
        Mając uruchomiony w tle serwer, wykorzystujemy bibliotekę `requests` do
        wysłania zwyczajne żądania HTTP na adres serwera.

        Wysyłamy żądanie ze zbyt młodym Zbigniewem i oczekujemy, że dostaniemy status
        401.
        """
        response = requests.post(
            root_address + "fraudCheck", json=self._too_young_zbigniew()
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def _too_young_zbigniew(self) -> dict:
        return {
            "uuid": "7b3e02b3-6b1a-4e75-bdad-cef5b279b074",
            "name": "Zbigniew",
            "surname": "Zamłodowski",
            "date_of_birth": date.today().strftime("%Y-%m-%d"),
            "gender": "MALE",
            "national_id_number": "18210116954",
        }
