from dataclasses import dataclass
from uuid import UUID

from smarttesting.customer.person import Person


@dataclass
class Customer:
    """Klient. Klasa opakowująca osobę do zweryfikowania."""

    _uuid: UUID
    _person: Person

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def person(self) -> Person:
        return self._person

    @property
    def is_student(self) -> bool:
        return self._person.is_student

    def student(self) -> None:
        return self._person.student()
