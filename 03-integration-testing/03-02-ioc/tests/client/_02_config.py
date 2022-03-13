from typing import Set

import injector
from smarttesting.client.customer_verifier import (
    AgeVerification,
    CustomerVerifier,
    Dao,
    EventEmitter,
    HttpCallMaker,
    IdentificationNumberVerification,
    NameVerification,
)
from smarttesting.client.verification import Verification


class _02_Module(injector.Module):  # pylint: disable=invalid-name
    """`Module` to w bibliotece injector część (lub całość) konfiguracji IoC.

    Z jednej lub kilku instancji klas pochodnych od `injector.Module` można
    zbudować kontener, instancję klasy Injector.

    Każda metoda udekorowana @injector.provider jest używana potem jako instrukcja
    do zbudowania obiektu zgodnie z adnotacją typu zwracanego.
    """

    @injector.provider
    def http_call_maker(self) -> HttpCallMaker:
        return HttpCallMaker()

    @injector.provider
    def dao(self) -> Dao:
        return Dao()

    @injector.provider
    def age_verification(
        self, http_call_maker: HttpCallMaker, dao: Dao
    ) -> AgeVerification:
        """Argumentami metody są zależności które chcemy by zostały wstrzyknięte.

        Nazwa argumentu nie ma znaczenie dla injectora. Liczy się typ w adnotacji.
        """
        return AgeVerification(http_call_maker, dao)

    @injector.provider
    def id_verification(self, dao: Dao) -> IdentificationNumberVerification:
        return IdentificationNumberVerification(dao)

    @injector.provider
    def event_emitter(self) -> EventEmitter:
        return EventEmitter()

    @injector.provider
    def name_verification(self, event_emitter: EventEmitter) -> NameVerification:
        return NameVerification(event_emitter)

    @injector.provider
    def verifications(
        self,
        age: AgeVerification,
        id_verification: IdentificationNumberVerification,
        name: NameVerification,
    ) -> Set[Verification]:
        """Injector w przeciwieństwie do springowego IoC nie będzie potrafił
        sam znaleźć wszystkich implementacji `Verification`, więc musimy mu pomóc.

        Alternatywnie można przerobić wszystkie providery na multiprovidery:
        ```
        @injector.multiprovider
        def id_verification(self, ...) -> List[Verification]:
            return [IdentificationNumberVerification(dao)]

        @injector.multiprovider
        def name_verification(self, ...) -> List[Verification]:
            return [NameVerification(event_emitter)]
        ```
        Następnie do `customer_verifier` wstrzykniemy List[Verification] i przerobimy
        na zbiór, np. `set(verifications)`.
        """
        return {age, id_verification, name}

    @injector.provider
    def customer_verifier(self, verifications: Set[Verification]) -> CustomerVerifier:
        return CustomerVerifier(verifications)
