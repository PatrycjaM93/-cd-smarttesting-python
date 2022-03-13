import uuid
from datetime import date

import injector
from smarttesting.client.customer_verification_result import Status
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.person import Gender, Person
from tests.client._02_config import _02_Module


class Test03InjectorIoc:
    def test_injector_usage(self) -> None:
        """Kod przedstawiony na slajdzie po zdefiniowaniu klasy konfiguracyjnej.

        Ten test buduje IoC Injectora na podstawie modułu. Oddzielamy w ten sposób
        konstrukcję

        ```
        container = injector.Injector([_02_Module()])
        customer_verifier = container.get(CustomerVerifier)
        ```

        od użycia

        ```
        result = customer_verifier.verify(self._stefan())
        ```
        """
        # Zbudowanie kontenera na podstawie listy modułów
        container = injector.Injector([_02_Module()])

        # Wyciągnięcie obiektu z kontenera
        customer_verifier = container.get(CustomerVerifier)

        # Wywołanie logiki biznesowej
        result = customer_verifier.verify(self._stefan())

        # Asercja
        assert result.status == Status.VERIFICATION_FAILED

    def _stefan(self) -> Person:
        return Person(uuid.uuid4(), "", "", date.today(), Gender.MALE, "")

    def test_pytest_fixtures_as_ioc(self, customer_verifier: CustomerVerifier) -> None:
        """Mechanizm fikstur pytesta już działa jak IoC.

        Często praktyczniej będzie użyć właśnie jego (szczególnie jeśli nie używamy
        injectora/innego IoC w kodzie poza testami) lub kombinacji dwóch.

        Ten test wykorzystuje fiksturę customer_verifier zdefiniowaną w pliku
        conftest.py. W przeciwieństwie do injectora, tutaj liczą się nazwy argumentów,
        a nie typ w adnotacji. To znaczy, że nawet jeśli opuścimy adnotacje

        ```
        def test_pytest_fixtures(self, customer_verifier):
            ...
        ```
        test nadal będzie działać pod warunkiem, że istnieje fikstura
        `customer_verifier`.
        """
        # Wywołanie logiki biznesowej
        result = customer_verifier.verify(self._stefan())

        # Asercja
        assert result.status == Status.VERIFICATION_FAILED
