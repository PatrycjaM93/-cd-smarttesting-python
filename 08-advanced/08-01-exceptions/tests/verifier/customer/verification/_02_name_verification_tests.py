from datetime import date

import pytest
from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification import (
    _01_name_verification,
    _05_name_with_custom_exception_verification,
)
from smarttesting.verifier.customer.verification._04_verification_exception import (
    VerificationException,
)


class Test02NameVerification:
    """Wskazówka: Domyślnie pytest łapie wszystko, co printujemy na ekran.

    By wyłączyć to zachowanie, uruchamiamy go z flagą "-s".
    """

    def test_should_throw_an_exception_when_checking_verification(self) -> None:
        """Weryfikujemy czy został rzucony bardzo generyczny wyjątek AttributeError.

        Test ten przechodzi nam przypadkowo, gdyż AttributeError leci w innym miejscu
        w kodzie niż się spodziewaliśmy.

        Uruchamiając ten test nie widzimy żeby zalogowała nam się linijka z klasy
        `_01_name_verification.NameVerification`...
        """
        verification = _01_name_verification.NameVerification()

        with pytest.raises(AttributeError):
            verification.passes(self._person_without_name())

    @pytest.mark.xfail
    def test_should_throw_an_exception_when_checking_verification_only(self) -> None:
        """Poprawiona wersja poprzedniego testu, gdzie tym razem zweryfikujemy
        zawartość wiadomości w rzuconym wyjątku.

        Test nie przechodzi (tak się spodziewamy - dekorator @pytest.mark.xfail), gdyż
        nie jest rzucany nasz AttributeError pod if'em, tylko automatycznie gdy
        próbujemy na stringu "FEMALE" dobrać się do atrybutu `.name`.

        Zakomentuj linijkę `@pytest.mark.xfail`, by zobaczyć komunikat błędu.

        Problem polega na tym, że `_person_without_name` jest źle przygotowana, jednak
        nie byliśmy w stanie tego wyłapać poprzednim testem i uzyskaliśmy
        false-negative.
        """
        verification = _01_name_verification.NameVerification()

        with pytest.raises(AttributeError, match="Name cannot be None"):
            verification.passes(self._person_without_name())

    @pytest.mark.xfail
    def test_should_fail_verification_when_name_is_invalid(self) -> None:
        """W momencie, w którym nasza aplikacja rzuca wyjątki domenowe, wtedy nasz test
        może po prostu spróbować go wyłapać.

        Zakomentuj `@pytest.mark.xfail` żeby zobaczyć, że test się wysypuje gdyż
        wyjątek ktory poleci to AttributeError a nie VerificationException.
        """
        verification = (
            _05_name_with_custom_exception_verification.NameWithCustomExceptionVerification()
        )

        with pytest.raises(VerificationException):
            verification.passes(self._person_without_name())

    @pytest.mark.xfail
    def test_should_fail_verification_if_name_is_invalid_with_explicit_assertion(
        self,
    ) -> None:
        """Koncepcyjnie to samo co powyżej. Do zastosowania w momencie, w którym
        używana biblioteka nie posiada helpera do wyjątków, jak pytest czy unittest.

        Łapiemy w try..except wywołanie metody, która powinna rzucić wyjątek.
        Koniecznie należy wywalić test, jeżeli wyjątek nie został rzucony!!!

        W sekcji except możemy wykonywać dodatkowe asercje na wyjątku.
        """
        verification = (
            _05_name_with_custom_exception_verification.NameWithCustomExceptionVerification()
        )
        try:
            verification.passes(self._person_without_name())
            pytest.fail("Should fail the verification")
        except VerificationException:
            pass

    def _person_without_name(self) -> Person:
        """Celowo zepsuta instancja Person.

        Ma None zamiast imienia i string zamiast wartości z typu wyliczeniowego Gender.

        Weźmy pod uwagę, że przed takimi błędami zabezpiecza nas mypy
        (stąd komentarz # type: ignore by go wyłączyć w tej linii) lub jeżeli dane
        pochodzą z zewnątrz (np. z requestu) to wyłapać to powinna nasza biblioteka
        do walidacji, np. marshmallow czy pydantic.

        Niemniej, łapanie wbudowanych wyjątków trzeba robić bardzo świadomie i raczej
        nie powinniśmy nimi komunikować domenowych sytuacji wyjątkowych.
        """
        return Person(
            None, "Smith", date.today(), "FEMALE", "00000000000"  # type: ignore
        )
