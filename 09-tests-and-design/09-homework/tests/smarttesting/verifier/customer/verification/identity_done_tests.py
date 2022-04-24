from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.customer.verification.identity import IdentityVerification


class TestIdentifyVerificationDone:
    """Pierwotny test testuje tylko negatywny przypadek.

    Kod produkcyjny zawiera automatycznie generowany kod przez IDE.
    Czasami zdarza się, że test przechodzi, a nie powinien tylko dlatego, że użyte
    zostały wartości domyślne takie jak None, 0, False.

    W Pythonie na przykład można wpaść w pułapkę funkcji bez `return`, gdyż wtedy
    wynikiem działania jest `None`. Jeżeli mamy tylko jeden test, który sprawdza czy
    wynikiem jest właśnie `None` to przecież możemy dostać fałszywie przechodzący test
    mimo np. braku implementacji.
    """

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._verification = IdentityVerification()

    def test_fails_for_an_invalid_identity_number(
        self, person_with_invalid_pesel: Person
    ) -> None:
        result = self._verification.passes(person_with_invalid_pesel)

        assert result is False

    @pytest.mark.xfail(
        reason="Teraz nie przejdzie, dopóki nie będzie dokończonej implementacji",
        strict=True,
    )
    def test_passes_for_a_valid_identity_number(
        self, person_with_valid_pesel: Person
    ) -> None:
        result = self._verification.passes(person_with_valid_pesel)

        assert result is True

    @pytest.fixture()
    def person_with_invalid_pesel(self) -> Person:
        return Person("jan", "kowalski", date.today(), Gender.MALE, "abcdefghijk")

    @pytest.fixture()
    def person_with_valid_pesel(self) -> Person:
        return Person("jan", "kowalski", date.today(), Gender.MALE, "49120966834")
