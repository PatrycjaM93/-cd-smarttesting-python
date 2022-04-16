import time

import polling
import pytest
from smarttesting.customer.customer import Customer
from smarttesting.verifier.customer._01_customer_verifier import CustomerVerifier
from smarttesting.verifier.customer._03_verification_listener import (
    VerificationListener,
)


class Test02CustomerVerifier:
    """Klasa testowa procesowania weryfikacji na wielu wątkach."""

    @pytest.mark.skip
    @pytest.mark.flaky(reruns=5)
    def test_should_return_results_in_order_of_execution(
        self, verifier: CustomerVerifier, stefan: Customer
    ) -> None:
        """Test uruchamia procesowanie klienta Stefan.

        Procesowanie zostanie ukończone w losowej kolejności, natomiast w naszym teście
        oczekujemy, że dostaniemy odpowiedź w kolejności weryfikacji age, id i na końcu
        name.

        Na wszelki wypadek uruchamiamy test 5 razy, żeby upewnić się, że za każdym
        razem przejdzie.

        Odkomentuj dekorator `@pytest.mark.skip`, żeby przekonać się, że test może nie
        przejść!
        """
        results = verifier.verify(stefan)

        verification_results_names = [result.verification_name for result in results]
        assert verification_results_names == ["age", "id", "name"]

    def test_should_work_in_parallel_with_less_constraint(
        self, verifier: CustomerVerifier, stefan: Customer
    ) -> None:
        """Test uruchamia procesowanie klienta Stefan.

        Procesowanie zostanie ukończone w losowej kolejności. W naszym teście
        oczekujemy, że dostaniemy odpowiedź zawierającą wszystkie 3 weryfikacje w
        losowej kolejności.
        """
        results = verifier.verify(stefan)

        verification_results_names = [result.verification_name for result in results]
        assert set(verification_results_names) == {"age", "id", "name"}

    @pytest.mark.skip
    def test_should_work_in_parallel_without_a_sleep(
        self,
        verifier: CustomerVerifier,
        stefan: Customer,
        verifications_listener: VerificationListener,
    ) -> None:
        """Testujemy asynchroniczne procesowanie zdarzeń.

        Po każdej weryfikacji zostaje wysłane zdarzenie, które komponent
        `_03_verification_listener.VerificationListener` trzyma w kolejce.

        Procesowanie jest asynchroniczne, a test na to nie reaguje. Po zakolejkowaniu
        wywołań asynchronicznych od razu przechodzi do asercji zapisanych zdarzeń w
        kolejce. Problem w tym, że procesowanie jeszcze trwa! Innymi słowy test jest
        szybszy niż kod, który testuje.

        Odkomentuj dekorator `@pytest.mark.skip`, żeby przekonać się, że test może nie
        przejść!
        """
        verifier.verify_async(stefan)

        events = verifications_listener.received_events
        source_descriptions = [event.source_description for event in events]
        assert set(source_descriptions) == {"age", "id", "name"}

    def test_should_work_in_parallel_with_a_sleep(
        self,
        verifier: CustomerVerifier,
        stefan: Customer,
        verifications_listener: VerificationListener,
    ) -> None:
        """Próba naprawy sytuacji z testu powyżej.

        Zakładamy, że w ciągu 4 sekund zadania powinny się ukończyć, a zdarzenia
        powinny zostać wysłane.

        Rozwiązanie to w żaden sposób się nie skaluje i jest marnotrawstwem czasu.
        W momencie, w którym procesowanie ukończy się po np. 100 ms, zmarnujemy
        3.9 sekundy by dokonać asercji.
        """
        verifier.verify_async(stefan)

        time.sleep(4)

        events = verifications_listener.received_events
        source_descriptions = [event.source_description for event in events]
        assert set(source_descriptions) == {"age", "id", "name"}

    def test_should_work_in_parallel_with_polling(
        self,
        verifier: CustomerVerifier,
        stefan: Customer,
        verifications_listener: VerificationListener,
    ) -> None:
        """Najlepsze rozwiązanie problemu.

        Wykorzystujemy bibliotekę polling która wykorzystuje okresowe sprawdzenia
        z maksymalnym timeout'em - czyli tak zwany polling :) Wykorzystamy ją,
        dokonując sprawdzenia co 100ms, czekając maksymalnie 5s. W ten sposób nasz
        test w pesymistycznym przypadku zmarnuje tylko 100ms.
        """
        verifier.verify_async(stefan)

        polling.poll(
            # czekamy, aż wszystkie zdarzenia zostaną odebrane
            # moglibyśmy też umieścić tu warunek z asercji z końca testu
            lambda: len(verifications_listener.received_events) == 3,
            step=0.1,
            timeout=5,
        )
        events = verifications_listener.received_events
        source_descriptions = [event.source_description for event in events]
        assert set(source_descriptions) == {"age", "id", "name"}
