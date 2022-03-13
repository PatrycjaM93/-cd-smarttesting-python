from dataclasses import dataclass
from typing import Set, Union

from smarttesting.client.customer_verification_result import CustomerVerificationResult
from smarttesting.client.person import Person
from smarttesting.client.verification import Verification


@dataclass(init=False)
class CustomerVerifier:
    """Weryfikacja czy klient jest oszustem czy nie.

    Przechodzi po różnych implementacjach weryfikacji i zwraca zagregowany wynik.
    """

    _verifications: Set[Verification]

    def __init__(self, *args: Union[Verification, Set[Verification]]):
        """
        Initializer wspierający dwie metody tworzenia obiektu.
        """
        self._verifications = set()
        for arg in args:
            if isinstance(arg, set):
                self._verifications.update(arg)
            else:
                self._verifications.add(arg)

    def verify(self, person: Person) -> CustomerVerificationResult:
        """
        Główna metoda biznesowa. Weryfikuje czy dana osoba jest oszustem.
        """
        verifications_passed = all(
            verification.passes(person) for verification in self._verifications
        )

        if verifications_passed:
            return CustomerVerificationResult.create_passed(person.uuid)
        else:
            return CustomerVerificationResult.create_failed(person.uuid)


class HttpCallMaker:
    """Klasa udająca klasę łączącą się po HTTP."""


class Dao:
    """Klasa udająca klasę łączącą się po bazie danych.."""


class EventEmitter:
    """Klasa udająca klasę łączącą się po brokerze wiadomości."""


@dataclass(unsafe_hash=True)
class AgeVerification(Verification):
    """
    Weryfikacja po wieku.

    Na potrzeby scenariusza lekcji, brak prawdziwej implementacji.
    Klasa symuluje połączenie po HTTP i po bazie danych.
    """

    _http_call_maker: HttpCallMaker
    _dao: Dao


@dataclass(unsafe_hash=True)
class IdentificationNumberVerification(Verification):
    """
    Weryfikacja po numerze pesel.

    Na potrzeby scenariusza lekcji, brak prawdziwej implementacji.
    Klasa symuluje połączenie po bazie danych.
    """

    _dao: Dao


@dataclass(unsafe_hash=True)
class NameVerification(Verification):
    """
    Weryfikacja po nazwisku.

    Na potrzeby scenariusza lekcji, brak prawdziwej implementacji.
    Klasa symuluje połączenie po brokerze wiadomości.
    """

    _event_emitter: EventEmitter
