from datetime import date

import pytest
from smarttesting.customer.person import Gender, Person


class TestPerson:
    @pytest.mark.homework(
        reason="Zrefaktoruj ten test. Czy na pewno musimy tyle weryfikować?"
    )
    def test_attributes_accessible(self) -> None:
        person = Person("name", "surname", date(2001, 11, 1), Gender.MALE, "1234567890")

        assert person.name == "name"
        assert person.surname == "surname"
        assert person.gender == Gender.MALE
        assert person.national_id_number == "1234567890"
        assert person.age >= 9
