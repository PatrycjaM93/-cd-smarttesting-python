from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from smarttesting.customer.customer import Customer
from smarttesting.customer.person import Gender, Person, Status


class CustomerTestBase:
    """Klasa bazowa z przykładem buildera obiektu wykorzystywanego w teście."""

    @staticmethod
    def builder() -> "CustomerBuilder":
        return CustomerBuilder()


@dataclass
class CustomerBuilder:
    """Przykład buildera do setupu testów."""

    _uuid: UUID = field(default_factory=uuid4)
    _name: str = "Anna"
    _surname: str = "Kowalska"
    _date_of_birth: date = date(1978, 9, 12)
    _gender: Gender = Gender.FEMALE
    _national_id_number: str = "78091211463"
    _status: Status = Status.NOT_STUDENT

    def with_uuid(self, uuid: UUID) -> "CustomerBuilder":
        self._uuid = uuid
        return self

    def with_name(self, name: str) -> "CustomerBuilder":
        self._name = name
        return self

    def with_surname(self, surname: str) -> "CustomerBuilder":
        self._surname = surname
        return self

    def with_date_of_birth(self, year: int, month: int, day: int) -> "CustomerBuilder":
        self._date_of_birth = date(year, month, day)
        return self

    def with_gender(self, gender: Gender) -> "CustomerBuilder":
        self._gender = gender
        return self

    def with_national_id_number(self, national_id_number: str) -> "CustomerBuilder":
        self._national_id_number = national_id_number
        return self

    def with_status(self, status: Status) -> "CustomerBuilder":
        self._status = status
        return self

    def build(self) -> Customer:
        person = Person(
            self._name,
            self._surname,
            self._date_of_birth,
            self._gender,
            self._national_id_number,
        )
        customer = Customer(self._uuid, person)
        if self._status == Status.STUDENT:
            customer.student()
        return customer
