from datetime import date

import injector
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from smarttesting.client.app import create_app
from smarttesting.client.customer_verification_result import CustomerVerificationResult
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.person import Person


class Test04TestClient:
    """
    Klasa testowa do slajdu z testowaniem kontrolera z zamockowaną warstwą HTTP.

    Wykorzystując TestClienta z FastAPI (a właściwie ze Starlette, na którym jest
    zbudowane FastAPI) nie będziemy wykonywać prawdziwych requestów, jednak przejdziemy
    przez wszystkie warstwy frameworka.

    W tym teście nie traktujemy widoku jako funkcji. Wyślemy zamockowane żądanie HTTP
    i zweryfikujemy czy otrzymujemy rezultat, który nas interesuje.

    Rejestrujemy nadpisana wersję serwisu aplikacyjnego, która zwraca wartości
    "na sztywno". Gdybyśmy w którymś z innych komponentów mieli połączenie z bazą
    danych, NIE zostałoby ono nawiązane.
    """

    @pytest.fixture()
    def app(self) -> FastAPI:
        return create_app([MockCustomerVerifierModule()])

    @pytest.fixture()
    def test_client(self, app: FastAPI) -> TestClient:
        return TestClient(app)

    def test_rejects_loan_application_when_person_too_young(
        self, test_client: TestClient
    ) -> None:
        response = test_client.post("/fraudCheck", json=self._too_young_zbigniew())

        assert response.status_code == 401

    def _too_young_zbigniew(self) -> dict:
        return {
            "uuid": "7b3e02b3-6b1a-4e75-bdad-cef5b279b074",
            "name": "Zbigniew",
            "surname": "Zamłodowski",
            "date_of_birth": date.today().strftime("%Y-%m-%d"),
            "gender": "MALE",
            "national_id_number": "18210116954",
        }


class MockCustomerVerifierModule(injector.Module):
    """Klasa konfiguracyjna ustawiająca prosty przypadek biznesowy.

    W naszej kwestii pozostaje takie napisanie funkcji `create_app` żeby stawiając
    tylko częściowy kontekst aplikacji nie robić za dużo niepożądanych rzeczy.
    """

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
