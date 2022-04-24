from datetime import date

import pytest
from freezegun import freeze_time
from smarttesting.customer.person import Gender, Person


class TestPersonDone:
    """
    Pierwotny test testował gettery i settery, które jedynie zwracały ustawioną wartość.

    To, co na pewno powinniśmy przetestować to sposób liczenia wieku -
    tam nie jest zwracana ustawiona wartość wieku tylko jest on wyliczony.
    """

    def test_calculates_age_of_person(self) -> None:
        """Przykład udanego wyliczenia wieku z wykorzystaniem klasy potomnej."""

        class PersonUnderTest(Person):
            def _today(self) -> date:
                return date(2011, 11, 1)

        person = PersonUnderTest(
            "name", "surname", date(2001, 11, 1), Gender.MALE, "1234567890"
        )

        assert person.age == 10

    def test_calculates_age_of_person_using_freezegun(self) -> None:
        """Przykład udanego wyliczenia wieku z wykorzystaniem freezeguna."""
        person = Person("name", "surname", date(2001, 11, 1), Gender.MALE, "1234567890")

        with freeze_time("2011-11-01"):
            assert person.age == 10

    def test_raises_attribute_error_when_date_invalid(self) -> None:
        """Przykład wyliczenia wieku, który zakończy się rzuceniem wyjątku.

        Komentarz: W Pythonie z adnotacjami typów i mypy (lub innym narzędziem do ich
        weryfikacji) jesteśmy bezpieczni przed tego typu błędami gdyż zostaniemy
        ostrzeżeni.
        """
        person = Person(
            "name", "surname", None, Gender.MALE, "1234567890"  # type: ignore
        )

        with pytest.raises(AttributeError):
            # age to @property więc odwołanie się wywołuje przeliczenie
            person.age  # pylint: disable=pointless-statement
