import uuid
from dataclasses import fields
from datetime import date
from typing import Any, Dict, Type

import factory
from e2e.smarttesting.customer.customer import Customer
from e2e.smarttesting.customer.person import Gender, Person, Status


def _get_fields_mapping_for_dataclass(dataclass: Type) -> Dict[str, str]:
    return {
        field.name.lstrip("_"): field.name
        for field in fields(dataclass)
        if field.name.startswith("_")
    }


def _get_date_of_birth_from_age(person_being_constructed: Any) -> date:
    """Funkcja fabrykująca datę urodzenia zależnie od zadanego wieku.

    Nie będzie wywołana jeśli jawnie przekażemy `date_of_birth`.
    """
    if getattr(person_being_constructed, "age", None) is None:
        return date(1978, 9, 12)

    today = date.today()
    return today.replace(year=today.year - person_being_constructed.age)


class PersonFactory(factory.Factory):
    class Meta:
        model = Person
        rename = _get_fields_mapping_for_dataclass(Person)

    class Params:
        student = False
        age = None

    name = "Anna"
    surname = "Kowalska"
    date_of_birth = factory.LazyAttribute(_get_date_of_birth_from_age)
    gender = Gender.FEMALE
    national_id_number = "78091211463"
    status = factory.LazyAttribute(
        lambda o: Status.STUDENT if o.student else Status.NOT_STUDENT
    )


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer
        rename = _get_fields_mapping_for_dataclass(Customer)

    uuid = factory.LazyFunction(uuid.uuid4)
    person = factory.SubFactory(PersonFactory)


class AdultMalePersonFactory(PersonFactory):
    """Fabryka instancji `Person` używająca fakera."""

    name = factory.Faker("first_name_male")
    surname = factory.Faker("last_name")
    # faker nie wygeneruje nam PESELu, więc nasze dane nie przeszłyby weryfikacji
    # factory.Faker("date_between", start_date="-60y", end_date="-22y")
    date_of_birth = date(1989, 6, 6)
    gender = Gender.MALE
    national_id_number = "89060690710"


class AdultMaleCustomerFactory(CustomerFactory):
    person = factory.SubFactory(AdultMalePersonFactory)
