import uuid
from datetime import date

import pytest
from injector import Injector
from smarttesting.client.customer_verification_result import Status
from smarttesting.client.customer_verifier import CustomerVerifier
from smarttesting.client.person import Gender, Person
from tests.client._02_config import _02_Module


class Test05CustomerVerificationTests:
    """Narzędzia do IoC / DI można czasem łatwo wykorzystać z narzędziami do testów.

    Tutaj widzimy wykorzystanie razem Injectora i pytesta, oba działające jak IoC.
    Mamy fiksturę pytesta która zapewnia nam kontener Injectora który wykorzystujemy
    w innych fiksturach do tworzenia obiektów."""

    @pytest.fixture(scope="session")
    def container(self) -> Injector:
        """Fikstura z kontenerem Injectora.

        Prawdopodobnie wystarczy umieścić ją raz, w `conftest` najwyższego poziomu
        ze scope "session" by była wyliczona raz i dostępna dla wszystkich testów.
        """
        return Injector([_02_Module()])

    @pytest.fixture()
    def customer_verifier(self, container: Injector) -> CustomerVerifier:
        """Fikstura używa kontenera do zbudowania/wyciągnięcia obiektu."""
        return container.get(CustomerVerifier)

    def test_passes_verification_when_non_fraud_gets_verified(
        self, customer_verifier: CustomerVerifier
    ) -> None:
        """
        Pytest wstrzykuje fiksturę `customer_verifier`.
        """
        # Wywołanie logiki biznesowej
        result = customer_verifier.verify(self._too_young_stefan())

        assert result.status == Status.VERIFICATION_FAILED

    def _too_young_stefan(self) -> Person:
        return Person(uuid.uuid4(), "", "", date.today(), Gender.MALE, "")
