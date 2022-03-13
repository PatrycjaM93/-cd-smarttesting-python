import uuid
from datetime import date

from smarttesting.client.customer_verification_result import Status
from smarttesting.client.customer_verifier import (
    AgeVerification,
    CustomerVerifier,
    Dao,
    EventEmitter,
    HttpCallMaker,
    IdentificationNumberVerification,
    NameVerification,
)
from smarttesting.client.person import Gender, Person


class Test01IoC:
    def test_manual_object_creation(self) -> None:
        """
        Kod przedstawiony na slajdzie [W jaki sposób tworzysz obiekty?].

        Przedstawiamy tu ręczne utworzenie drzewa zależności obiektów.
        Trzeba pamiętać o odpowiedniej kolejności utworzenia obiektów oraz
        w jednym miejscu mieszamy tworzenie i realizacje akcji biznesowej
        wywołanie:

        CustomerVerifiery(...).verify()

        Problem zachowania kolejności argumentów nie występuje w Pythonie
        jeżeli użyjemy keyword arguments:

        age_verification = AgeVerification(_dao=dao, _http_call_maker=http_call_maker)

        """
        # Tworzenie `AgeVerification`
        http_call_maker = HttpCallMaker()
        dao = Dao()
        age_verification = AgeVerification(http_call_maker, dao)

        # Tworzenie `IdentificationNumberVerification`
        id_verification = IdentificationNumberVerification(dao)

        # Tworzenie `NameVerification`
        event_emitter = EventEmitter()
        name_verification = NameVerification(event_emitter)

        # Wywołanie logiki biznesowej
        result = CustomerVerifier(
            age_verification, id_verification, name_verification
        ).verify(self._stefan())

        # Asercja
        assert result.status == Status.VERIFICATION_FAILED

    def _stefan(self) -> Person:
        return Person(uuid.uuid4(), "", "", date.today(), Gender.MALE, "")
