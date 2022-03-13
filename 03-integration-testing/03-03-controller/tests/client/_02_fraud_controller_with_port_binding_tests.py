"""Potencjalne zastosowanie tej techniki w Pythonie jest dość ograniczone.

Wiele dojrzałych frameworków ma własne narzędzia ułatwiające testowanie, także FastAPI.
Jeden przypadek, w którym stawianie prawdziwego serwera jest przydatne to uruchamianie
testów Selenium na aplikacji webowej która nie jest typowym API, ale generuje widoki.
Kolejnym przypadkiem użycia będzie testowanie API zewnętrznym narzędziem, jak tavern
prezentowany w jednym z kolejnych przykładów.

Uogólniając, korzystanie z narzędzi które wymagają postawionej aplikacji.

Należy też zwrócić uwagę czy nasz framework nie posiada takiej funkcjonalności,
tak jak ma to miejsce w przypadku Django:
https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.LiveServerTestCase
"""
from datetime import date

import pytest
import requests
from fastapi import status


@pytest.mark.usefixtures("running_server")
class Test02FraudControllerWithPortBinding:
    """Klasa testowa do slajdu z testowaniem po warstwie HTTP z alokacją portu.

    Wykorzystując klasę `Process` uruchamiamy cały serwer w tle na losowym porcie.

    W tym teście nie traktujemy widoku jak funkcji. Wyślemy prawdziwe żądanie HTTP
    i zweryfikujemy czy otrzymamy rezultat, który nas interesuje.

    Uruchamiamy WSZYSTKIE warstwy naszej aplikacji. Gdybyśmy w którymś miejscu mieli
    połączenie z bazą danych, zostałoby ono nawiązane.
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
